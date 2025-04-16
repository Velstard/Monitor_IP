document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-ip-form");
    const ipField = document.getElementById("ip");
    const nameField = document.getElementById("name");
    const ipError = document.getElementById("ip-error");
    const nameError = document.getElementById("name-error");

    // Función para validar una dirección IP
    function isValidIP(ip) {
        const ipRegex = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
        return ipRegex.test(ip);
    }

    form.addEventListener("submit", function (event) {
        let valid = true;

        // Validar dirección IP
        if (!isValidIP(ipField.value.trim())) {
            ipError.classList.remove("d-none");
            ipError.textContent = "La dirección IP no es válida.";
            valid = false;
        } else {
            ipError.classList.add("d-none");
        }

        // Validar nombre
        if (nameField.value.trim() === "") {
            nameError.classList.remove("d-none");
            nameError.textContent = "El nombre no puede estar vacío.";
            valid = false;
        } else {
            nameError.classList.add("d-none");
        }

        // Si no es válido, prevenir el envío del formulario
        if (!valid) {
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Función para mostrar mensajes flash dinámicos
    function showFlashMessage(message, category) {
        const flashContainer = document.getElementById("dynamic-flash-messages");

        // Crear el elemento del mensaje flash
        const flashMessage = document.createElement("div");
        flashMessage.className = `alert alert-${category} mt-3 flash-message`;
        flashMessage.textContent = message;

        // Agregar el mensaje al contenedor
        flashContainer.appendChild(flashMessage);

        // Se eliminara el mensaje después de 5 segundos
        setTimeout(() => {
            flashMessage.remove();
        }, 5000);
    }

  
    
    showFlashMessage("No estás autorizado para realizar esta acción.", "danger");
 
});


CKEDITOR.replace( 'editor1' );
      $(document).ready(function(){
        $(document).on('mousemove',function(e){
        $("#cords").html("Cords: Y: "+e.clientY);
        })
      });

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

 // Recargar la página automáticamente cada 5 minutos 
 setTimeout(function () {
    location.reload();
}, 300000); // 300,000 ms = 5 minutos