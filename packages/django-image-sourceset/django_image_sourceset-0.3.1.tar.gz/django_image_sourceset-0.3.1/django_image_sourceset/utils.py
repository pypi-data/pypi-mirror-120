import hashlib
import os

import requests
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import ImageFieldFile
from easy_thumbnails.files import get_thumbnailer

from django_image_sourceset.conf import IMAGE_SOURCESET_SIZES


def get_size_type(name='default'):
    return IMAGE_SOURCESET_SIZES.get(name, IMAGE_SOURCESET_SIZES['default'])


def get_size(size, name='default'):
    return get_size_type(name).get(size)


def get_thumbnail_object(image):
    if isinstance(image, ImageFieldFile):
        return get_thumbnailer(image)
    elif image.startswith('http'):
        response = requests.get(image, stream=True, timeout=1)
        file_name = os.path.join('url_files', "%s.%s" % (hashlib.md5(image.encode()).hexdigest(), image.rsplit('.', 1)[1]))
        path = os.path.join(settings.MEDIA_ROOT, file_name)
        if not os.path.exists(path):
            storage = FileSystemStorage()
            storage.save(path, ContentFile(response.content))
        return get_thumbnailer(default_storage.open(path), relative_name=file_name)
    else:
        try:
            return get_thumbnailer(staticfiles_storage.open(image), relative_name=image)
        except FileNotFoundError:
            return None


def get_image_in_size(image, size):
    thumbnailer = get_thumbnail_object(image)
    thumb = thumbnailer.get_thumbnail({'size': (get_size(size), 0)})
    return thumb.url


def get_complete_sourceset(image, name='default'):
    thumbnailer = get_thumbnail_object(image)
    sizes = get_size_type(name)
    images = []
    for key, value in sizes.items():
        try:
            images.append({
                'size': value['width'],
                'url': thumbnailer.get_thumbnail({'size': (value['size'], 0)}).url
            })
        except (FileNotFoundError, AttributeError) as e:
            # At this point a strange error occurs sporadically, where easy_thumbnails tries to save a thumbnail and fails
            pass

    images = sorted(images, key=lambda k: k['size'])
    return images
