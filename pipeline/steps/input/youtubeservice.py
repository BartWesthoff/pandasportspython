import os

from pytube import YouTube

from pipeline.steps.input.input import Input


class YoutubeService(Input):
    """" Class for the Youtube service step"""

    def process(self):
        """ abstract method for using the data of the step """
        videos = ['https://www.youtube.com/shorts/bWnT9esxOU0']

        for url in videos:
            self.download(url=url)


    def download(self, url):
        yt = YouTube(url)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
            os.sep.join(["data", "production"]))
