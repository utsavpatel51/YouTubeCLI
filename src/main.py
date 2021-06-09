from screens import render_welcome_screen
from config import Config


def main() -> None:
    # load config.json into class variable
    Config.load()

    render_welcome_screen()


if __name__ == "__main__":
    main()
