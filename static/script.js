document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const playlistForm = document.getElementById('playlistForm');

    if (loginButton) {
        loginButton.addEventListener('click', function() {
            window.location.href = '/login';
        });
    }

    if (playlistForm) {
        playlistForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const playlistId = document.getElementById('playlistId').value;
            const songs = document.getElementById('songs').value.split(',').map(s => s.trim());
            
            const response = await fetch('/api/add-to-playlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ playlistId, songs })
            });
            
            const result = await response.json();
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '';

            if (response.ok) {
                result.detalles.forEach(detalle => {
                    const p = document.createElement('p');
                    p.textContent = `Canción: ${detalle.cancion} - Estado: ${detalle.estado}`;
                    responseDiv.appendChild(p);
                });
            } else if (result.message === "Autenticación requerida.") {
                const p = document.createElement('p');
                p.textContent = "Se requiere autenticación. Por favor, utiliza el botón de autorizar.";
                responseDiv.appendChild(p);
            } else {
                const p = document.createElement('p');
                p.textContent = result.message;
                responseDiv.appendChild(p);
            }
        });
    }
});