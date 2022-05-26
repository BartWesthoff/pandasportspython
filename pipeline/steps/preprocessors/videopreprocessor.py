import os

import cv2
import moviepy.editor as mpy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from classes.cloudfile import CloudFile
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils

"""
PreProcessor class
used to preprocess video material
"""


class VideoPreProcessor(Step):

    def process(self, data: list[CloudFile]):
        return self._preprocessVideo(data)

    def _preprocessVideo(self, data: list[CloudFile]):
        # for i in data:
        #     print(i.name)
        # # idee is dat we deze video namen gebruiken om van gedownloaden data goede data te maken
        # # wordt bijvoorbeeld gedownload in een download mapje,
        # # en daar sorteren we de video's en bewerken we ze
        # # bewerkte data komt dan is positief of negatief
        # # kan ook in 1 mapje production
        #
        # for name in ["positive", "negative"]:
        #     folder = Utils().root_dir + os.sep + "data" + os.sep + f"{name}_squat" + os.sep
        #     for index, file_name in enumerate(os.listdir(folder)):
        #         # Construct old file name
        #         source = folder + file_name
        #
        #         # Adding the count to the new file name and extension
        #         # TODO bespreken: hoe gaan we 'ready' data neerzetten?
        #         # met production data folder of gewoon overwritten
        #         destination = folder + f"{name}_squat{index // 2}.mp4"
        #
        #         # destination = folder.replace(f'{name}_squat', "production") + f"{name}_squat{index}.mp4"
        #
        #         # Video bestaat al zonder geluid
        #         if not os.path.exists(destination):
        #             os.rename(source, destination)
        #             self.removesound(str(destination))
        for item in data:
            name = item.name
            name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + name
            name = self.cropVideo(name, "edited footage")
            # self.grayvideo(name, name)
        return data

    def removesound(self, source: str, output: str):
        """" Remove sound from video """
        videoclip = mpy.VideoFileClip(source)
        new_clip = videoclip.without_audio()
        name = source.split(os.sep)[-1].split(".")[0]
        codec = name.split(os.sep)[-1].split(".")[-1]
        new_clip.write_videofile(f"{output}_edit.{codec}")

        videoclip.reader.close()
        videoclip.audio.reader.close_proc()

    def capFPS(self, source: str, output: str, fps: int):
        """" Cap FPS of video """
        video = mpy.VideoFileClip(source)
        video.write_videofile(output, fps=fps)
        video.close()

    def cropVideo(self, source: str, newname: str):
        """" changed width and height of video """
        output = Utils().changeFileName(source, newname)
        cap = cv2.VideoCapture(source)
        fps = cap.get(cv2.CAP_PROP_FPS)

        # get video frames
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        rval, frame = cap.read()
        if frame is not None:
            im = frame.copy()

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Convert image to grayscale
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # make binary image
            im = cv2.threshold(im, 5, 255, cv2.THRESH_BINARY)[1]

            # draw black border around image to better detect blobs:
            cv2.rectangle(im, (0, 0), (width, height), 0, thickness=width // 25)

            # Invert the black and white colors
            im = ~im

            # Find contours and sort them by width
            cnts, _ = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            list(cnts).sort(key=lambda x: cv2.boundingRect(x)[2], reverse=True)

            # Change the type and channels of image copies
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

            x, y, w, h = cv2.boundingRect(cnts[1])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 0, 255), 10)
            cv2.rectangle(im, (x, y), (x + w, y + h), (128, 255, 0), 10)

            # output
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(f'{output}.mp4', codec, fps, (w, h))

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
                    cv2.imshow('frame', frame1)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
            return f'{output}.mp4'

    # alleen voor vergelijken gebruiken
    def grayvideo(self, source: str, newname: str):
        """" Convert video to black/white """
        output = Utils().changeFileName(source, newname)
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
        # codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        size = (frame_width, frame_height)
        result = cv2.VideoWriter(f'{output}.mp4',
                                 codec,
                                 fps, size, isColor=False)

        while video.isOpened():
            ret, frame = video.read()
            if ret:
                cv2.imshow("Live", frame)
                gray = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
                result.write(gray)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            # Break the loop
            else:
                break

        video.release()
        result.release()
        cv2.destroyAllWindows()

        print("The video was successfully saved")

    # def imageToVideo(self):
    #     image_folder = 'images'
    #     video_name = 'video.avi'
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

    # deprecated waarschijnlijk
    def trimvideo(self, name: str, start_time: float, end_time: float):
        """" Trim video """
        name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + name
        ffmpeg_extract_subclip(f"{name}.mp4", start_time, end_time, targetname=f"{name}_short.mp4")

    # deprecated waarschijnlijk
    def trimvideo2(self, name: str):
        """" 2nd Trim video method """
        vcodec = "libx264"
        name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + name
        videoquality = "30"

        # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        compression = "slow"

        title = name
        loadtitle = title + '.mp4'
        savetitle = title

        # modify these start and end times for your subclips
        cuts = [('00:00:02.949', '00:00:04.152'),
                ('00:00:06.328', '00:00:13.077')]

        # load file
        video = mpy.VideoFileClip(loadtitle)

        # cut file
        clips = []
        clip = None
        for index, cut in enumerate(cuts):
            clip = video.subclip(cut[0], cut[1])
            clip.write_videofile(f"{savetitle}-{index}.mp4", threads=4, fps=30,
                                 codec=vcodec,
                                 preset=compression,
                                 ffmpeg_params=["-crf", videoquality])
        print(type(clip))

        #     clips.append(clip)
        #
        # final_clip = mpy.concatenate_videoclips(clips)
        #
        #
        # final_clip = mpy.CompositeVideoClip([final_clip, txt])
        #
        # # save file

        #
        # video.close()

    # deprecated waarschijnlijk
    def runBash(self, command: str):
        """ Run bash command """
        os.system(command)

    # deprecated waarschijnlijk
    def crop(self, start, end, source: str, output: str):
        """ shortens video """
        name = Utils().root_dir + os.sep + "data" + os.sep + "production" + os.sep + source
        str = "ffmpeg -i " + f"{name}.mp4" + " -ss  " + start + " -to " + end + " -c copy " + f"{output}.mp4"
        self.runBash(str)
