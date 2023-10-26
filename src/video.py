from googleapiclient.discovery import build
import os


API_KEY: str = os.getenv('API_KEY')


class MixApi:
    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return build("youtube", "v3", developerKey=API_KEY)


class Video(MixApi):
    def __init__(self, video_id):
        self.video_id = video_id
        if self.get_resource():
            self.title: str = self.get_resource()['snippet']['title']
            self.channel_title: str = self.get_resource()['snippet']['channelTitle']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}&ab_channel={self.channel_title}"
            self.view_count: int = self.get_resource()['statistics']['viewCount']
            self.like_count: int = self.get_resource()['statistics']['likeCount']
            self.duration: int = self.get_resource()['contentDetails']['duration']
        else:
            self.title = None
            self.channel_title = None
            self.url = None
            self.view_count = None
            self.like_count = None
            self.duration = None

    def get_resource(self):
        try:
            api = self.get_service()
            response: dict = api.videos().list(part="snippet,contentDetails,statistics",
                                               id=self.video_id).execute()["items"][0]
        except (KeyError, IndexError):
            return
        else:
            return response

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, channel_id, playlist_id):
        super().__init__(channel_id)
        self.playlist_id = playlist_id


