'''
    This code was based on these repositories,
    so special thanks to:
        https://github.com/datademofun/spotify-flask
        https://github.com/drshrey/spotify-flask-auth-example

'''

from flask import Flask, request, redirect, g, render_template, session
from spotify_requests import spotify
from songkick_requests import songkick
from map_creator import folium

app = Flask(__name__)
app.secret_key = 'some key for session'

# ----------------------- AUTH API PROCEDURE -------------------------

@app.route("/auth")
def auth():
    return redirect(spotify.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header
    session['map'] = "null"
    return profile('long_term')

def valid_token(resp):
    return resp is not None and not 'error' in resp

# -------------------------- API REQUESTS ----------------------------


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    try:
        search_type = request.args['search_type']
        name = request.args['name']
        return make_search(search_type, name)
    except:
        return render_template('search.html')


@app.route('/search/<search_type>/<name>')
def search_item(search_type, name):
    return make_search(search_type, name)


def make_search(search_type, name):
    if search_type not in ['artist', 'album', 'playlist', 'track']:
        return render_template('index.html')

    data = spotify.search(search_type, name)
    api_url = data[search_type + 's']['href']
    items = data[search_type + 's']['items']

    return render_template('search.html',
                           name=name,
                           results=items,
                           api_url=api_url,
                           search_type=search_type)


@app.route('/artist/<id>')
def artist(id):
    auth_header = session['auth_header']
    artist = spotify.get_artist(auth_header, id)

    if artist['images']:
        image_url = artist['images'][0]['url']
    else:
        image_url = 'http://bit.ly/2nXRRfX'

    tracksdata = spotify.get_artist_top_tracks(auth_header, id)
    tracks = tracksdata['tracks']

    albums = spotify.get_artist_albums(auth_header, id)

    on_tour = songkick.get_artist_info(artist['name'])
    image_id = image_url.replace("https://i.scdn.co/image/", "")
    return render_template('artist.html',
                           artist=artist,
                           image_url=image_url,
                           tracks=tracks,
                           albums=albums["items"],
                           on_tour=on_tour,
                           image_id=image_id)




@app.route('/profile/<time_range>')
def profile(time_range):
    if time_range not in ['long_term', 'medium_term', 'short_term']:
        print('invalid type')
        return None
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        profile_data = spotify.get_users_profile(auth_header)
        # get users top artists
        top_artists = spotify.get_users_top(auth_header, 'artists', time_range, 50)
        # get users top tracks
        top_tracks = spotify.get_users_top(auth_header, 'tracks', time_range, 50)
        #on_tour = []
        #for artist_name in top_artists["items"]:
        #    on_tour.append(songkick.get_artist_info(artist_name['name']))
        if valid_token(top_artists):
            return render_template("profile.html",
                               user=profile_data,
                               top_artists=top_artists["items"],
                               top_tracks=top_tracks["items"])

    return render_template('profile.html')

@app.route('/album/<id>')
def album(id):
    if 'auth_header' in session:
        auth_header = session['auth_header']
        album_tracks = spotify.get_album_tracks(auth_header, id)
        album_info = spotify.get_album(auth_header, id)
        if valid_token(album_tracks):
            return render_template("album.html",
                                   album_tracks=album_tracks["items"],
                                   album_info=album_info)
@app.route('/concerts/<songkick_id>/<name>/<image_id>')
def concerts(songkick_id, name, image_id):
    if 'auth_header' in session:
        auth_header = session['auth_header']
        artist_concerts = songkick.get_artist_concerts(songkick_id)
        concert_map = folium.create_map(artist_concerts['resultsPage']['results']['event'])
        session['map'] = concert_map
        image_url = 'https://i.scdn.co/image/'+image_id
        if valid_token(artist_concerts):
            return render_template("concerts.html",
                                   artist_concerts=artist_concerts['resultsPage']['results']['event'],
                                   image_url=image_url,
                                   name=name)

@app.route('/map')
def show_map():
    return render_template("map.html",
                           map=session['map'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/featured_playlists')
def featured_playlists():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        hot = spotify.get_featured_playlists(auth_header)
        if valid_token(hot):
            return render_template('featured_playlists.html', hot=hot)

    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True, port=spotify.PORT)
