document.addEventListener("DOMContentLoaded", function () {
    // Comprobar si la ubicación ya ha sido obtenida
    if (localStorage.getItem('ubicacionObtenida') !== 'true') {
        // Verificar si el navegador soporta la geolocalización
        if (navigator.geolocation) {
            const permiso = confirm("Esta página necesita acceder a tu ubicación. ¿Permites el acceso?");
            if (permiso) {
                // Obtener la ubicación del usuario
                navigator.geolocation.getCurrentPosition(function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    // Depurar: Mostrar las coordenadas obtenidas
                    console.log("Ubicación actual:", lat, lon);

                    // Verificar si las coordenadas son válidas
                    if (lat && lon) {
                        // Guardar las coordenadas en el localStorage
                        localStorage.setItem('lat', lat);
                        localStorage.setItem('lon', lon);
                        localStorage.setItem('ubicacionObtenida', 'true');

                        console.log("Latitud y longitud asignada:");
                        console.log("Latitud:", lat);
                        console.log("Longitud:", lon);

                        // Sincronizar las coordenadas con los campos del formulario
                        document.getElementById('lat').value = lat;
                        document.getElementById('lon').value = lon;
                    } else {
                        console.error("No se obtuvieron coordenadas válidas.");
                    }

                    // Disparar un evento para notificar que la ubicación ha sido obtenida
                    window.dispatchEvent(new CustomEvent('ubicacionObtenida', { detail: { lat, lon } }));
                }, function (error) {
                    console.error("Error al obtener la geolocalización:", error);
                    alert("No se pudo obtener la ubicación.");
                });
            }
        } else {
            alert("La geolocalización no está disponible en tu navegador.");
        }
    } else {
        // Si la ubicación ya fue obtenida, sincronizarla con el formulario
        const lat = localStorage.getItem('lat');
        const lon = localStorage.getItem('lon');

        // Verificar si las coordenadas están en el localStorage
        if (lat && lon) {
            document.getElementById('lat').value = lat;
            document.getElementById('lon').value = lon;
            console.log("Ubicación obtenida previamente:", lat, lon);
        } else {
            console.error("No se encontraron coordenadas en el localStorage.");
        }
    }

    // Escuchar el evento personalizado 'ubicacionObtenida'
    window.addEventListener('ubicacionObtenida', function (event) {
        const { lat, lon } = event.detail;
        console.log("Ubicación obtenida mediante evento:", lat, lon);
        // Realizar otras acciones, como actualizar el mapa o enviar las coordenadas a un servidor
    });
});