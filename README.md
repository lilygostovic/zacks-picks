# Zacks Picks: From Apple Music to Spotify

A friend who uses Apple Music updates a playlist weekly with his favourite songs from the week. As a Spotify user, I can not access his playlist to get his recommendations. The goal of this project is to create a script that scrapes his playlist weekly and updates a playlist on my Spotify with his new picks of the week. 

The Apple Music API requires a large payment to gain access to so I will instead scrape the apple music website html to get all the songs on the playlist. I will then use `spotipy`, a "lightweight Python library for the Spotify Web API" to update my Spotify playlist. This script will be called from a file which uses a crontab bash file to run it every Sunday evening at 11pm. 
