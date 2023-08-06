from django import template

from django_image_sourceset.utils import get_image_in_size, get_complete_sourceset

register = template.Library()


@register.simple_tag
def image_size(image, size):
    """ returns a single image with max size """
    return get_image_in_size(image, size)


@register.inclusion_tag('django_image_sourceset/picture_tag.html')
def sourceset(image, name='default', **kwargs):
    context = {
        'images': get_complete_sourceset(image, name)
    }
    context.update(**kwargs)
    return context
