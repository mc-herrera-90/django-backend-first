document.querySelectorAll("[data-game-card]").forEach((card) => {
  const video = card.querySelector("[data-game-video]");

  if (!video) {
    return;
  }

  let hoverTimer = null;

  card.addEventListener("mouseenter", () => {
    hoverTimer = setTimeout(async () => {
      try {
        video.load();

        await video.play();

        card.classList.add("is-playing");
      } catch (error) {
        console.error("No se pudo reproducir el gameplay:", error);
      }
    }, 1300);
  });

  card.addEventListener("mouseleave", () => {
    clearTimeout(hoverTimer);

    video.pause();

    video.currentTime = 0;

    card.classList.remove("is-playing");
  });
});
