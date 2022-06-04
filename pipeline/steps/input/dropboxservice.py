import dropbox

from classes.cloudfile import CloudFile
from pipeline.steps.input.input import Input


class DropBoxService(Input):
    """" Class for recieving data from Google Drive step"""

    def __init__(self):
        """" Instantiate the GoogleDriveService class """
        super().__init__()
        self.shared_link = dropbox.files.SharedLink(
            url="https://www.dropbox.com/sh/37i4bda7vse3dof/AABf_QVa_nExn7qxcUP7pR8Ua?dl=0")
        self.service = dropbox.Dropbox(
            "sl.BI4uK4R_KXtpb21NYg_KtwA9CajhhRCJ7W7w6JuQXmIw1OhLf5IPi74_qmU-AqP4WMFDqkKRADOH0-OkQfo2p31_oQJPYTKcXOHb5QtqClzTT0p5640IlCxp9cLkJgqbPZW4QSJyNVG9")

    def process(self) -> None:
        """given items returned by Google Drive API"""
        folder = self.get_files_in_folder("videos minor ai")
        print(f"found {len(folder)} files")
        for entry in folder:
            if entry.name.endswith(".mp4"):
                with open(entry.name, "wb") as f:
                    # note: this simple implementation only works for files in the root of the folder
                    metadata, res = self.service.sharing_get_shared_link_file(url=self.shared_link.url,
                                                                          path="/" + entry.name)
                    f.write(res.content)

    def get_files_in_folder(self, foldername: str) -> list[CloudFile]:
        """given items returned by Google Drive API"""
        listing = self.service.files_list_folder(path="", shared_link=self.shared_link)
        # todo: add implementation for files_list_folder_continue
        return listing.entries

    def download_file(self, name: str) -> None:
        """" given a file, download it by its name """

        if name.endswith(".mp4"):
            with open(name, "wb") as f:
                # note: this simple implementation only works for files in the root of the folder
                metadata, res = self.service.sharing_get_shared_link_file(url=self.shared_link.url,
                                                                          path="/" + name)
                f.write(res.content)
