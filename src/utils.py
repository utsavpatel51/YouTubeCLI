from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.styles import Style
from collections import namedtuple
import logging

logger = logging.getLogger('AppLog')
style = Style.from_dict(
    {
        "title": "#f2ed46",
        "sub_title": "#ffff00",
        "invalid": "#ff0000",
        "odd_list": "#2978b5",
        "even_list": "#ff8303",
        "success": "#00ff00"
    }
)

Video = namedtuple("Video", ["ID", "Title"])

def fprint(text: str):
    """Print Formated String

    Args:
        text (str): [description]
    """
    print_formatted_text(HTML(text), style=style)


def rj(text: str, margin: int = 2):
    return text.rjust(len(text) + margin)


def lj(text: str, margin: int = 2):
    return text.ljust(len(text) + margin)


class PromtSession:
    """
    Singleton Object for prompt session
    """

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = PromptSession()
        return cls.__instance

    def __init__(self) -> None:
        raise RuntimeError("Call instance() instead")


def log_command_use(func):
    def wrapTheFunction(user_input, *args, **kwargs):
        logger.debug("Use command:- {}".format(user_input))
        func(user_input, *args, **kwargs)
    return wrapTheFunction