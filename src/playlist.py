import json
import os
from pathlib import Path
from utils import Video

class Playlist:
    """Playlist class.
    Playlist(Video(ID, Title), Video(ID, Title))
    """

    _loaded = {}
    root_key = 'playlists'
    __store_playlist = list()
    PLAYLIST_PATH = Path(__file__).parent.joinpath('const', 'playlist.cache')

    def __new__(cls, name: str):
        if cls._loaded.get(name):
            # Returning Playlist object from local cache
            return cls._loaded[name]

        # Create new Playlist object
        playlist_obj = super().__new__(cls)
        cls._loaded[name] = playlist_obj
        playlist_obj._init_playlist_list_from_file(name)
        return playlist_obj

    def _init_playlist_list_from_file(self, name):
        """
        Create playlist cache file if not exists
        else create a new one.
        """
        self.name = name
        self.__store_playlist = self.__create_and_get_playlist_file()

    @classmethod
    def get_all_playlist(cls) -> list:
        # Return all playlist list
        if os.path.exists(cls.PLAYLIST_PATH):
            data = cls.__read_file()
            return list(data[cls.root_key].keys())
        return list()

    @classmethod
    def do_playlist_exists(cls, name):
        if os.path.exists(cls.PLAYLIST_PATH):
            data = cls.__read_file()
            if name in data[cls.root_key].keys():
                return True
        return False

    @property
    def playlist(self):
        # Load individual video as Video namedtuple
        # Playlist(Video(ID, Title), Video(ID, Title))
        return [Video(video_id, video_title) for video_id, video_title in self.__store_playlist]

    @playlist.setter
    def playlist(self, var):
        # append video to existing list of playlist
        self.__store_playlist.append(var)
        self.__save_to_playlist_file()


    def __save_to_playlist_file(self):
        """
        Store current list of playlist to file
        """
        data = self.__read_file()
        data[self.root_key][self.name] = self.__store_playlist
        self.__write_file(data)

    def __create_and_get_playlist_file(self):
        if not os.path.isfile(self.PLAYLIST_PATH):
            # File not exists create a new one with raw data
            data = {}
            data[self.root_key] = dict()
            data[self.root_key][self.name] = list()
            self.__write_file(data)
        else:
            data = self.__read_file()
            # File exists but playlist name not
            if not self.name in data[self.root_key].keys():
                data[self.root_key][self.name] = list()
                self.__write_file(data)

        return data[self.root_key][self.name]

    @classmethod
    def __read_file(cls):
        with open(cls.PLAYLIST_PATH, 'r') as fp:
            data = json.load(fp)
        return data

    @classmethod
    def __write_file(cls, data):
        with open(cls.PLAYLIST_PATH, 'w') as fp:
            json.dump(data, fp)