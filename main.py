from tqdm import tqdm
import requests
import cgi
import sys
from urllib.parse import urlparse


def get_filename_from_url(url):
    """
    Extracts filename from the URL or content-disposition header.
    """
    parsed_url = urlparse(url)
    default_filename = parsed_url.path.split("/")[-1]

    response = requests.head(url)
    content_disposition = response.headers.get("Content-Disposition")

    if content_disposition:

        # parse the header using cgi
        value, params = cgi.parse_header(content_disposition)

        # extract filename from content disposition
        filename = params.get("filename", default_filename)
    else:
        
        # otherwise uses the default filename by url
        filename = default_filename

    return filename


def download_file(url):
    """
    Downloads a file from the given URL.
    """

    # Read amount of bytes every time
    buffer_size = 1024

    # Download the body by chunk
    response = requests.get(url, stream=True)

    # Get total file size from header
    file_size = int(response.headers.get('Content-Length', 0))
    filename = get_filename_from_url(url)

    progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_file.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    download_file(url)