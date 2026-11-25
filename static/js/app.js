function copyHash() {
  const hash = document.getElementById("hash");
  if (!hash) return;
  navigator.clipboard.writeText(hash.textContent)
    .then(() => {
      const button = document.querySelector(".copy");
      const previous = button.textContent;
      button.textContent = "Copiado";
      setTimeout(() => button.textContent = previous, 1400);
    })
    .catch(() => alert("No se pudo copiar automáticamente. Selecciona el hash y cópialo."));
}
