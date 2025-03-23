let cronometro;
let seg = 0, min = 0, hora = 0;

const contador = document.getElementById("contador");
const iniciar = document.getElementById("ini_turno");
const turno = document.getElementById("turno");
const detener = document.getElementById("fin_turno");
const formulario = document.querySelector("form");
const fecha = document.getElementById("fecha");

const obtenerHoraLocal = () => {
    const ahora = new Date();
    const year = ahora.getFullYear();
    const month = (ahora.getMonth() + 1).toString().padStart(2, "0");
    const day = ahora.getDate().toString().padStart(2, "0");
    const hours = ahora.getHours().toString().padStart(2, "0");
    const minutes = ahora.getMinutes().toString().padStart(2, "0");
    const seconds = ahora.getSeconds().toString().padStart(2, "0");

    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
};

function iniciarCronometro() {
    if (!localStorage.getItem("horaInicio")) {
        horaInicio = obtenerHoraLocal();  
        localStorage.setItem("horaInicio", horaInicio);  
    } else {
        horaInicio = localStorage.getItem("horaInicio");  
    }

    calcularTiempoTranscurrido();  

    cronometro = setInterval(() => {
        seg++;
        if (seg === 60) {
            seg = 0;
            min++;
            if (min === 60) {
                min = 0;
                hora++;
            }
        }

        contador.textContent = `${hora.toString().padStart(2, "0")}:${min.toString().padStart(2, "0")}:${seg.toString().padStart(2, "0")}`;
    }, 1000);
}

function calcularTiempoTranscurrido() {
    const horaInicio = new Date(localStorage.getItem("horaInicio")).getTime();  
    const ahora = Date.now();  

    const tiempoTranscurrido = Math.floor((ahora - horaInicio) / 1000);  
    hora = Math.floor(tiempoTranscurrido / 3600);  
    min = Math.floor((tiempoTranscurrido % 3600) / 60);  
    seg = tiempoTranscurrido % 60;  

    contador.textContent = `${hora.toString().padStart(2, "0")}:${min.toString().padStart(2, "0")}:${seg.toString().padStart(2, "0")}`;
}

iniciar.addEventListener("click", function () {
    iniciarCronometro();  
    iniciar.disabled = true;  
    detener.disabled = false;  

    const latitud = document.getElementById("lat").value;
    const longitud = document.getElementById("lon").value;
    const turnoValue = turno.value;
    const fecha = document.getElementById("fecha").value;

    const data = {
        latitud: latitud,
        longitud: longitud,
        turno: turnoValue,
        fecha_registro: fecha,
        hora_inicio: horaInicio,  
        estado: true,  
        usuario_id: 1  
    };

    fetch("/asistencia", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del backend:", data);
    })
    .catch(error => {
        console.error("Error al enviar datos:", error);
    });
});

detener.addEventListener("click", function () {
    clearInterval(cronometro);  
    localStorage.removeItem("horaInicio");  

    const horaFin = obtenerHoraLocal();  

    const latitud = document.getElementById("lat").value;
    const longitud = document.getElementById("lon").value;
    const turnoValue = turno.value;
    const fecha = document.getElementById("fecha").value; 

    const data = {
        latitud: latitud,
        longitud: longitud,
        turno: turnoValue,
        fecha_registro: fecha,
        hora_inicio: horaInicio,  
        hora_fin: horaFin,  
        tiempo_trabajo: `${hora.toString().padStart(2, "0")}:${min.toString().padStart(2, "0")}:${seg.toString().padStart(2, "0")}`,  
        usuario_id: 1  
    };

    fetch("/asistencia", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del backend:", data);
    })
    .catch(error => {
        console.error("Error al enviar datos:", error);
    });

    detener.disabled = true;
    iniciar.disabled = false;
});

window.addEventListener("load", function () {
    if (localStorage.getItem("horaInicio")) {
        iniciarCronometro();  
    }
});