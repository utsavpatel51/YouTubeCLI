import os
import sys
from playlist import Playlist
from utils import fprint, lj, rj, PromtSession, log_command_use
from _api_call import SearchSongByName
from config import Config
import random


# Initiate Singletone object
session = PromtSession.instance()

def render_logo() -> None:
    """render logo of application"""
    print("\n" * 20)
    logo = r"""
    __  __           ______      __            ________    ____
    \ \/ /___  __  _/_  __/_  __/ /_  ___     / ____/ /   /  _/
     \  / __ \/ / / // / / / / / __ \/ _ \   / /   / /    / /
     / / /_/ / /_/ // / / /_/ / /_/ /  __/  / /___/ /____/ /
    /_/\____/\__,_//_/  \__,_/_.___/\___/   \____/_____/___/"""
    print(logo)
    print("\n" * 2)
    fprint("<title>{}</title>".format(rj("Enter help to see all available options")))


@log_command_use
def check_user_input(user_input: str) -> None:
    """
    Common method to check user input from prompt
    Args:
        user_input (str): user's input
    """

    # Help command
    if user_input.lower().startswith("help"):
        render_help_screen()

    # Search command
    elif user_input.lower().startswith("search"):
        if len(user_input.split("=")) > 1:
            render_search_screen(user_input)
        else:
            print("\n" * 20)
            fprint("<invalid>Bad Syntax. Use search=[value]</invalid>")

    # Set config command
    elif user_input.lower().startswith("set"):
        if user_input.find("=") >= 0:
            set_user_config(user_input)
        elif user_input.lower() == "set":
            print("\n" * 20)
            render_all_configs()
        else:
            print("\n" * 20)
            fprint("<invalid>Bad Syntax. Use set [key]=[value] </invalid>")

    # Playlist command
    elif user_input.lower().startswith("playlist"):
        command = user_input.split(" ")[-1]
        if user_input.find("=") >= 0 and command in ["create", "play", "download"]:
            render_playlist_screen(user_input, command)
        else:
            print("\n" * 20)
            fprint("<invalid>Bad Syntax. Use playlist=[name] create/play/download </invalid>")

    # Render default screens
    else:
        render_logo()


def render_welcome_screen() -> None:
    """Render welcome screen of application"""
    render_logo()

    while True:
        try:
            user_input = session.prompt(">").strip()
            check_user_input(user_input)
        except KeyboardInterrupt:
            sys.exit(0)


def render_help_screen() -> None:
    """Render help screen"""
    print("\n" * 20)
    fprint("<sub_title>{}</sub_title>".format(rj("Available options")))
    print()
    print(rj("{}: Search for song".format(lj("search")), 4))
    print(rj("{}: Check/Edit your config(s)".format(lj("set")), 4))
    print(rj("{}: Manage your playlist".format(lj("playlist")), 4))

def helper_to_render_list(items_list: list, field=None):
    for i, item in enumerate(items_list):
            item = getattr(item, field) if field else item
            if i % 2 != 0:
                fprint(
                    "<odd_list>{}{}</odd_list>".format(str(i + 1).ljust(5), item)
                )
            else:
                fprint(
                    "<even_list>{}{}</even_list>".format(
                        str(i + 1).ljust(5), item
                    )
                )

def helper_to_play_video(video_id):
    print("  {:<20}{:<20}".format("[<- | ->] seek", "[q] return"))
    print("  {:<20}{:<20}".format("[9 | 0] volume", "[space] pause/play"))
    param = " --no-video" if Config.AUDIO_ONLY.lower() == "true" else ""
    os.system(
        r'"{}"{} https://www.youtube.com/watch?v={}'.format(
            Config.MPV_PATH, param, video_id
        )
    )

def render_search_screen(user_input: str) -> None:
    """Render search screen

    Args:
        user_input (str): search query
    """
    print("\n" * 20)
    search_title = user_input.split("=")[-1].strip()
    videos_list = SearchSongByName(query=search_title)
    while True:
        print(f"Result for {search_title}\n")
        print("{}{}".format("Num".ljust(5), "Title"))

        helper_to_render_list(videos_list, field="Title")

        print("\nEnter <index> to play. download=<index> to download the song. add_to_playlist=<index> to add video to playlist. \n")

        user_input = session.prompt(">").strip()
        # Check if user want to play song from above list
        if user_input.isdigit():
            index = int(user_input)
            if index > 0 and index <= len(videos_list):
                helper_to_play_video(videos_list[index - 1].ID)
            else:
                print("\n" * 20)
                fprint("<invalid>Please provide valid index</invalid>")
        elif user_input.startswith("download"):
            index = user_input.split("=")[-1]
            if index.isdigit():
                index = int(index)
                if index > 0 and index <= len(videos_list):
                    output = os.system(
                        "youtube-dl https://www.youtube.com/watch?v={} -F".format(
                            videos_list[index - 1].ID
                        )
                    )
                    print(output)
                    format_code = input("Provide format code no:- ")
                    if not Config.DOWNLOAD_PATH:
                        fprint(
                            "<invalid>Download path is not set. Downloading on working directory</invalid>"
                        )
                    os.system(
                        'youtube-dl https://www.youtube.com/watch?v={} -f {} -o "{}"'.format(
                            videos_list[index - 1].ID,
                            format_code,
                            Config.DOWNLOAD_PATH + "/%(title)s.%(ext)s",
                        )
                    )
                else:
                    print("\n" * 20)
                    fprint("<invalid>Please provide valid index</invalid>")
        elif user_input.startswith("add_to_playlist"):
            index = user_input.split("=")[-1]
            if index.isdigit():
                index = int(index)
                if index > 0 and index - 1 <= len(videos_list):
                    render_playlist_screen(user_input, command="add", video=videos_list[index - 1])
            else:
                print("\n" * 20)
                fprint("<invalid>Please provide valid index</invalid>")
        # Check if user want to check others command
        else:
            break
    check_user_input(user_input)


def set_user_config(user_input: str) -> None:
    """Set config value of application

    Args:
        user_input (str): User input string
    """
    command, value = map(str.strip, user_input.split("set")[-1].split("="))
    # If config key match set
    if Config.check_key(command):
        Config.set(command, value)
    else:
        fprint(
            "<invalid>Bad key. Check set commad to know all availabe configrations.</invalid>"
        )


def render_all_configs() -> None:
    # Render all config to screen
    fprint("<title> {:<20}: {:<20}</title>".format("Key", "Value"))
    for key, val in Config.get_all_key().items():
        if not key.startswith("__"):
            fprint("<subtitle> {:<20}: {:<20}</subtitle>".format(key, val))


def render_playlist_screen(user_input, command, **kwargs) -> None:
    print("\n" * 20)
    if command == "create":
        playlist_name = user_input.split('=')[-1].split(" ")[0]

        if Playlist.do_playlist_exists(playlist_name):
            fprint("<invalid> Playlist already exists!! Try different name. </invalid>")
        else:
            _ = Playlist(playlist_name)
            fprint("<success> Playlist created successfully </success>")

    elif command == "play":
        playlist_name = user_input.split('=')[-1].split(" ")[0]

        if not Playlist.do_playlist_exists(playlist_name):
            fprint("<invalid> Playlist not exists!! Try different name. </invalid>")
        else:
            playlist_obj = Playlist(playlist_name)
            for video in playlist_obj.playlist:
                fprint("<subtitle>Currently playing {}</subtitle>".format(video.Title))
                helper_to_play_video(video.ID)

    elif command == "add":
        all_playlist = render_playlist_screen(user_input, command="list")
        helper_to_render_list(all_playlist)
        print("\nEnter <index> to add video into particular playlist\n")

        user_input = session.prompt(">").strip()
        if user_input.isdigit():
            index = int(user_input)
            if index > 0 and index <= len(all_playlist):
                playlist_name = all_playlist[index - 1]
                playlist_obj = Playlist(playlist_name)
                playlist_obj.playlist = kwargs['video']
            else:
                print("\n" * 20)
                fprint("<invalid>Please provide valid index</invalid>")

    elif command == "list":
        return Playlist.get_all_playlist()