import io
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from classes.cloudfile import CloudFile
from pipeline.steps.input.input import Input
from pipeline.utils.deprecated import deprecated
from pipeline.utils.utils import Utils


class GoogleDriveService(Input):
    """" Class for recieving data from Google Drive step"""

    def __init__(self):
        """" Instantiate the GoogleDriveService class """
        super().__init__()
        self.scopes = ['https://www.googleapis.com/auth/drive']  # read,write,update,delete permission
        self.service = self.get_gdrive_service()

    def process(self) -> list[CloudFile]:
        """given items returned by Google Drive API"""
        folder = self.get_files_in_folder("videos minor ai")
        print(f"found {len(folder)} files")
        for cloudfile in folder:
            if not os.path.exists(Utils().datafolder + os.sep + cloudfile.name):
                self.download_file(cloudfile)
                if self.settings['testing']:
                    break

        if self.settings['amount'] <= 0:
            return folder
        else:
            print(f"returning {self.settings['amount']} files")
            return folder[:self.settings['amount']]

    def get_gdrive_service(self) -> object:
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
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

    def get_files_in_folder(self, foldername: str) -> list[CloudFile]:
        """given items returned by Google Drive API"""
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

    @deprecated
    def get_size_format(self, b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    @deprecated
    def upload_file(self, parents: list[str], filename: str) -> None:
        name = f'{filename}.mp4',
        file_metadata = {
            'name': name,
            'parents': parents
        }
        media = MediaFileUpload(name,
                                mimetype='video/mp4',
                                resumable=True)
        self.service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

    def download_file(self, file: CloudFile) -> None:
        """" given a file, download it by its id """
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
