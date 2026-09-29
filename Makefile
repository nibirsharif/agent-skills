.PHONY: help install uninstall test eval

help:
	@echo "make install    symlink skills into ~/.agents/skills and ~/.claude/skills (TARGET=dir to override)"
	@echo "make uninstall  remove the symlinks this repo created"
	@echo "make test       validate every skill and run the unit tests (free, no agent calls)"
	@echo "make eval       run eval cases through an agent (paid): SKILL=name, MODEL=, RUNS=, JUDGE=1"

install:
	./setup.sh $(if $(TARGET),--target $(TARGET))

uninstall:
	./setup.sh --uninstall $(if $(TARGET),--target $(TARGET))

test:
	./test.sh

# Without SKILL, runs every skill that has evals/<skill>/config.json, one after another.
eval:
	@status=0; for skill in $(or $(SKILL),$(patsubst evals/%/config.json,%,$(wildcard evals/*/config.json))); do \
	  python3 evals/run.py $$skill $(if $(MODEL),--model $(MODEL)) $(if $(RUNS),--runs $(RUNS)) $(if $(JUDGE),--judge) || status=1; \
	done; exit $$status
