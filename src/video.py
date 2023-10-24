from googleapiclient.discovery import build
import os

api_key: str = os.getenv('API_KEY')


class Video:
    def __init__(self, video_id):
        self.video_id = video_id

        api = self.get_service()

        video_response: dict = api.videos().list(id=self.video_id,
                                                 part='snippet,contentDetails,statistics').execute()['items'][0]
        self.video_title: str = video_response['snippet']['title']
        self.channel_title: str = video_response['snippet']['channelTitle']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}&ab_channel={self.channel_title}"
        self.view_count: int = video_response['statistics']['viewCount']
        self.like_count: int = video_response['statistics']['likeCount']
        self.duration: int = video_response['contentDetails']['duration']

    def __str__(self):
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return build("youtube", "v3", developerKey=api_key)


class PLVideo(Video):
    def __init__(self, channel_id, playlist_id):
        super().__init__(channel_id)
        self.playlist_id = playlist_id
