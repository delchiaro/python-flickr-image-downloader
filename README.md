# Python Flickr Images Downloader
Python functions for searching and downloading images/links from Flickr.<br />
Use the flickr.photos.search API to search image (using tags/text):<br />
https://www.flickr.com/services/api/explore/flickr.photos.search<br />

## Compatability
Tested only on python 2.7

## Limitations
Not all the possible search arguments are implemented (for example place, geolocalization, and others).


## Disclaimer
This program lets you download tons of images from Flickr.<br />
Please do not violate its copyright or license terms. <br />
 <br />
Flickr photos licenses API:  <br />
https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html
https://www.flickr.com/services/api/explore/flickr.photos.licenses.getInfo

## Install
git clone https://github.com/nagash91/python-flickr-image-downloader.git <br />
cd python-flickr-image-downloader <br />
sudo python setup.py install <br />
 <br />

## Usage
```python
from flickrDownloader import *

api_key = "INSERT_HERE_YOUR_API_KEY"  # if you want to insert your apikey in source code
api_key = "flickr.apikey"  # if you want to read apikey from file

license_id = 10  # "using public domain mark" license

# Get links and download photos:
flickr_photos_downloader(api_key,
                         n_images=10,
                         query_text="Firenze",
                         tags="Art",
                         tag_mode=FlickrTagMode.any,
                         image_size=FlickrImageSize.longedge_1600,
                         content_type=FlickrContentType.photos,
                         media=FlickrMedia.photos,
                         download_path="img_downloads",
                         save_filename_prefix="flickr_downloaded_",
                         forced_extension=None,
                         verbose=True,
                         ignore_errors=False,
                         license_id=license_id)

# Get links only:
only_link = flickr_photos_links(api_key,
                                n_images=1500,
                                query_text="Firenze",
                                tags="Art",
                                tag_mode=FlickrTagMode.any,
                                image_size=FlickrImageSize.longedge_1600,
                                content_type=FlickrContentType.photos,
                                media=FlickrMedia.photos,
                                verbose=True,
                                ignore_errors=False,
                                license_id=license_id)
# Print links:
for i, link in enumerate(only_link):
    print str(i) + "\t-\t" + link                       
```
 <br />
 <br />
Available options:
```python
# ENUM DEFINED FOR OPTIONS:

class FlickrContentType(Enum):
    default                  = ""
    photos                   = "&content_type=1"
    screenshoots             = "&content_type=2"
    other                    = "&content_type=3"
    photos_screenshots       = "&content_type=4"
    screenshoots_other       = "&content_type=5"
    photos_other             = "&content_type=6"
    photos_screenshots_other = "&content_type=7"


class FlickrTagMode(Enum):
    default = ""
    any     = '&tag_mode=any' # logic OR
    all     = '&tag_mode=all' # logic AND


class FlickrMedia(Enum):
    default = ""
    photos  = "&media=photos"
    videos  = "&media=videos"


class FlickrResponseFormat(Enum):
    JSON       = "&format=json&nojsoncallback=1"
    JSONP      = "&format=json"
    XML        = "&format=rest"
    PHP_SERIAL = "&format=php_serial"
    default = JSON

class FlickrImageSize(Enum):
    default = ""
    square_75x75   = "_s"  # 75 x 75
    square_150x150 = "_q"  # 150 x 150
    longedge_100   = "_t"  # 100 on the longest edge
    longedge_240   = "_m"  # 240 on the longest edge
    longedge_320   = "_n"  # 320 on the longest edge
    longedge_500   = "_-"  # 500 on the longest edge
    longedge_640   = "_z"  # 640 on the longest edge
    longedge_800   = "_c"  # 800 on the longest edge (flickr new feature from 01/03/2012)
    longedge_1024  = "_b"  # 1024 on the longest edge
    longedge_1600  = "_h"  # 1600 on the longest edge (flickr new feature from 01/03/2012)
    longedge_2048  = "_k"  # 2048 on the longest edge (flickr new feature from 01/03/2012)
```
