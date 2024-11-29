document.addEventListener("DOMContentLoaded", function() {
    const showClaveCheckbox = document.getElementById("show_clave");
    const showConfirmCheckbox = document.getElementById("show_confirm");
    const claveInput = document.getElementById("clave_input");
    const confirmInput = document.getElementById("confirm_input");

    // Mostrar/Ocultar contraseña principal
    showClaveCheckbox.addEventListener("change", function() {
        claveInput.type = this.checked ? "text" : "password";
    });

    // Mostrar/Ocultar confirmación de contraseña
    showConfirmCheckbox.addEventListener("change", function() {
        confirmInput.type = this.checked ? "text" : "password";
    });
});

