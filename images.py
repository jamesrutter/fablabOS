import utils.google as google
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, HttpRequest
import io
import os

# Path to image folder
IMAGE_FOLDER = 'assets/images/'

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
    Returns:
    - items: list of file objects (list with id and name)
    """
    print("Getting images from Google Drive...")
    try:
        # Construct the query for the Drive API
        query = f"mimeType != 'application/vnd.google-apps.folder' and '{PHOTOS_FOLDER_ID}' in parents"
        # Call the Drive v3 API with custom query
        results = (
            drive.files()
            .list(fields="files(id, name)", q=query)
            .execute()
        )
        # Get the list of files from the results and return it
        items = results.get("files", [])
        if not items:
            print("No files found.")
            return
        print(f'Found {len(items)} files.')
        print(type(items))
        return items
    except HttpError as error:
        print(f"An error occurred: {error}")


def download_image(drive, image):
    """Downloads an image file from Google Drive and saves it to the images folder.\n
    Args:
    - drive: Google Drive Resources service object
    - image: file object (list with id and name)
    """
    # Get file ID and name from the file object
    image_id = image['id']
    image_name = image['name']
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    # Check if the file already exists in the images folder
    if os.path.isfile(image_path):
        print(f"{image_name} already exists! Skipping download.")
        return

    print(f"Downloading {image_name}...")
    try:
        # Create an API request for the file to download
        request: HttpRequest = drive.files().get_media(fileId=image_id)
        # Create a BytesIO object for the file to download into (memory buffer)
        buffer = io.BytesIO()
        # Create a downloader object for the file to download
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        # Download the file
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloaded {int(status.progress() * 100)} %")

    except HttpError as error:
        print(f"An error occurred: {error}")
        image = None

    # Save the file to the images folder
    file_path = f"{IMAGE_FOLDER}{image_name}"
    with open(file_path, 'wb') as f:
        f.write(buffer.getvalue())
    print(f"File saved to {file_path}")


def main():
    drive = google.setup_gdrive()
    images = get_images(drive)
    for image in images:
        download_image(drive, image)


if __name__ == '__main__':
    main()
