
document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("lightbox");
  if (!box) return;
  const boxImg = box.querySelector("img");
  const closeBtn = box.querySelector(".lightbox-close");

  function closeLightbox() {
    box.classList.remove("open");
    boxImg.src = "";
    boxImg.alt = "";
  }

  document.querySelectorAll(".lightbox-trigger").forEach(img => {
    img.addEventListener("click", () => {
      boxImg.src = img.dataset.full || img.src;
      boxImg.alt = img.alt || "";
      box.classList.add("open");
    });
  });

  closeBtn?.addEventListener("click", closeLightbox);

  box.addEventListener("click", (ev) => {
    if (ev.target === box) closeLightbox();
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") closeLightbox();
  });
});
