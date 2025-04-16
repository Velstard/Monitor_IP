document.addEventListener("DOMContentLoaded", function () {
    const paginationLinks = document.querySelectorAll(".pagination .page-link");

    paginationLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            // Obtener la URL del enlace
            const url = new URL(this.href);

            // Actualizar los parámetros de la URL
            const params = new URLSearchParams(url.search);

            // Redirigir a la nueva URL
            window.location.href = `${url.pathname}?${params.toString()}`;
        });
    });
});