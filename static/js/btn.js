document.addEventListener("DOMContentLoaded", function() {
    const showClaveCheckbox = document.getElementById("show_clave");
    const showConfirmCheckbox = document.getElementById("show_confirm");
    const claveInput = document.getElementById("clave_input");
    const confirmInput = document.getElementById("confirm_input");

    showClaveCheckbox.addEventListener("change", function() {
        claveInput.type = this.checked ? "text" : "password";
    });

    showConfirmCheckbox.addEventListener("change", function() {
        confirmInput.type = this.checked ? "text" : "password";
    });
    document.getElementById('delete_user').addEventListener('click', function() {
        if (confirm("¿Estás seguro de que deseas eliminar este trabajador?")) {
            document.getElementById('delete_form').submit();
        }
    });
});






