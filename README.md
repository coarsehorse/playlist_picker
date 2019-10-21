# Spotify playlist picker

```
python3 playlist_picker.py -h
```
Built in help:
```
usage: playlist_picker.py [-h] [-pl PLAYLIST_LINK | -pf PLAYLIST_FILE]
                          [-of OUTPUT_FILE] [-sf SECRET_FILE]

Parse tracks info from Spotify playlist

optional arguments:
  -h, --help            show this help message and exit
  -pl PLAYLIST_LINK, --playlist-link PLAYLIST_LINK
                        Playlist sharing link, e.g. https://open.spotify.com/u
                        ser/{user_id}/playlist/{playlist_id}?si=pRBErmskRAWY-u
                        2CAQ5t0w
  -pf PLAYLIST_FILE, --playlist-file PLAYLIST_FILE
                        Playlist in file(text file with the list of tracks).
                        Can be obtained from the Spotify app: select all
                        tracks from playlist(Ctrl + A), copy it(Ctrl + C) and
                        paste(Ctrl + V) in the text file
  -of OUTPUT_FILE, --output-file OUTPUT_FILE
                        Save tracks info to the specified file. Will be
                        rewrited if exists
  -sf SECRET_FILE, --secret-file SECRET_FILE
                        File with your credentials in JSON format: {
                        client_id: "xxx", client_secret: "yyy" }. It used for
                        authorization. Can be obtained here:
                        https://developer.spotify.com/dashboard/
```

Tracks in PLAYLIST_FILE format:
```
https://open.spotify.com/track/3FiDA9GX921AiW7iEpYS3K
```
SECRET_FILE format(JSON):
```
{
    "client_id": "xxx",
    "client_secret": "yyy"
}
```
For obtaining client_id and client_secret you must registrate new application for your account [here](https://developer.spotify.com/dashboard/)


Use cases:
```
python3 playlist_picker.py -pf playlist.txt -sf secret.json
```
```
python3 playlist_picker.py -sf secret.json -of output.txt -pl https://open.spotify.com/user/{user_id}/playlist/{playlist_id}?si=qQvI_Ii-SEabLb23j-vgRQ
```
