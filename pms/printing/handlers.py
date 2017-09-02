import secrets
import os

from django.core.files.storage import FileSystemStorage
import logging

from pms import settings
from pms.settings import FILES_ROOT

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
        with Image(filename=pdf + '[0]', resolution=70) as i:
            i.format = 'png'
            i.background_color = Color('white')  # Set white background.
            i.alpha_channel = 'remove'
            i.save(filename=pdf.replace('.pdf', '.png'))
    except:
        logger.error('Could not convert pdf to png. Please check your imagemagick and wand installation')


def process_stl(stl, order):
    try:
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import pyplot

        from numpy.ma import subtract
        from stl import mesh

        mesh_file = mesh.Mesh.from_file(stl)
        from mpl_toolkits import mplot3d
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Load the STL files and add the vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_file.vectors))

        size = subtract(mesh_file.max_, mesh_file.min_)
        order.width = size[0]
        order.depth = size[1]
        order.height = size[2]
        order.save()
        scale = mesh_file.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        pyplot.savefig(stl.replace('.stl', '.png'))
    except:
        logger.error('Could not convert stl to png. Please check your numpy and matplotlib installation')


def _delete_order(order_hash):
    """ Deletes file from filesystem. """
    path = os.path.join(FILES_ROOT, order_hash)
    print(path)
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(path, file))
    os.rmdir(path)
