# flexget.rutorrent
flexget  output plugin for rutorrent

# Installation
put rutorrent.py into your plugin folder

# Configuration

rutorrent:
 url: webui url without end slash "/" (required)
 path: path for download of torrent content, can be used "set" plugin (optional)
 user: webui user (optional)
 pass: webui pass (optional)
 autostart: should the torrent start automatically (optional default : true)
