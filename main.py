import argparse
import datetime
import logging
import os
import qrcode
import sys
import validators

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes') # Directory for saving QR code
FILL_COLOR = os.getenv('FILL_COLOR', 'red') # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white') # Background color for the QR code

def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

def create_directory(path: Path):

    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f'Failed to create directory {path}: {e}')
        exit(1)

def is_valid_url(url):

    # Return True if URL is valid, else return false with an error message printed
    if validators.url(url):
        return True
    else:
        logging.error(f'Invalid URL provided: {url}')
        return False

def generate_qr_code(data, path, fill_color='red', back_color='white'):

    if not is_valid_url(data):
        return # Exit if the URL is invalid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        logging.info(f'Creating QR code with fill_color = {fill_color}, back_color = {back_color}')
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f'QR code successfully saved to {path}')

    except Exception as e:
        logging.error(f'An error occurred while generating or saving the QR code: {e}')

def main():

    # Do command-line parsing
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default='https://github.com/mbel12345')
    args = parser.parse_args()

    # Logging setup
    setup_logging()

    # Generate the timestamped filename for the QR code
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f'QRCode_{timestamp}.png'

    # Create the dir for the QR code file
    create_directory(Path.cwd() / QR_DIRECTORY)

    # Generate and save the QR code
    qr_full_file_path = Path.cwd() / QR_DIRECTORY / qr_filename
    generate_qr_code(args.url, qr_full_file_path, FILL_COLOR, BACK_COLOR)

if __name__ == '__main__':
    main()

