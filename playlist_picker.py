import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib import parse
import argparse
import base64

argparser = argparse.ArgumentParser(description="Parse tracks info from Spotify playlist")
group = argparser.add_mutually_exclusive_group()
group.add_argument("-pl", "--playlist-link", help="Playlist sharing link, e.g. https://open.spotify.com/user/{user_id}/playlist/{playlist_id}?si=pRBErmskRAWY-u2CAQ5t0w")
group.add_argument("-pf", "--playlist-file", help="Playlist in file(text file with the list of tracks). Can be obtained from the Spotify app: select all tracks from playlist(Ctrl + A), copy it(Ctrl + C) and paste(Ctrl + V) in the text file")
argparser.add_argument("-of", "--output-file", help="Save tracks info to the specified file. Will be rewrited if exists")
argparser.add_argument("-sf", "--secret-file", help="File with your credentials in JSON format: { \"client_id\": \"xxx\", \"client_secret\": \"yyy\" }. It used for authorization. Can be obtained here: https://developer.spotify.com/dashboard/")
args = argparser.parse_args()

if (args.secret_file == None):
    argparser.error("argument -sf/--secret-file: required for authorization")

if (args.playlist_link == None and args.playlist_file == None):
    argparser.error("No action specified! Please add one of the next arguments: -pl/-fp")


def refresh_access_token():
    secret_json = None

    with open(args.secret_file, encoding='utf-8') as s:
        secret_json = json.load(s)
    
    client_id = secret_json['client_id']
    client_secret = secret_json['client_secret']
    base64_enc = base64.b64encode((client_id + ":" + client_secret).encode('utf-8'))
    base64_str = base64_enc.decode('utf-8')
    
    data = parse.urlencode({'grant_type': 'client_credentials'}).encode('utf-8')
    request = Request("https://accounts.spotify.com/api/token", data = data)
    request.add_header('Authorization', 'Basic ' + base64_str)
    response = urlopen(request).read().decode('utf-8')
    json_resp = json.loads(response)
    new_token = json_resp['access_token']

    return new_token


access_token = refresh_access_token()


def get_track_info(track_id):
    request = Request("https://api.spotify.com/v1/tracks/" + track_id)
    request.add_header('Authorization', "Bearer " + access_token)
    response = urlopen(request).read().decode('utf-8')
    json_resp = json.loads(response)

    return json_resp['artists'][0]['name'] + " - " + json_resp['name']


def get_tracks_from_playlist_file(input_file):
    track_ids = []

    with open(input_file, encoding="utf-8") as inp_f:
        for line in inp_f:
            line = line.strip("\n ")
            track_id = line.split("/track/")[1]
            track_ids.append(track_id)

    playlist = []

    for id in track_ids:
        try:
            playlist.append(get_track_info(id))
        except HTTPError as err:
            if err.code == 401:
                refresh_access_token()
                playlist.append(get_track_info(id))
            else:
                raise err

    return playlist


def get_tracks_from_playlist_link(playlist_sharing_link, offset=0, limit=100):
    username = playlist_sharing_link.split("/user/")[1].split("/")[0]
    playlist_id = playlist_sharing_link.split("/playlist/")[1].split("?")[0]

    request = Request("https://api.spotify.com/v1/users/" + username 
        + "/playlists/" + playlist_id + "/tracks?" 
        + "offset=" + str(offset) + "&limit=" + str(limit))
    request.add_header('Authorization', "Bearer " + access_token)
    response = urlopen(request).read().decode('utf-8')
    json_resp = json.loads(response)

    tracks = [
        ' & '.join([artist['name'] for artist in item['track']['album']['artists']]) 
            + " - " + item['track']['name']
        for item in json_resp['items']
    ]

    if json_resp['next']:
        return tracks + get_tracks_from_playlist_link(
            playlist_sharing_link, offset + limit, limit)
    else:
        return tracks

# Start

result = None

if (args.playlist_link != None):
    result = get_tracks_from_playlist_link(args.playlist_link)
elif (args.playlist_file != None):
    result = get_tracks_from_playlist_file(args.playlist_file)

if (args.output_file != None):
    with open(args.output_file, encoding='utf-8', mode='w') as out_f:
        for track in result:
            out_f.write(track + "\n")
else:
    print()
    for track in result:
        print(track)

print("\nDone")
