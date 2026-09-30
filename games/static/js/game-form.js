document.querySelectorAll(".game-platform-select").forEach((select) => {
    const nativeSelect = select.querySelector("select");
    const toggle = select.querySelector(".game-platform-toggle");
    const selected = select.querySelector(".game-platform-selected");
    const dropdown = select.querySelector(".game-platform-dropdown");

    toggle.addEventListener("click", () => {
        const isOpen = select.classList.toggle("is-open");

        toggle.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );
    });

    select.querySelectorAll(".game-platform-option").forEach((option) => {
        option.addEventListener("click", () => {
            const value = option.dataset.value;

            nativeSelect.value = value;

            nativeSelect.dispatchEvent(
                new Event("change", {
                    bubbles: true
                })
            );

            selected.innerHTML = option.innerHTML;

            select.classList.remove("is-open");

            toggle.setAttribute("aria-expanded", "false");
        });
    });

    document.addEventListener("click", (event) => {
        if (!select.contains(event.target)) {
            select.classList.remove("is-open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });

    if (nativeSelect.value) {
        const selectedOption = select.querySelector(
            `[data-value="${nativeSelect.value}"]`
        );

        if (selectedOption) {
            selected.innerHTML = selectedOption.innerHTML;
        }
    }
});