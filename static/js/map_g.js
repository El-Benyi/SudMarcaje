document.addEventListener("DOMContentLoaded", function () {
    const map = L.map('map', {
        attributionControl: false
    }).setView([0, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    const markers = L.markerClusterGroup();
    const usuariosMarcados = {}; 

    fetch('/api/coordenadas')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(usuario => {
                    if (usuariosMarcados[usuario.nombre]) {
                        markers.removeLayer(usuariosMarcados[usuario.nombre]);
                    }

                    const fecha = new Date(usuario.fecha);
                    const fechaFormateada = fecha.toLocaleDateString('es-ES', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });

                    const marker = L.marker([usuario.lat, usuario.lon])
                        .bindPopup(`${usuario.nombre} está aquí<br>Fecha turno: ${fechaFormateada}<br>Inicio del turno: ${usuario.ini}<br>Fin del turno: ${usuario.fin} <br>Tiempo Activo: ${usuario.tiempo_trabajo}`);

                    markers.addLayer(marker);
                    usuariosMarcados[usuario.nombre] = marker;
                });

                map.addLayer(markers);
                map.fitBounds(markers.getBounds());
            } else {
                console.log("No hay usuarios para mostrar.");
            }
        })
        .catch(error => {
            console.error("Error al obtener las coordenadas:", error);
        });
});