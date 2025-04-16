document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            event.preventDefault(); // Evitar el envío del formulario
            alert("Por favor, completa todos los campos.");
        }
    });

    const togglePassword = document.getElementById("togglePassword");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
        const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
        passwordField.setAttribute("type", type);
        this.textContent = type === "password" ? "Mostrar" : "Ocultar";
    });

    const loginForm = document.getElementById("login-form");

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

    // Simular validación de inicio de sesión
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar el envío del formulario para pruebas

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Validación simulada
        if (username !== "admin" || password !== "password123") {
            showFlashMessage("Usuario o contraseña incorrectos.", "error");
        } else {
            showFlashMessage("Inicio de sesión exitoso.", "success");
            // Aquí puedes redirigir al usuario o enviar el formulario
            // window.location.href = "/status";
        }
    });
});
