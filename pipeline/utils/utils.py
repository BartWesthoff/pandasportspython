import json
import pickle

import os
import sys

import moviepy.editor as mpy


class Utils:

    def __init__(self):
        self.name = "Utils"
        self.jsonfile = "testing.json"
        self.yamlfile = "settings.yaml"
        self.root_dir = os.getcwd()



    # def getdict(self):
    #     """" return the dictionary of all saved data """
    #     with open(self.jsonfile, "r") as f:
    #         a = json.load(f)
    #     # print(a)
    #     return a

    # def _checkifexists(self):
    #     """ check if jsonfile exists so that we can do IO operations"""
    #     if not os.path.exists(self.jsonfile):
    #         with open(self.jsonfile, "x") as f:
    #             f.write("{}")
    #
    #     with open(self.jsonfile, "r") as f:
    #         text = f.read()
    #         if len(text) == 0 or text[0] != '{':
    #             with open(self.jsonfile, "w+") as f:
    #                 f.write("{}")
    #
    #     if not os.path.exists(self.yamlfile):
    #         with open(self.yamlfile, "x") as f:
    #             f.write("")

    def save(self, _dict):
        """saves dictionary to disk"""
        with open(self.jsonfile, "w+") as f:
            json.dump(_dict, f, indent=4)


    def deletefile(self, filename):
        """deletes file from system"""
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("The file does not exist")

    def ensure_pythonhashseed(self, seed):
        """makes sure to run application with given pythonhashseed so outputs is not random """
        current_seed = os.environ.get("PYTHONHASHSEED")

        seed = str(seed)
        if current_seed is None or current_seed != seed:
            print(f'Setting PYTHONHASHSEED="{seed}"')
            os.environ["PYTHONHASHSEED"] = seed
            # restart the current process
            os.execl(sys.executable, sys.executable, *sys.argv)



    def save_model(self, model, modelname):
        """saves machine learning model"""
        filename = modelname + '.sav'
        pickle.dump(model, open(filename, 'wb'))

    def load_model(self, filename):
        """loads given machine loading model"""
        filename += ".sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model

    def load_yaml(self):
        """laods yamlfile """
        """returns settings type of dictionary"""
        with open(self.yamlfile, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    #
    # def save_yaml(self, data):
    #     """saves data to a yaml file"""
    #     with open(self.yamlfile, "w") as f:
    #         yaml.dump_all(data, f)
    # propably not needed ^^

    # def load_settings(self):
    #     """loads yamlfile """
    #     """returns settings type of dictionary"""
    #     with open(self.yamlfile, "r") as f:
    #         data = yaml.load(f, Loader=yaml.FullLoader)
    #     return data["settings"]

    # def edit_video(self):
    #     vcodec = "libx264"
    #
    #     videoquality = "24"
    #
    #     # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    #     compression = "slow"
    #
    #     title = "test"
    #     loadtitle = title + '.mov'
    #     savetitle = title + '.mp4'
    #
    #     # modify these start and end times for your subclips
    #     cuts = [('00:00:02.949', '00:00:04.152'),
    #             ('00:00:06.328', '00:00:13.077')]
    #     # load file
    #     video = mpy.VideoFileClip(loadtitle)
    #
    #     # cut file
    #     clips = []
    #     for cut in cuts:
    #         clip = video.subclip(cut[0], cut[1])
    #         clips.append(clip)
    #
    #     final_clip = mpy.concatenate_videoclips(clips)
    #
    #     # save file
    #     final_clip.write_videofile(savetitle, threads=4, fps=24,
    #                                codec=vcodec,
    #                                preset=compression,
    #                                ffmpeg_params=["-crf", videoquality])
    #
    #     video.close()

    def removesound(self, name):
        # TODO besluiten: videoclip in mp4,mpeg .... (Bart)
        videoclip = mpy.VideoFileClip(name)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(name.replace("squat0", "no_sound_squat"))

        videoclip.reader.close()
        videoclip.audio.reader.close_proc()


