from django.conf import settings

IMAGE_SOURCESET_SIZES = {
    'default': {
        'xs': {'width': 480, 'size': 480},
        'sm': {'width': 768, 'size': 768},
        'md': {'width': 1024, 'size': 1024},
        'lg': {'width': 1200, 'size': 1200},
        'xl': {'width': 1920, 'size': 1920},
    }
}

IMAGE_SOURCESET_SIZES.update(getattr(settings, 'IMAGE_SOURCESET_SIZES', {}))
