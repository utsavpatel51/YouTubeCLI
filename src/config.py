import os
import sys
from pathlib import Path
import json

conf_file_path = os.path.join(Path(__file__).parent, "const", "config.json")


class Config:
    API_KEY = ""
    MPV_PATH = ""
    AUDIO_ONLY = ""

    def __init__(self) -> None:
        raise RuntimeError("Use classmethod insted of creating instance.")

    @classmethod
    def get_all_key(cls) -> dict:
        return {key: val for key, val in vars(cls).items() if key.isupper()}

    @classmethod
    def check_key(cls, key) -> bool:
        return True if key in vars(cls) else False

    @classmethod
    def set(cls, key: str, val: str) -> None:
        setattr(cls, key, val)
        cls.save()

    @classmethod
    def save(cls) -> None:
        config_dict = {key: val for key, val in vars(cls).items() if key.isupper()}
        with open(conf_file_path, "w+") as fp:
            json.dump(config_dict, fp, indent=4)
        cls.load()

    @classmethod
    def load(cls) -> None:
        if os.path.exists(conf_file_path):
            with open(conf_file_path) as fp:
                saved_config = json.load(fp)
            for key, val in saved_config.items():
                setattr(cls, key, val)
