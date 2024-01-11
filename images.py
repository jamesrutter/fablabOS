import utils.google as google
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, HttpRequest
import io
import pprint

# Path to database
DATABASE = '../db/fablab.db'

# Google Drive Folder ID: Fab Lab App (Root)
FOLDER_ID = '1xE3B_5-EtqmvYmIAKCdHMeNFahVfp3oz'

# Google Drive Folder ID: Fab Lab App > Photos
PHOTOS_FOLDER_ID = '1ONLufSPSeu9u80VCrRXtfpffDLApJQaf'


def get_images(drive):
    """Returns a list of image files from the Fab Lab App > Photos folder.\n
    Args:
    - drive: Google Drive Resources service object
    """
    try:
        # Call the Drive v3 API
        results = (
            drive.files()
            .list(fields="files(id, name)", q="mimeType != 'application/vnd.google-apps.folder'")
            .execute()
        )
    except HttpError as error:
        print(f"An error occurred: {error}")
        return


def download_image(drive, file):
    """Downloads an image file from Google Drive and saves it to the images folder.\n
    Args:
    - drive: Google Drive Resources service object
    - file: file object (list with id and name)
    """
    # Get file ID and name from the file object
    file_id = file['id']
    file_name = file['name']

    try:
        # Create an API request for the file to download
        request: HttpRequest = drive.files().get_media(fileId=file_id)
        # Create a BytesIO object for the file to download into (memory buffer)
        buffer = io.BytesIO()
        # Create a downloader object for the file to download
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        # Download the file
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)} %")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    # Save the file to the images folder
    file_path = f"images/{file_name}"
    with open(file_path, 'wb') as f:
        f.write(file)


def main():
    drive = google.setup_gdrive()

    try:
        # Call the Drive v3 API
        query = f"mimeType != 'application/vnd.google-apps.folder' and '{PHOTOS_FOLDER_ID}' in parents"
        results = (
            drive.files()
            .list(fields="files(id, name)", q=query)
            .execute()
        )
        print("------------------------")
        print("Print results...")
        pprint.pprint(results)
        print("------------------------")
        print(type(results))
        items = results.get("files", [])
        print("Print items...")
        pprint.pprint(items)
        print(type(items))
        if not items:
            print("No files found.")
            return
        print("------------------------")
        print("Print list of files...")
        for item in items:
            print(f"{item['name']} ({item['id']})")
        print("------------------------")
        print(f'Number of files: {len(items)}')
        print("------------------------")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    main()
