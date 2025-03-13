document.addEventListener("DOMContentLoaded", function () {
    console.log("Script cargado correctamente.");

    const rememberCheckbox = document.querySelector(".remember-checkbox");
    const emailInput = document.querySelector("#mail");
    const passwordInput = document.querySelector("#pass");

    if (!rememberCheckbox || !emailInput || !passwordInput) {
        console.error("No se encontró uno de los elementos en el HTML.");
        return;
    }

    // Evento para guardar datos
    rememberCheckbox.addEventListener("change", function () {
        console.log("Checkbox cambiado:", this.checked);

        if (this.checked) {
            if (emailInput.value && passwordInput.value) {
                localStorage.setItem("savedEmail", emailInput.value);
                localStorage.setItem("savedPassword", passwordInput.value);
                localStorage.setItem("rememberMe", true);
                console.log("Datos guardados en localStorage.");
            } else {
                console.warn("Faltan valores en los campos.");
            }
        } else {
            localStorage.removeItem("savedEmail");
            localStorage.removeItem("savedPassword");
            localStorage.setItem("rememberMe", false);
            console.log("Datos eliminados de localStorage.");
        }
    });

    // Cargar datos al cargar la página
    const savedEmail = localStorage.getItem("savedEmail");
    const savedPassword = localStorage.getItem("savedPassword");
    const rememberMe = localStorage.getItem("rememberMe") === "true";

    if (rememberMe) {
        emailInput.value = savedEmail || "";
        passwordInput.value = savedPassword || "";
        rememberCheckbox.checked = true;
        console.log("Datos cargados desde localStorage.");
    }
});