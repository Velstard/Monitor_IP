document.addEventListener("DOMContentLoaded", function () {
    // Tiempo total en segundos para el próximo monitoreo (5 minutos = 300 segundos)
    const totalTime = 300;

    // Recuperar el tiempo restante del almacenamiento local o establecerlo en el tiempo total
    let countdownTime = localStorage.getItem("countdownTime")
        ? parseInt(localStorage.getItem("countdownTime"))
        : totalTime;

    // Guardar el tiempo restante en el almacenamiento local cada segundo
    function saveCountdownTime() {
        localStorage.setItem("countdownTime", countdownTime);
    }

    // Función para actualizar el cronómetro
    function updateCountdown() {
        const minutes = Math.floor(countdownTime / 60);
        const seconds = countdownTime % 60;

        // Formatear el tiempo como MM:SS
        const formattedTime = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
        document.getElementById("countdown").textContent = formattedTime;

        // Reducir el tiempo restante
        if (countdownTime > 0) {
            countdownTime--;
            saveCountdownTime(); // Guardar el tiempo restante
        } else {
            // Reiniciar el cronómetro cuando llegue a 0
            countdownTime = totalTime;
            saveCountdownTime(); // Reiniciar el tiempo en el almacenamiento local
        }
    }

    // Actualizar el cronómetro cada segundo
    setInterval(updateCountdown, 1000);
});