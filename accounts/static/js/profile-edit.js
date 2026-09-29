document.addEventListener("DOMContentLoaded", () => {
  const editButton = document.getElementById("profile-edit-button");
  const saveButton = document.getElementById("profile-save-button");
  const profileFields = document.getElementById("profile-fields");
  const profileForm = document.getElementById("profile-form");
  const editStatus = document.getElementById("profile-edit-status");

  let editing = false;

  function setEditing(value) {
    editing = value;

    profileFields.disabled = !editing;

    saveButton.disabled = !editing;

    if (editing) {
      editButton.textContent = "✕";
      editButton.title = "Cancelar edición";
      editButton.setAttribute("aria-label", "Cancelar edición");
      editButton.classList.add("is-editing");
      editStatus.textContent = "MODO EDICIÓN";
      editStatus.classList.add("is-editing");
    } else {
      editButton.textContent = "✎";
      editButton.title = "Editar perfil";
      editButton.setAttribute("aria-label", "Editar perfil");
      editButton.classList.remove("is-editing");
      editStatus.textContent = "MODO LECTURA";
      editStatus.classList.remove("is-editing");
    }
  }

  editButton.addEventListener("click", () => {
    if (editing) {
      profileForm.reset();
      setEditing(false);
    } else {
      setEditing(true);
    }
  });

  setEditing(false);
});
