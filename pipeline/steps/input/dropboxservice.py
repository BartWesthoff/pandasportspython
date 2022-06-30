import json
import os
import pickle

import dropbox
import requests

from classes.cloudfile import CloudFile
from pipeline.steps.input.input import Input
from pipeline.utils.utils import Utils


class DropBoxService(Input):
    """" Class for recieving data from Dropbox"""

    def __init__(self):
        """" Instantiate the DropBoxService class """
        super().__init__()
        self.shared_link = dropbox.files.SharedLink(
            self.get_source())
        self.service = dropbox.Dropbox(
            self.get_token())

    def process(self) -> list[CloudFile]:
        """given items returned by Dropbox API"""
        folder = self.get_files_in_folder()

        # convert every file from folder to a CloudFile object
        folder = [CloudFile(name=file.name, parents='', id=file.id) for file in folder]

        print(f"found {len(folder)} file(s)")
        if self.settings["amount"] < 0:
            self.settings["amount"] = len(folder)
        for entry in folder[:self.settings["amount"]]:

            if not os.path.exists(Utils().datafolder + os.sep + entry.name):
                self.download_file(entry.name)
                if self.settings["testing"]:
                    break

        print(f"returning {min(self.settings['amount'], len(folder))} file(s)")
        return folder[:self.settings["amount"]]

    def get_token(self):
        """ get the access token from the pickle file """
        try:
            with open(os.sep.join(["data", "credentials", "acces_token.pickle"]), "rb") as token:
                creds = pickle.load(token)
        except FileNotFoundError:
            self.refresh_token()
        return creds

    def get_source(self) -> str:
        """ get the source from the dropbox file """
        with open(os.sep.join(["data", "credentials", "source.pickle"]), "rb") as token:
            source = pickle.load(token)
        return source

    def get_files_in_folder(self) -> list[CloudFile]:
        """given items returned by Dropbox"""
        listing = self.service.files_list_folder(path="", shared_link=self.shared_link)
        # todo: add implementation for files_list_folder_continue
        return listing.entries

    def download_file(self, name: str) -> None:
        """" given a file, download it by its name """

        if name.endswith(".mp4"):
            with open(os.sep.join([Utils().datafolder, name]), "wb") as f:
                # note: this simple implementation only works for files in the root of the folder
                metadata, res = self.service.sharing_get_shared_link_file(url=self.shared_link.url,
                                                                          path="/" + name)
                f.write(res.content)

    def refresh_token(self):
        """ refresh the access token """
        app_key = "7yiemxlek5s846k"
        app_secret = "g70t3hljceheq04"

        # build the authorization URL:
        authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

        # send the user to the authorization URL:

        print(authorization_url)

        # get the authorization code from the user:
        authorization_code = input("Enter the code:\n")

        # exchange the authorization code for an access token:
        token_url = "https://api.dropboxapi.com/oauth2/token"
        params = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "client_id": app_key,
            "client_secret": app_secret
        }
        r = requests.post(token_url, data=params)
        res = json.loads(r.text)
        Utils().saveObject(res["access_token"], os.sep.join(["data", "credentials", "acces_token.pickle"]))
