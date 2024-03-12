# Data 2 Spotify
Pulls data from PostNords API for showing which day post is delivered and updates a Spotify playlist with image of the data. Scheduled to run once at night every day.

Project is a valid [Home Assistant add-on](https://www.home-assistant.io/addons/) and can be installed by copying code to *addons/* in your Home Assistant server and installing it from the interface. This helps with having the service running continuously.

![Screenshot of Spotify](https://raw.githubusercontent.com/gotling/Data2Spotify/main/screenshot.jpg)

# Why this project exists?
When driving or coming home I sometimes want to have some basic data available to know if I should check the mailbox or connect the car for charging. Spotify is easily accessable from the cars display so it seemed like a good place to put data.

# Getting started
First time running must be interactive to authenticate user with Spotify. A web browser will open where you login.
To run again non interactive on a server, copy .cache* files from this folder to the server.

# Settings
Store settings in a file called *.env* or use environment variables.

    SPOTIPY_CLIENT_ID=''
    SPOTIPY_CLIENT_SECRET=''
    SPOTIPY_REDIRECT_URI='http://127.0.0.1:9000'
    SPOTIPY_USER=''
    PLAYLIST_ID=''
    POSTAL_CODE=''

Get client id and client secret by creating a application on the Spotify developer dashboard. Set redirect uri to same value as here.

https://developer.spotify.com/dashboard

Manually create a playlist or use the commented out code in the source. Store the playlist id as it can be seen in the url in a browser.

Postal code that you want to find deliver day for, only numbers, no dash or whitespace.

# Acknowledgement
## Libraries
### spotipy
https://spotipy.readthedocs.io/

### python-dotenv
https://pypi.org/project/python-dotenv/

### requests
https://pypi.org/project/requests/

### dateparser
https://pypi.org/project/dateparser/

### pillow
https://pypi.org/project/pillow/

### schedule
https://schedule.readthedocs.io/

## Media
### Background
https://www.pexels.com/photo/silhouette-of-a-person-carrying-a-surfboard-standing-on-shore-5019646/

### Postbox icon
https://creazilla.com/sv/nodes/49884-postlada-clipart

### Font
https://www.dafont.com/lt-saeada.font?text=M%E5ndag+30