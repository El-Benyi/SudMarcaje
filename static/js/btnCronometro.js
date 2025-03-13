document.addEventListener("DOMContentLoaded", function () {
    const fecha = document.getElementById("fecha");
    const turno = document.getElementById("turno");
    const iniciar = document.getElementById("ini_turno");
    const detener = document.getElementById("fin_turno");

    if (localStorage.getItem("fecha")) {
        fecha.value = localStorage.getItem("fecha");
    }
    if (localStorage.getItem("turno")) {
        turno.value = localStorage.getItem("turno");
    }

    fecha.addEventListener("input", function () {
        localStorage.setItem("fecha", fecha.value);
        verificarCampos();
    });

    turno.addEventListener("input", function () {
        localStorage.setItem("turno", turno.value);
        verificarCampos();
    });

    function verificarCampos() {
        if (fecha.value && turno.value) {
            iniciar.disabled = false;
        } else {
            iniciar.disabled = true;
        }
    }

    if (localStorage.getItem("turnoIniciado") === "true") {
        iniciar.disabled = true;
        turno.disabled = true;
        fecha.disabled = true;
        detener.disabled = false; 
    } else {
        detener.disabled = true; 
    }

    iniciar.addEventListener("click", function () {
        turno.disabled = true;
        fecha.disabled = true;
        iniciar.disabled = true;
        detener.disabled = false; 
        localStorage.setItem("turnoIniciado", "true"); 
    });

    detener.addEventListener("click", function () {
        turno.disabled = false;
        fecha.disabled = false;
        iniciar.disabled = false;
        detener.disabled = true; 
        localStorage.removeItem("turnoIniciado"); 
    });
});
