from flask import Flask, request, jsonify, render_template, redirect, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)

# Configurar la secret key para gestionar sesiones
app.secret_key = os.urandom(24)

CLIENT_ID = "61a8a0da61df40fa88d99be9d3a222f4"
CLIENT_SECRET = "e857b8e9d3664bcf8ebb7e5a04c30cd8"
SCOPE = "playlist-modify-public playlist-modify-private user-library-modify"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri="http://localhost:5000/callback/",
                            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback/')
def callback():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri="http://localhost:5000/callback/",
                            scope=SCOPE)
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        return redirect('/')
    else:
        return jsonify({"message": "Error en la autenticación."}), 400

@app.route('/api/add-to-playlist', methods=['POST'])
def add_to_playlist():
    data = request.json
    playlist_id = data['playlistId']
    songs = data['songs']
    
    token_info = session.get('token_info')  # Obtener el token de la sesión
    if not token_info:
        return jsonify({"message": "Autenticación requerida."}), 401

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    respuestas = []
    total = len(songs)
    for idx, song in enumerate(songs, start=1):
        try:
            respuestas.append({"cancion": song, "estado": f"Procesando {idx} de {total}..."})
            results = sp.search(q=song, type="track", limit=1)
            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']
                sp.playlist_add_items(playlist_id, [track_id])
                respuestas.append({"cancion": song, "estado": f"{idx} de {total} agregada exitosamente."})
            else:
                respuestas.append({"cancion": song, "estado": f"{idx} de {total} - No se encontró la canción."})
        except Exception as e:
            respuestas.append({"cancion": song, "estado": f"{idx} de {total} - Error: {str(e)}"})
    
    return jsonify({"mensaje": "Proceso completado.", "detalles": respuestas}), 200

if __name__ == '__main__':
    app.run(debug=True)