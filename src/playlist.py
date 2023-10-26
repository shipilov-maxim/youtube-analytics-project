from datetime import timedelta
from src.video import Video, MixApi
import isodate


class PlayList(MixApi):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

        api = self.get_service()

        self.title = api.playlists().list(part='snippet',
                                          id=self.playlist_id).execute()['items'][0]['snippet']['localized']['title']

        self.playlist = api.playlistItems().list(playlistId=self.playlist_id,
                                                 part='snippet,contentDetails',
                                                 maxResults=50,
                                                 ).execute()

        self.video_ids = self.playlist['items']
        self.videos = self.get_videos()

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.videos:
            duration = isodate.parse_duration(video.duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        return f"https://youtu.be/{(max(self.videos, key=lambda video: video.like_count)).video_id}"

    def get_videos(self) -> list[Video]:
        return [Video(video["contentDetails"]["videoId"]) for video in self.video_ids]
