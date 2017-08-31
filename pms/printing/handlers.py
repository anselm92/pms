import secrets
import os

from django.core.files.storage import FileSystemStorage

from pms import settings

fs = FileSystemStorage(location=settings.FILES_ROOT)

CONTENT_TYPES = {
    '.pdf': 'application/pdf', '.jpg': 'image/jpg', '.png': 'image/png',
    '.jpeg': 'image/jpg', '.zip': 'application/zip', '.svg': 'image/svg',
}


def order_files_upload_handler(order, filename):
    order.file_name = filename
    return "{hash}/{file}".format(hash=order.order_hash,
                                         file=secrets.token_urlsafe(20) + os.path.splitext(filename)[1])
