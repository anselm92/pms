import secrets
import os

import matplotlib
from django.core.files.storage import FileSystemStorage
import logging

from matplotlib import pyplot
from stl import mesh

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
        with Image(filename=pdf + '[0]', resolution=300) as i:
            i.format = 'png'
            i.background_color = Color('white')  # Set white background.
            i.alpha_channel = 'remove'
            i.save(filename=pdf.replace('.pdf', '.png'))
    except:
        logger.error('Could not convert pdf to png. Please check your imagemagick and wand installation')


def convert_stl_to_png(stl):
    try:
        matplotlib.use('Agg')
        mesh_file = mesh.Mesh.from_file(stl)
        from mpl_toolkits import mplot3d
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Load the STL files and add the vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_file.vectors))

        # Auto scale to the mesh size
        scale = mesh_file.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        pyplot.savefig(stl.replace('.stl', '.png'))
    except:
        logger.error('Could not convert stl to png. Please check your numpy and matplotlib installation')
