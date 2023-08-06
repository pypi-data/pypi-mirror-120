from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as g:
        long_description = f.read() + '\n\n' + g.read()

setup(
    name='django-gift-registry',
    version='0.5.3',
    description='A minimal wedding registry or gift registry app.',
    long_description=long_description,
    url='https://gitlab.com/BenSturmfels/django-gift-registry',
    author='Ben Sturmfels',
    author_email='ben@sturm.com.au',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'Django>=3.2',
        'Pillow>=2.5.1',
    ],
    package_data={
        'gift_registry': [
            'templates/gift_registry/*',
            'static/gift_registry/img/*',
            'fixtures/*',
        ],
    },
    project_urls={
        'Source': 'https://gitlab.com/BenSturmfels/django-gift-registry',
        'Bug Reports': 'https://gitlab.com/BenSturmfels/django-gift-registry/-/issues',
    }
)
