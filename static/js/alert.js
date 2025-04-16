document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-ip-form");
    const ipField = document.getElementById("ip");
    const nameField = document.getElementById("name");
    const ipError = document.getElementById("ip-error");
    const nameError = document.getElementById("name-error");
    const successMessage = document.getElementById("success-message"); // Elemento para mostrar mensajes de éxito

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar el envío del formulario por defecto

        const formData = new FormData(form);

        fetch("/add", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Limpiar errores anteriores
            ipError.classList.add("d-none");
            nameError.classList.add("d-none");
            successMessage.classList.add("d-none");

            if (data.status === "error") {
                // Mostrar errores específicos
                if (data.message.includes("IP")) {
                    ipError.textContent = data.message;
                    ipError.classList.remove("d-none");
                } else if (data.message.includes("nombre")) {
                    nameError.textContent = data.message;
                    nameError.classList.remove("d-none");
                }
            } else if (data.status === "success") {
                // Mostrar mensaje de éxito y cerrar el modal
                successMessage.textContent = data.message;
                successMessage.classList.remove("d-none");
                $('#addPage').modal('hide'); // Cerrar el modal (requiere jQuery)
                form.reset(); // Limpiar el formulario
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});

feather.replace();
