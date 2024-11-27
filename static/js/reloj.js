function actualizarHora() {
    const reloj = document.getElementById("reloj");
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString("es-ES", { hour12: false });
    reloj.textContent = hora;
}

// Actualiza la hora cada segundo
setInterval(actualizarHora, 1000);