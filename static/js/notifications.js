document.addEventListener("DOMContentLoaded", function () {
    // Realiza una solicitud para obtener la cantidad de usuarios pendientes
    fetch("/api/pending_users_count")
        .then(response => response.json())
        .then(data => {
            const pendingCount = data.count || 0;
            const badge = document.getElementById("pending-count");

            // Actualiza el contador en el botón
            badge.textContent = pendingCount;

            // Oculta el badge si no hay usuarios pendientes
            if (pendingCount === 0) {
                badge.style.display = "none";
            }
        })
        .catch(error => {
            console.error("Error al obtener la cantidad de usuarios pendientes:", error);
        });
});

document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    // Función para mostrar mensajes flash dinámicos
    function showFlashMessage(message, category) {
        const flashContainer = document.getElementById("dynamic-flash-messages");

        // Crear el elemento del mensaje flash
        const flashMessage = document.createElement("div");
        flashMessage.className = `flash-message ${category}`;
        flashMessage.textContent = message;

        // Agregar el mensaje al contenedor
        flashContainer.appendChild(flashMessage);

        // Eliminar el mensaje después de 5 segundos
        setTimeout(() => {
            flashMessage.remove();
        }, 5000);
    }

    // Simular validación de registro
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar el envío del formulario para pruebas

        // Simular mensaje de registro exitoso
        showFlashMessage("Registro exitoso. Tu cuenta está pendiente de aprobación por un administrador o DM.", "success");

        // Aquí puedes redirigir al usuario o enviar el formulario al backend
        // registerForm.submit();
    });
});