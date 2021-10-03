# YouTubeCLI

## How to setup MPV and youtube-dl?

 - Download mpv for windows rom [here](https://sourceforge.net/projects/mpv-player-windows/).
 -- Extract the downloaded zip file and run the batch file.
 -- provide 'y' to install mpv and do no install youtube-dl from script.
 -  Download youtube-dl from [here](http://ytdl-org.github.io/youtube-dl/download.html).

## Commands

# 1. Get list of command
Use `help` command to get the list and help text for each command currently supported

# 2. Set necessary config values
Use `set` command to see the current configuration. To change particular configuration you can use set [key]=[value].
For example set API_KEY=abc-sample-api-key.

Note:- For MPV_PATH provide the path for mpv instead of mpv.exe

# 1. Search for songs
Use `search=[value]` to search the song.
After hitting above command you will see the list of available youtube video matching your search text. Use <index> to play particular video and to download any video use download=<index>. If you choose to play video mpv player will play your video based on your configuration.