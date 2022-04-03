import io
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
from classes.cloudfile import CloudFile
from pipeline.steps.step import Step

# from tabulate import tabulate
from pipeline.utils.utils import Utils

SCOPES = ['https://www.googleapis.com/auth/drive']  # read,write,update,delete permission


class Input(Step):


    def __init__(self):
        self.service = self.get_gdrive_service()
    def get_gdrive_service(self):
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

    def process(self, data):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 5 files the user has access to.
        """

        # Call the Drive v3 API
        results = self.service.files().list(
            fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
        # get the results
        items = results.get('files', [])
        # file_metadata = {
        #     'name': 'Invoices',
        #     'mimeType': 'application/vnd.google-apps.folder'
        # }
        # file = service.files().create(body=file_metadata,
        #                                     fields='id').execute()
        # print
        # 'Folder ID: %s' % file.get('id')



        # folder id for minor 1IwR32VVb9QimVdXYDMGEfSdwJONuR9_X


        # list all 20 files & folders
        file = self.list_files(items)

        print(f"{items=}")
        print(f"{file=}")
        print(f"{len(file)=}")
        # self.upload_file(folderid=file.id)
        # self.download_file("11P_OhCF6PnofciQAbeqAJk_xrhETNjVR")

        for video in file:
            self.download_file(video)


    def list_files(self, items):
        """given items returned by Google Drive API, prints them in a tabular way"""
        file = None
        filesInFolder =[]
        if not items:
            # empty drive
            print('No files found.')
            return None

        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = self.get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            if name == "videos minor ai":
                file = CloudFile(id=id, name=name, parents=parents, size=size, mime_type=mime_type,
                                 time=modified_time)
                print(file)
            if parents[0] == "11P_OhCF6PnofciQAbeqAJk_xrhETNjVR":


                filesInFolder.append(id)

            # print("Files:")
            # convert to a human readable table
            # table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
            # print the table

        return filesInFolder

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

    def upload_file(self, folderid):
        file_metadata = {
            'name': 'school video.mp4',
            'parents': [folderid]
        }
        media = MediaFileUpload('school video.mp4',
                                mimetype='video/mp4',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def download_file(self, folderid):
        request = self.service.files().get_media(fileId=folderid)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)

        with open(f"{Utils().datafolder}{os.sep}{folderid}.mp4", 'wb') as f:
            f.write(fh.read())
            f.close()
