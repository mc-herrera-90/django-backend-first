document.addEventListener("DOMContentLoaded", () => {
  const actors = document.querySelectorAll(".cast-person");

  let activeActor = null;
  let activePopover = null;

  const closeActive = () => {
    if (activePopover) {
      activePopover.hide();
      activePopover.dispose();
    }

    if (activeActor) {
      activeActor.classList.remove("active");
    }

    activeActor = null;
    activePopover = null;
  };

  actors.forEach((actor) => {
    let personData = null;
    let loading = false;

    const showPopover = (content) => {
      if (activePopover) {
        activePopover.hide();
        activePopover.dispose();
      }

      if (activeActor) {
        activeActor.classList.remove("active");
      }

      activeActor = actor;
      actor.classList.add("active");

      activePopover = new bootstrap.Popover(actor, {
        html: true,
        content,
        placement: "top",
        trigger: "manual",
        container: "body",
        customClass: "wikipedia-popover-container",

        popperConfig(defaultConfig) {
          return {
            ...defaultConfig,

            modifiers: [
              {
                name: "flip",
                enabled: false,
              },
              {
                name: "preventOverflow",
                options: {
                  boundary: "viewport",
                  padding: 10,
                },
              },
            ],
          };
        },
      });

      activePopover.show();
    };

    const showLoading = () => {
      showPopover(`
        <div class="wikipedia-popover wikipedia-popover-loading">
          <div class="wikipedia-popover-loader"></div>
          <span>Buscando información...</span>
        </div>
      `);
    };

    const showPerson = (person) => {
      showPopover(`
        <div class="wikipedia-popover">

          ${
            person.image
              ? `
                <div class="wikipedia-popover-image-wrapper">
                  <img
                    src="${person.image}"
                    alt="${person.title}"
                    class="wikipedia-popover-image"
                  >
                </div>
              `
              : ""
          }

          <div class="wikipedia-popover-body">

            <h5>${person.title}</h5>

            ${
              person.description
                ? `
                  <p class="wikipedia-popover-description">
                    ${person.description}
                  </p>
                `
                : ""
            }

            ${
              person.extract
                ? `
                  <p class="wikipedia-popover-extract">
                    ${person.extract}
                  </p>
                `
                : ""
            }

            ${
              person.url
                ? `
                  <a
                    href="${person.url}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="wikipedia-popover-link"
                  >
                    Ver en Wikipedia
                  </a>
                `
                : ""
            }

          </div>

        </div>
      `);
    };

    const loadPerson = async () => {
      if (loading || personData) {
        return;
      }

      loading = true;

      try {
        const response = await fetch(
          `/api/wikipedia/person/?name=${encodeURIComponent(
            actor.dataset.person
          )}`
        );

        if (!response.ok) {
          throw new Error("No se encontró información");
        }

        const data = await response.json();

        /*
         * Precargar la imagen antes de
         * mostrar el contenido.
         */
        if (data.image) {
          const image = new Image();

          image.src = data.image;

          await new Promise((resolve) => {
            image.onload = resolve;
            image.onerror = resolve;
          });
        }

        personData = data;

        /*
         * Si el actor sigue siendo el activo,
         * reemplazamos el loading por los datos.
         */
        if (activeActor === actor) {
          showPerson(personData);
        }

      } catch (error) {
        console.error("Wikipedia:", error);

        if (activeActor === actor) {
          showPopover(`
            <div class="wikipedia-popover-error">
              No se encontró información.
            </div>
          `);
        }

      } finally {
        loading = false;
      }
    };


    /* =====================================================
       HOVER → PRE-CARGAR
       ===================================================== */

    actor.addEventListener("mouseenter", () => {
      loadPerson();
    });


    /* =====================================================
       CLICK → MOSTRAR
       ===================================================== */

    actor.addEventListener("click", (event) => {
      event.stopPropagation();

      /*
       * Si ya está seleccionado,
       * cerramos el popover.
       */
      if (activeActor === actor) {
        closeActive();
        return;
      }

      /*
       * Si había otro actor abierto,
       * lo cerramos primero.
       */
      if (activeActor) {
        closeActive();
      }

      /*
       * Si los datos ya están cargados,
       * mostramos inmediatamente.
       */
      if (personData) {
        showPerson(personData);
        return;
      }

      /*
       * Si todavía no están cargados,
       * mostramos loading.
       */
      showLoading();

      loadPerson();
    });
  });


  /* =====================================================
     CLICK FUERA → CERRAR
     ===================================================== */

  document.addEventListener("click", (event) => {
    const popover = document.querySelector(
      ".wikipedia-popover-container"
    );

    if (
      activeActor &&
      event.target !== activeActor &&
      !activeActor.contains(event.target) &&
      (!popover || !popover.contains(event.target))
    ) {
      closeActive();
    }
  });
});