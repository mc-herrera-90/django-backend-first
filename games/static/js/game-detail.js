document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("retro-delete-modal");

  const message = document.getElementById("retro-delete-modal-message");

  const confirmButton = document.getElementById("retro-delete-modal-confirm");

  let activeForm = null;

  /* =====================================================
        ABRIR MODAL
        ===================================================== */

  document.querySelectorAll("[data-delete-modal]").forEach((button) => {
    button.addEventListener("click", () => {
      activeForm = button.closest("form");

      message.textContent =
        button.dataset.deleteMessage || "¿Quieres eliminar esta valoración?";

      modal.classList.add("is-open");

      modal.setAttribute("aria-hidden", "false");
    });
  });

  /* =====================================================
        CERRAR MODAL
        ===================================================== */

  document.querySelectorAll("[data-delete-close]").forEach((element) => {
    element.addEventListener("click", () => {
      modal.classList.remove("is-open");

      modal.setAttribute("aria-hidden", "true");

      activeForm = null;
    });
  });

  /* =====================================================
        CONFIRMAR ELIMINACIÓN
        ===================================================== */

  confirmButton.addEventListener("click", () => {
    if (activeForm) {
      activeForm.submit();
    }
  });

  /* =====================================================
        CERRAR CON ESC
        ===================================================== */

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-open")) {
      modal.classList.remove("is-open");

      modal.setAttribute("aria-hidden", "true");

      activeForm = null;
    }
  });
});
