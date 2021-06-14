import os
import sys
from utils import fprint, lj, rj, _PromtSession
from _api_call import SearchSongByName
from config import Config

# Initiate Singletone object
session = _PromtSession.instance()


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
        if len(user_input.split(" ")) > 1:
            render_search_screen(user_input)
        else:
            print("\n" * 20)
            fprint(
                "<invalid>Bad Syntax. Please provide title for search or check help section</invalid>"
            )
    # Set config command
    elif user_input.lower().startswith("set"):
        if user_input.find("=") >= 0:
            set_user_config(user_input)
        elif user_input.lower() == "set":
            print("\n" * 20)
            render_all_configs()
        else:
            print("\n" * 20)
            fprint("<invalid>Bad Syntax. Use set [key] [value] </invalid>")
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
    print(rj("{}: Check/Edit your config(s)".format(lj("config")), 4))


def render_search_screen(user_input: str) -> None:
    """Render search screen

    Args:
        user_input (str): search query
    """
    print("\n" * 20)
    search_title = user_input.split("search")[1].strip()
    videos_list = SearchSongByName(query=search_title)
    while True:
        print(f"Result for {search_title}")
        print("{}{}".format("Num".ljust(5), "Title"))
        for i, video in enumerate(videos_list):
            if i % 2 != 0:
                fprint(
                    "<odd_list>{}{}</odd_list>".format(str(i + 1).ljust(5), video[1])
                )
            else:
                fprint(
                    "<even_list>{}{}</even_list>".format(str(i + 1).ljust(5), video[1])
                )

        user_input = session.prompt(">").strip()
        # Check if user want to play song from above list
        if user_input.isdigit():
            user_input = int(user_input)
            if user_input > 0 and user_input - 1 <= len(videos_list):
                video_id = videos_list[user_input - 1][0]
                # TODO:- Add AUDI_ONLY SUPPORT FROM conf
                print("  {:<20}{:<20}".format("[<- | ->] seek", "[q] return"))
                print("  {:<20}{:<20}".format("[9 | 0] volume", "[space] pause/play"))
                param = " --no-video" if Config.AUDIO_ONLY else ""
                os.system(
                    r'"{}"{} https://www.youtube.com/watch?v={}'.format(
                        Config.MPV_PATH, param, video_id
                    )
                )
                break
            else:
                print("\n" * 20)
                fprint("<invalid>Invalid range provided</invalid>")
        # Check if user want to check others command
        else:
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
