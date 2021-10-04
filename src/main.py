from screens import render_welcome_screen
from config import Config
from logging_ import setup_log

def main() -> None:
    #Setup Log
    _ = setup_log()
    # load config.json into class variable
    Config.load()
    render_welcome_screen()


if __name__ == "__main__":
    main()
