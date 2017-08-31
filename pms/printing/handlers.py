import secrets
import os

from django.core.files.storage import FileSystemStorage
import logging

from pms import settings

fs = FileSystemStorage(location=settings.FILES_ROOT)
logger = logging.getLogger(__name__)

CONTENT_TYPES = {
    '.pdf': 'application/pdf', '.jpg': 'image/jpg', '.png': 'image/png',
    '.jpeg': 'image/jpg', '.zip': 'application/zip', '.svg': 'image/svg',
}


def order_files_upload_handler(order, filename):
    order.file_name = filename
    return "{hash}/{file}".format(hash=order.order_hash,
                                  file=secrets.token_urlsafe(20) + os.path.splitext(filename)[1])


def convert_pdf_to_png(pdf):
    try:
        from wand.color import Color
        from wand.image import Image
        with Image(filename=pdf+'[0]', resolution=300) as i:
            i.format = 'png'
            i.background_color = Color('white')  # Set white background.
            i.alpha_channel = 'remove'
            i.save(filename=pdf.replace('.pdf', '.png'))
    except:
        logger.error('Could not convert pdf to png. Please check your imagemagick and wand installation')
