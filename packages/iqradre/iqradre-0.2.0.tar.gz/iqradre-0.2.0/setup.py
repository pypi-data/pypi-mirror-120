from setuptools import setup, find_packages
from os import path
from setuptools.config import read_configuration

# conf_dict = read_configuration("setup.cfg")

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

print(path.join(here, 'requirements.txt'))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirement_packages = f.read().split("\n")


setup(
    name='iqradre',
    version='0.2.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nunenuh/iqradre',
    author='Lalu Erfandi Maula Yusnu',
    author_email='nunenuh@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='pytorch deep learning machine learning',  # Optional
    packages=find_packages(),  # Required

    python_requires='>=3.8',
    install_requires=requirement_packages,

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nunenuh/iqradre/issues',
        'Source': 'https://github.com/nunenuh/iqradre/',
    },
)
