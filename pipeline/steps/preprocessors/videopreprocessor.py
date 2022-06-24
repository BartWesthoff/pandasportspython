import os
import shutil
from random import *

import cv2
import moviepy.editor as mpy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from pipeline.steps.step import Step
from pipeline.utils.deprecated import deprecated
from pipeline.utils.utils import Utils

"""
PreProcessor class
used to preprocess video material
"""


class VideoPreProcessor(Step):
    """" class for video preprocessing """

    def process(self, data: list[str]) -> list[str]:
        """" processes given data"""
        return self._preprocessVideo(data)
        # return data

    def _preprocessVideo(self, data: list[str]) -> list[str]:
        """" preprocesses video """
        proccessed_data = []
        path = os.sep.join(["data", "negative_squat"])

        path2 = os.sep.join(["data", "positive_squat"])

        for root, directories, files in os.walk(path, topdown=False):
            for name in files:
                source = os.path.join(root, name)
                name = self.cropVideo(source)
                if self.settings["color"]:
                    name = self.grayvideo(name)
                proccessed_data.append(name)

        for root, directories, files in os.walk(path2, topdown=False):
            for name in files:
                name = self.cropVideo(os.path.join(root, name))
                if self.settings["color"]:
                    name = self.grayvideo(name)
                proccessed_data.append(name)

        return proccessed_data

    def _getnewname(self, fullsource: str, appendix: str) -> str:
        name = fullsource.split(os.sep)[-1].split(".")[0]
        source = os.sep.join(fullsource.split(os.sep)[:-1])
        new_name = f"{source}{os.sep}{name}_{appendix}.mp4"
        return new_name

    def removesound(self, source: str) -> str:
        """" Removes sound from video """
        new_name = self._getnewname(source, "NS")
        if os.path.exists(new_name):
            return new_name

        videoclip = mpy.VideoFileClip(source)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(new_name)
        videoclip.reader.close()
        videoclip.audio.reader.close_proc()
        return new_name

    @deprecated
    def capFPS(self, source: str, output: str, fps: int) -> None:
        """" Cap FPS of video """
        video = mpy.VideoFileClip(source)
        video.write_videofile(output, fps=fps)
        video.close()

    def cropVideo(self, source: str):
        """" changed width and height of video """
        new_name = self._getnewname(source, "NB")
        # check if file exists
        if "_NB" in source:
            return new_name


        cap = cv2.VideoCapture(source)
        fps = cap.get(cv2.CAP_PROP_FPS)

        # get video frames
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        rval, frame = cap.read()
        if frame is not None:
            im = frame.copy()

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            x, y, w, h = cv2.boundingRect(cnt)
            print(x, y, w, h)

            # no contour or too small
            if w == width or h == height or x == 0 or y == 0 or w < 20 or h < 20:
                return new_name
            print("cropping video")
            # output
            shutil.copyfile(source, new_name)
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(new_name, codec, fps, (w, h))

            # Now we start
            cnt = 0
            while cap.isOpened():
                ret, frame1 = cap.read()
                cnt += 1  # Counting frames

                # Avoid problems when video finish
                if ret:
                    cropped_frame = frame1[y:y + h, x:x + w]
                    out.write(cropped_frame)
                    # Percentage
                    xx = cnt * 100 / frames
                    print(int(xx), '%')
                    if self.settings['testing']:
                        cv2.imshow('frame', frame1)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                else:
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
            return new_name

    def playVideo(self, source: str) -> None:
        """" plays video """
        cap = cv2.VideoCapture(source)

        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error opening video  file")

        # Read until video is completed
        while cap.isOpened():

            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:

                # Display the resulting frame
                cv2.imshow("Frame", frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    break
                # Press S on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord("s"):
                    print("Saving" + str(randint(0, 100)))

            # Break the loop
            else:
                break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

    # alleen voor vergelijken gebruiken
    def grayvideo(self, source: str) -> str:
        """" Convert video to black/white """
        new_name = self._getnewname(source, "BW")
        if os.path.exists(new_name):
            return new_name
        output = Utils().changeFileName(source, new_name)
        video = cv2.VideoCapture(source)
        fps = video.get(cv2.CAP_PROP_FPS)
        # We need to check if camera
        # is opened previously or not
        if not video.isOpened():
            print("Error reading video file")

        # We need to set resolutions.
        # so, convert them from float to integer.
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        x, y, w, h = 0, 0, frame_width, frame_height

        # Set up codec and output video settings
        # codec = cv2.VideoWriter_fourcc("X", "V", "I", "D")
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        size = (frame_width, frame_height)
        result = cv2.VideoWriter(f"{output}.mp4",
                                 codec,
                                 fps, size, isColor=False)

        while video.isOpened():
            ret, frame = video.read()
            if ret:
                cv2.imshow("Live", frame)
                gray = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
                result.write(gray)
                if cv2.waitKey(1) & 0xFF == ord("s"):
                    break
            # Break the loop
            else:
                break

        video.release()
        result.release()
        cv2.destroyAllWindows()

        print("The video was successfully saved")
        return new_name

    # def imageToVideo(self):
    #     image_folder = "images"
    #     video_name = "video.avi"
    #
    #     images = [i.name for i in sorted(Path(image_folder).iterdir(), key=os.path.getmtime)]
    #
    #     frame = cv2.imread(os.path.join(image_folder, images[0]))
    #     height, width, layers = frame.shape
    #
    #     video = cv2.VideoWriter(video_name, 0, 30, (width, height))
    #
    #     for image in images:
    #         video.write(cv2.imread(os.path.join(image_folder, image)))
    #
    #     cv2.destroyAllWindows()
    #     video.release()

    @deprecated
    def trimvideo(self, name: str, start_time: float, end_time: float):
        """" Trim video """
        name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + name
        ffmpeg_extract_subclip(f"{name}.mp4", start_time, end_time, targetname=f"{name}_short.mp4")

    # deprecated waarschijnlijk
    @deprecated
    def trimvideo2(self, name: str):
        """" 2nd Trim video method """
        vcodec = "libx264"
        name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + name
        videoquality = "30"

        # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        compression = "slow"

        title = name
        loadtitle = title + ".mp4"
        savetitle = title

        # modify these start and end times for your subclips
        cuts = [("00:00:00.000", "00:00:05.530")]

        # load file
        video = mpy.VideoFileClip(loadtitle)

        # cut file
        clips = []
        clip = None
        for index, cut in enumerate(cuts):
            clip = video.subclip(cut[0], cut[1])
            if video.rotation == 90:
                clip = video.resize(clip.size[::-1])
                clip.rotation = 0
            clip.write_videofile(f"{savetitle}-{index}.mp4", threads=4, fps=30,
                                 codec=vcodec,
                                 preset=compression,
                                 ffmpeg_params=["-crf", videoquality])
        print(type(clip))

        # final_clip = mpy.CompositeVideoClip([final_clip, txt])
        #
        # # save file
        # final_clip.write_videofile(savetitle, threads=4, fps=24,
        #                            codec=vcodec,
        #                            preset=compression,
        #                            ffmpeg_params=["-crf", videoquality])

        video.close()

    def runBash(self, command: str) -> None:
        """ Run bash command """
        os.system(command)

    def crop(self, start: float, end: float, source: str, output: str) -> None:
        """ crop video by given start and end time """
        name = os.sep.join([Utils().datafolder, source])
        output = os.sep.join([Utils().datafolder, output])

        str = f"ffmpeg -i {name}.mp4 -ss  {start} -to {end} -c copy {output}.mp4"
        self.runBash(str)
