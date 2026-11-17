// Draw the notes of notes.json as a list.
function render(notes) {
  const list = document.getElementById("notes");
  list.replaceChildren();
  for (const note of notes) {
    const item = document.createElement("li");
    item.textContent = note.text;
    list.appendChild(item);
  }
}

fetch("notes.json").then((response) => response.json()).then(render);
