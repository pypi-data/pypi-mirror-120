from distutils.core import setup

setup(
    name="django_image_sourceset",
    version="0.3.1",
    description='Create a sourceset for an django image',
    author='Martin Gutmair',
    author_email='martin@gutmair.de',
    url='https://gitlab.com/gudi89/django_image_sourceset',
    license='MIT',
    download_url='https://gitlab.com/gudi89/django_image_sourceset/-/archive/0.3.1/django_image_sourceset-0.3.1.tar.gz',
    packages=['django_image_sourceset', 'django_image_sourceset.templates', 'django_image_sourceset.templatetags'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >=2.0',
        'easy-thumbnails==2.7'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
