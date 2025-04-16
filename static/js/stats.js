document.addEventListener("DOMContentLoaded", function () {
    // Actualizar estadísticas de usuarios e IPs
    fetch("/api/stats")
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-users").textContent = data.total_users;
            document.getElementById("total-ips").textContent = data.total_ips;
        })
        .catch(error => console.error("Error al obtener las estadísticas:", error));
});