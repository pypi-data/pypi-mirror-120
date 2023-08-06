# django_image_sourceset - a simple sourceset generator

# Overview
With django_image_sourceset you can create with a simple templatetag a complete sourceset for images

# Usage
```html
{% sourceset header_image %}
```

# Optional Parameters
- title: The image title attr
- alt: The image alt attr
- class: The image class
- name: The IMAGE_SOURCESET_SIZE name. Default is 'default'

# Default sizes
```python
IMAGE_SOURCESET_SIZES = {
    'default': {
    'xs': {'width': 480, 'size': 480},
    'sm': {'width': 768, 'size': 768},
    'md': {'width': 1024, 'size': 1024},
    'lg': {'width': 1200, 'size': 1200},
    'xl': {'width': 1920, 'size': 1920},
    }
}
```

# Add new sizes
Add the following code to your settings.py
```python
IMAGE_SOURCESET_SIZES = {
    'new_sizes': {
    'xs': {'width': 300, 'size': 300},
    'sm': {'width': 400, 'size': 400},
    'md': {'width': 500, 'size': 500},
    }
}
```

And the following in your tag:
```html
{% sourceset header_image name='new_sizes' %}
```

# The result:
```html
<picture>
    <source media="(max-width: 480px)" srcset="/bild.jpg.840x0.jpg">
    <source media="(max-width: 768px)" srcset="/bild.jpg.1080x0.jpg">
    <source media="(max-width: 1024px)" srcset="bild.jpg.1500x0.jpg">
    <img alt="Alt" class="Class" srcset="/bild.jpg.1920x0.jpg" title="Title">
</picture>
```