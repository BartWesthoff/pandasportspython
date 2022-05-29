import io
import os
import pickle
from abc import abstractmethod

import yaml
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from classes.cloudfile import CloudFile
# from tabulate import tabulate
from pipeline.utils.utils import Utils


SCOPES = ['https://www.googleapis.com/auth/drive']  # read,write,update,delete permission


class Input:
    """" checks if class is instantiated"""
    # Klasse voor de imput van de googleDrive
    def __init__(self):
        """ this has to be type because in a """
        """ inherented situation it will always become true """
        # NOTE: issubclass(self.__class__, type) werkt niet
        if self.__class__ == Input:
            raise Exception('I am abstract!')

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def process(self) -> object:
        pass

    @property
    def settings(self) -> dict:
        with open("settings.yaml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["settings"]


class GoogleDriveService(Input):
    # Klasse voor het opzetten van een verbinding met de GoogleDrive

    def __init__(self):
        super().__init__()
        self.service = self.get_gdrive_service()

    #Verbinden met Google Drive
    @staticmethod
    def get_gdrive_service() -> object:
        """" instantiate a Google Drive service object """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

    # Open een specifieke folder en download alle files die gedownload kunnen worden.
    # functie returns de specifieke folder
    def process(self) -> list[CloudFile]:
        """given items returned by Google Drive API"""
        """returns list of CloudFile objects"""
        folder = self.get_files_in_folder("videos minor ai")
        for cloudfile in folder:
            if not os.path.exists(Utils().datafolder + os.sep + cloudfile.name):
                # TODO check if cloudfile.name is str
                self.download_file(cloudfile)
                if self.settings['testing']:
                    break
        return folder

    # Haalt alle files op uit de folder
    def get_files_in_folder(self, foldername: str) -> list[CloudFile]:
        """given items returned by Google Drive API"""
        """returns list of CloudFile objects"""
        # TODO check naam ipv folder ID

        results = self.service.files().list(pageSize=400,  # TODO kijken of je kan querying op folder ipv alle bestanden
                                            fields="nextPageToken, files(id, name, parents)").execute()
        # get the results
        folderid = "1GO8kwJTL8x8Pg1Dy5AdhCOECz9rKoqOs"
        items = results.get('files', [])

        if not items:
            # empty drive
            print('No files found.')
            return []

        files_in_folder = []
        for item in items:
            item_id = item["id"]
            name = item["name"]

            parents = [None]
            if "parents" in item:
                parents = item["parents"]
            if parents == [folderid]:
                files_in_folder.append(CloudFile(id=item_id, name=name, parents=parents))
                # files_in_folder.append({"name": name, "id": item_id})
        return files_in_folder

    # deprecated
    # def get_size_format(self, b, factor=1024, suffix="B"):
    #     """
    #     Scale bytes to its proper byte format
    #     e.g:
    #         1253656 => '1.20MB'
    #         1253656678 => '1.17GB'
    #     """
    #     for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
    #         if b < factor:
    #             return f"{b:.2f}{unit}{suffix}"
    #         b /= factor
    #     return f"{b:.2f}Y{suffix}"

    # deprecated
    # def upload_file(self, folderid):
    #     file_metadata = {
    #         'name': 'school video.mp4',
    #         'parents': [folderid]
    #     }
    #     media = MediaFileUpload('school video.mp4',
    #                             mimetype='video/mp4',
    #                             resumable=True)
    #     self.service.files().create(body=file_metadata,
    #                                 media_body=media,
    #                                 fields='id').execute()

    # Functie om files mee te downloaden
    def download_file(self, file: CloudFile) -> None:
        file_id = file.id
        name = file.name
        print(f"downloading {name}")
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}")
        fh.seek(0)

        with open(f"{Utils().datafolder}{os.sep}{name}", 'wb') as f:
            f.write(fh.read())
