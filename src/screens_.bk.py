import os
import sys
from prompt_toolkit import PromptSession, prompt

from utils import fprint, lj, rj


def render_logo():
    logo = r"""
    __  __           ______      __            ________    ____
    \ \/ /___  __  _/_  __/_  __/ /_  ___     / ____/ /   /  _/
     \  / __ \/ / / // / / / / / __ \/ _ \   / /   / /    / /
     / / /_/ / /_/ // / / /_/ / /_/ /  __/  / /___/ /____/ /
    /_/\____/\__,_//_/  \__,_/_.___/\___/   \____/_____/___/"""
    print(logo)


def check_user_input(user_input):
    if user_input.lower().startswith("help"):
        render_help_screen()
        show_only_once = False
    elif user_input.lower().startswith("search"):
        if len(user_input.split(" ")) > 1:
            show_only_once = render_search_screen(user_input)
        else:
            fprint(
                "<invalid>Bad Syntax. Please provide title for search or check help section</invalid>"
            )
            show_only_once = False
    else:
        show_only_once = True
    return show_only_once


def render_welcome_screen():
    show_only_once = True
    session = PromptSession()
    while True:
        try:
            if show_only_once:
                print("\n" * 20)
                render_logo()
                print("\n" * 2)
                fprint(
                    "<title>{}</title>".format(
                        rj("Enter help to see all available options")
                    )
                )
            user_input = session.prompt(">").strip()
            show_only_once = check_user_input(user_input)
        except KeyboardInterrupt:
            sys.exit(0)


def render_help_screen():
    print("\n" * 20)
    fprint("<sub_title>{}</sub_title>".format(rj("Available options")))
    print()
    print(rj("{}: Search for song".format(lj("search")), 4))
    print(rj("{}: Check/Edit your config(s)".format(lj("config")), 4))


def render_search_screen(user_input):
    print("\n" * 20)
    search_title = user_input.split("search")[1]
    print("1. In the end {}".format(user_input))
    print("2. In the end")
    print("3. In the end")
    print("4. In the end")
    user_input = prompt(">").strip()
    if user_input in ["1", "2", "3"]:
        os.system(
            r'"C:\Users\Utsav Patel\Downloads\Programs\bootstrapper\mpv" --no-video https://www.youtube.com/watch?v=poD0gD7hi5s'
        )
        show_only_once = False
    else:
        show_only_once = check_user_input(user_input)

    return show_only_once
