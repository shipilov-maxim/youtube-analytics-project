import json
import os
from pathlib import Path
from googleapiclient.discovery import build

JSON_PATH = Path(__file__).resolve().parent / "channels.json"
api_key: str = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

        api = self.get_service()

        channel: dict = api.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel['items'][0]['id']}"
        self.subscriberCount = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Rласс-метод, возвращающий объект для работы с YouTube API"""
        return build("youtube", "v3", developerKey=api_key)

    def to_json(self, file):
        """Загружает все публичные атрибуты объекта и свойства property в объект json"""
        with open(file, "a") as json_file:
            return json.dump(self.__dict__, json_file, indent=2, ensure_ascii=False)

