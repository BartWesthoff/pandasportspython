import os

import cv2

from classes.cloudfile import CloudFile
from pipeline.steps.preprocessors.preprocessor import PreProcessor
from pipeline.utils.utils import Utils
import moviepy.editor as mpy

"""
PreProcessor class
used to preprocess video material
"""


class VideoPreProcessor(PreProcessor):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        data = self._preprocessVideo(data)

        return data

    def _preprocessVideo(self, data: list[CloudFile]):
        """
        :param query: string
        :return: modified string
        """
        for i in data:
            print(i.name)
        # idee is dat we deze video namen gebruiken om van gedownloaden data goede data te maken
        # wordt bijvoorbeeld gedownload in een download mapje,
        # en daar sorteren we de video's en bewerken we ze
        # bewerkte data komt dan is positief of negatief
        # kan ook in 1 mapje production

        for name in ["positive", "negative"]:
            folder = Utils().root_dir + os.sep + "data" + os.sep + f"{name}_squat" + os.sep
            for index, file_name in enumerate(os.listdir(folder)):
                # Construct old file name
                source = folder + file_name

                # Adding the count to the new file name and extension
                # TODO bespreken: hoe gaan we 'ready' data neerzetten?
                # met production data folder of gewoon overwritten
                destination = folder + f"{name}_squat{index // 2}.mp4"

                # destination = folder.replace(f'{name}_squat', "production") + f"{name}_squat{index}.mp4"

                # Video bestaat al zonder geluid
                if not os.path.exists(destination):
                    os.rename(source, destination)
                    self.removesound(str(destination))
        return data

    def removesound(self, name):
        videoclip = mpy.VideoFileClip(name)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(name.replace("squat0", "no_sound_squat"))

        videoclip.reader.close()
        videoclip.audio.reader.close_proc()

    def capFPS(self, name):
        video = mpy.VideoFileClip(name)
        video.write_videofile("final_clip.mp4", fps=15)

        video.close()

    def cropVideo(self, name: str, fps):

        # Open the video
        cap = cv2.VideoCapture(name)

        # Initialize frame counter
        cnt = 0

        # Some characteristics from the original video
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Here you can define your croping values
        x, y, w, h = 22, 22, 1037, 1877

        # output
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('result2.mp4', fourcc, fps, (w, h))

        # Now we start

        while (cap.isOpened()):
            ret, frame1 = cap.read()
            cnt += 1  # Counting frames

            # Avoid problems when video finish
            if ret:

                # Load our image
                #
                # im = frame1.copy()
                # H, W = im.shape[:2]
                #
                # # Convert image to grayscale
                # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #
                # # remove noise
                # im = cv2.GaussianBlur(im, (21, 21), 21)
                # im = cv2.erode(im, np.ones((5, 5)))
                #
                # # remove horizantal line
                # im = cv2.GaussianBlur(im, (5, 0), 21)
                # # blr = im.copy()
                #
                # # make binary image
                # im = cv2.threshold(im, 5, 255, cv2.THRESH_BINARY)[1]
                #
                # # Invert the black and white colors
                # im = ~im
                #
                # # Find contours and sort them by width
                # cnts, _ = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                # list(cnts).sort(key=lambda x: cv2.boundingRect(x)[2], reverse=True)

                cv2.rectangle(frame1, (x, y), (x + w, y + h), (128, 0, 255,), 10)

                # Save final result
                cv2.imwrite(f'img{cnt}.png', frame1[y:y + h, x:x + w])

                out.write(cv2.imread(f'img{cnt}.png'))
                os.remove(f'img{cnt}.png')

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
        return (x, y, w, h)

    def imageToVideo(self):
        image_folder = 'images'
        video_name = 'video.avi'

        images = [i.name for i in sorted(Path(image_folder).iterdir(), key=os.path.getmtime)]

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 30, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()