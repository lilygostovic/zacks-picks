import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config["SESSION_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = "wernkwebfbdkfjbwksjbfoarwob"
TOKEN_INFO = "token_info"


@app.route("/")
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("update_zacks_picks", _external=True))


@app.route("/updateZacksPicks")
def update_zacks_picks():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user_id = sp.current_user()["id"]

    zacks_picks_id = None

    # save playlist ID if playlist exists
    current_playlists = sp.current_user_playlists()["items"]
    for playlist in current_playlists:
        if playlist["name"] == "Zacks Picks":
            zacks_picks_id = playlist["id"]

    # create new playlist and save ID if it does not exist
    if not zacks_picks_id:
        new_playlist = sp.user_playlist_create(user_id, "Zacks Picks")
        zacks_picks_id = new_playlist["id"]

    # remove old tracks from playlist
    tracks = sp.playlist_items(zacks_picks_id)
    if tracks["total"] != 0:
        sp.playlist_remove_all_occurrences_of_items(zacks_picks_id, tracks)

    # find URIs of new songs
    track_uris = []

    # add new tracks to playlist
    # sp.user_playlist_add_tracks(user_id, zacks_picks_id, track_uris)

    return "Success!"


def get_token():
    token_info = session.get(TOKEN_INFO)
    if not (token_info):
        redirect(url_for("login", _external=False))

    now = int(time.time())

    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


def create_spotify_oauth():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("redirect_page", _external=True),
        scope="user-library-read playlist-modify-public playlist-modify-private",
    )


app.run(debug=True)
