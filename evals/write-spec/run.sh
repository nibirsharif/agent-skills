#!/usr/bin/env bash
# Run eval cases through an agent, in parallel, and grade each reply.
# Usage: evals/write-spec/run.sh [case ...]    (no case: run them all)
#
# Environment:
#   MODEL=<name>   model for the default agent, for example sonnet or haiku (default: the CLI's default)
#   RUNS=<n>       run each case n times (default 1), to see how much results vary
#   AGENT="<cmd>"  use another agent command; it gets the prompt as its last argument
#   EVAL_TIMEOUT   seconds per run when the case's checks.json sets no "timeout_seconds" (default 600)
#
# Default agent: claude -p, allowed to read the skill folder and run its lint without prompting.
# With it, each run also records turns, time, cost, how often the lint ran, and the full transcript. All runs start at once, so a full run
# takes about as long as the slowest case.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill="$(cd "$here/../../skills/write-spec" && pwd)"
runs="${RUNS:-1}"

if [ -n "${AGENT:-}" ]; then
  read -r -a agent <<< "$AGENT"
else
  # A headless run cannot answer permission prompts, so allow what the skill needs up front:
  # reading its own files, writing a draft in the run folder, and running the lint.
  # --add-dir and --allowedTools take lists, so a flag with no value must follow them;
  # otherwise the prompt would be read as one more list item.
  agent=(claude -p
    --add-dir "$skill" "$HOME/.claude/skills/write-spec"
    --allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)" "Bash(cat:*)"
    --no-session-persistence --output-format stream-json --verbose)
  if [ -n "${MODEL:-}" ]; then agent+=(--model "$MODEL"); fi
fi

# Run one case once and print its report. Returns 1 when the run or the grade fails.
run_case() {
  local name="$1" out="$2" case_dir="$here/cases/$1" limit prompt dir
  limit="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("timeout_seconds", sys.argv[2]))' \
    "$case_dir/checks.json" "${EVAL_TIMEOUT:-600}")"
  prompt="Use the write-spec skill. Reply in chat only and do not save a requirements file.

$(cat "$case_dir/input.md")"
  # Run in an empty folder so no project config or files affect the reply. Empty stdin so the
  # agent never waits on the terminal. perl's alarm stands in for timeout(1), which macOS lacks.
  dir="$(mktemp -d "${TMPDIR:-/tmp}/write-spec-eval.XXXXXX")" || { echo "FAIL could not create an empty run folder"; return 1; }
  if ! (cd "$dir" && perl -e 'alarm shift; exec @ARGV' "$limit" "${agent[@]}" "$prompt" < /dev/null) \
      > "$out" 2> "${out%.md}.err"; then
    echo "FAIL agent exited with an error or passed the ${limit}s limit; see ${out#$here/} and its .err file"
    return 1
  fi
  [ -s "${out%.md}.err" ] || rm -f "${out%.md}.err"
  if [ -z "${AGENT:-}" ]; then
    # Split the stream into the reply, its stats (including lint runs), and the transcript.
    python3 "$here/parse_run.py" "$out"
  fi
  echo "   reply: ${out#$here/}"
  python3 "$here/grade.py" "$case_dir" "$out"
}

cases=("$@")
if [ ${#cases[@]} -eq 0 ]; then cases=($(ls "$here/cases")); fi
mkdir -p "$here/runs"
stamp="$(date +%Y%m%d-%H%M%S)"
labels=() pids=() logs=()
for name in "${cases[@]}"; do
  for i in $(seq 1 "$runs"); do
    out="$here/runs/$name-$stamp-r$i${MODEL:+-$MODEL}.md"
    run_case "$name" "$out" > "${out%.md}.log" 2>&1 &
    labels+=("$name run $i") pids+=($!) logs+=("${out%.md}.log")
  done
done
echo "Started ${#pids[@]} runs${MODEL:+ on $MODEL}. Waiting..."

status=0 results=()
for k in "${!pids[@]}"; do
  if wait "${pids[$k]}"; then results+=("PASS  ${labels[$k]}"); else results+=("FAIL  ${labels[$k]}"); status=1; fi
  echo; echo "== ${labels[$k]}"; cat "${logs[$k]}"; rm -f "${logs[$k]}"
done
echo; echo "== Summary${MODEL:+ ($MODEL)}"
printf '%s\n' "${results[@]}"
exit $status
