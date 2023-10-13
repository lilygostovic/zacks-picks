import requests
from bs4 import BeautifulSoup

URL = "https://music.apple.com/library/playlist/p.kGoq3mrSR17A7De"
r = requests.get(URL)
print(r.content)

soup = BeautifulSoup(r.content, "html5lib")

# table = soup.find("div", class="songs-list-row")

f = open("soup.txt", "w")
f.write(soup.prettify())
f.close()

# get all library playlists
# https://api.music.apple.com/v1/me/library/playlists

# loop through all playlists until you find one with name Zack's Picks
#### save the playlist ID

# get the playlist info
# https://api.music.apple.com/v1/me/library/playlists/{id}

# Playlists.Relationships.PlaylistsTracksRelationship
#### has data property which is an array of MusicVideos and Songs
#### Song type: Songs.attributes = {name, artistName, albumName, ...}


# return list of type Song
# type Song = {
#     name: string;
#     artist: string;
#     albumName: string;
# }
