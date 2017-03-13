from setuptools import setup
from setuptools import find_packages


setup(name='flickrDownloader',
      version='0.1.3',
      description='Helper for Flickr photos.search API',
      author='Riccardo Del Chiaro',
      author_email='riccardo.delchiaro@gmail.com',
      url='https://github.com/nagash91/python-flickr-image-downloader',
      license='MIT',
      packages=find_packages(),
      package_dir={'flickrDownloader':'flickrDownloader'},
      long_description=open('README.md').read(),
      requires=['requests']
      )

