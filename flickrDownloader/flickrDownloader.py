import json
from enum import Enum
import requests
from requests import Response

from utils import string_or_path
from utils import web_downloader

# TODO: always using public for now
class FlickrPrivacyFilter(Enum):
    default         = ""
    public          = "&privacy_filter=1"
    friends         = "&privacy_filter=2"
    family          = "&privacy_filter=3"
    friends_family  = "&privacy_filter=4"
    private         = "&privacy_filter=5"


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


    # TODO: original image: jpg, gif or png according to the source format, not supported yet
    #  original = "_o"
    # Require original secret (o-secret) but in responses I can't see that entry:
    # https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)
# class FlickrImageExtension(Enum):
#     jpg = "jpg"
#     png = "png"
#     gif = "gif"
#     default = jpg

# TODO: add localizations
def flickr_photos_search(api_key_or_file_path,                      # type: str
                         n_images=100,                              # type: int
                         query_text=None,                           # type: str
                         tags=None,                                 # type: str
                         tag_mode=FlickrTagMode.default,            # type: FlickrTagMode
                         content_type=FlickrContentType.default,    # type: FlickrContentType
                         media=FlickrMedia.default,                 # type: FlickrMedia
                         response_format=FlickrResponseFormat.JSON  # type: FlickrResponseFormat
                         ):
    # type: (str, int, str, str, FlickrTagMode, FlickrContentType, FlickrMedia, FlickrResponseFormat) -> list(Response)
    """

    :rtype: list(Response)
    """
    MAX_IMAGES_PER_PAGE = 500 # fixed by flickr api

    if not isinstance(api_key_or_file_path, str):
        raise ValueError("api_key_or_file_path must be a str (flickr api key or path to text file containing key).")
    api_key = string_or_path(api_key_or_file_path).split(" ")[0].split("\n")[0]


    query = "https://api.flickr.com/services/rest/?method=flickr.photos.search"
    query += "&api_key=" + api_key

    if isinstance(query_text, str):
        query += "&text=" + query_text
    if isinstance(tags, str):
        query += "&tags=" + tags + tag_mode.value
    #  query.replace(" ", "%20")
    query += content_type.value + media.value + response_format.value + FlickrPrivacyFilter.public.value

    rest = n_images % MAX_IMAGES_PER_PAGE
    n_queries = n_images/MAX_IMAGES_PER_PAGE
    query_len_list = [MAX_IMAGES_PER_PAGE] * n_queries
    if rest > 0:
        query_len_list.append(rest)

    responses = []
    for i, query_len in enumerate(query_len_list):
        page_query = query + "&per_page=" + str(query_len) + "&page=" + str(i+1)
        responses.append(requests.get(page_query))

    return responses


def flickr_photos_links(api_key_or_file_path,                    # type: str
                        n_images=100,                            # type: int
                        query_text=None,                         # type: str
                        tags=None,                               # type: str
                        image_size=FlickrImageSize.default,      # type: FlickrImageSize
                        tag_mode=FlickrTagMode.default,          # type: FlickrTagMode
                        content_type=FlickrContentType.default,  # type: FlickrContentType
                        media=FlickrMedia.default,               # type: FlickrMedia
                        verbose=False,
                        ignore_errors=False
                        ):
    # type: (...) -> list(str)

    responses = flickr_photos_search(api_key_or_file_path=api_key_or_file_path,  n_images=n_images,
                                     query_text=query_text, tags=tags, tag_mode=tag_mode,
                                     content_type=content_type, media=media,
                                     response_format=FlickrResponseFormat.JSON)
    links = []

    for response in responses:
        if response.ok:
            content = response.content
            data = json.loads(content)
            if 'photos' in data.keys():
                data = data['photos']['photo']
                for d in data:
                    # https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg
                    lnk = "https://farm{}.staticflickr.com/{}/{}_{}{}.jpg"\
                        .format(d['farm'], d['server'], d['id'], d['secret'], image_size.value)
                    links.append(lnk)
            else:
                if not ignore_errors:
                    print("Format error in received json (can't find key 'photos').")
                    if 'message' in data.keys():
                        print("Received Message: {}".format(data['message']))

        else:
            if not ignore_errors:
                print("Flickr response not ok.")
    if verbose:
        print("Links retrived from flickr responses: {}".format(len(links)))
    return links



def flickr_photos_downloader(api_key_or_file_path,                    # type: str
                             n_images=100,                            # type: int
                             query_text=None,                         # type: str
                             tags=None,                               # type: str
                             tag_mode=FlickrTagMode.default,          # type: FlickrTagMode
                             image_size=FlickrImageSize.default,      # type: FlickrImageSize
                             content_type=FlickrContentType.default,  # type: FlickrContentType
                             media=FlickrMedia.default,               # type: FlickrMedia
                             download_path="",
                             save_filename_prefix="flickr_",
                             forced_extension=None,
                             verbose=False,
                             ignore_errors=False
                             ):
    # type: (...) -> list(str)

    links = flickr_photos_links(api_key_or_file_path=api_key_or_file_path, query_text=query_text, tags=tags, n_images=n_images,
                                image_size=image_size, tag_mode=tag_mode, content_type=content_type, media=media,
                                verbose=verbose, ignore_errors=ignore_errors)
    web_downloader(link_list=links, download_path=download_path, save_filename_prefix=save_filename_prefix,
                   forced_extension=forced_extension, verbose=verbose, ignore_errors=ignore_errors)
    return links






# Flickr Documentations:
# For search:
# https://www.flickr.com/services/api/explore/flickr.photos.search
# (use public = 1 in the query!)
# (log in in flickr to automatically insert my api key).
#
#
# To download images, look at here: https://www.flickr.com/services/api/misc.urls.html
# example: http://farm3.staticflickr.com/2636/32179988483_cd41d8fca9_b.jpg
#
# Otherwise you can use getSize query and use the source response to get the direct link:
#   http://www.flickr.com/services/api/flickr.photos.getSizes.html
#












# * * * * * * * * * * * * * * * * * * * SEARCH API * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# SEARCH API ( https://www.flickr.com/services/api/flickr.photos.search.html )
# EXAMPLE OF QUERY:
# https://api.flickr.com/services/rest/?method=flickr.photos.search
# &api_key=API_KEY
# &tags=art
# &text=david
# &per_page=100
# &page=1
# &format=json

# tags (Facoltativo)
# A comma-delimited list of tags. Photos with one or more of the tags listed will be returned. You can exclude results
# that match a term by prepending it with a - character.

# tag_mode (Facoltativo)
# Either 'any' for an OR combination of tags, or 'all' for an AND combination. Defaults to 'any' if not specified.

# text (Facoltativo)
# A free text search. Photos who's title, description or tags contain the text will be returned. You can exclude results
# that match a term by prepending it with a - character.

# sort (Facoltativo)
# The order in which to sort returned photos. Deafults to date-posted-desc (unless you are doing a radial geo query, in
# which case the default sorting is by ascending distance from the point specified). The possible values are:
# date-posted-asc,
# date-posted-desc,
# date-taken-asc,
# date-taken-desc,
# interestingness-desc,
# interestingness-asc,
# relevance.


# privacy_filter (Facoltativo)
# Return photos only matching a certain privacy level.
# This only applies when making an authenticated call to view photos you own.
# Valid values are:
# 1 public photos
# 2 private photos visible to friends
# 3 private photos visible to family
# 4 private photos visible to friends & family
# 5 completely private photos


# content_type (Facoltativo)
# Content Type setting:
# 1 for photos only.
# 2 for screenshots only.
# 3 for 'other' only.
# 4 for photos and screenshots.
# 5 for screenshots and 'other'.
# 6 for photos and 'other'.
# 7 for photos, screenshots, and 'other' (all).


# media (Facoltativo)
# Filter results by media type. Possible values are all (default), photos or videos



# per_page (Facoltativo)
# Number of photos to return per page. If this argument is omitted, it defaults to 100. The maximum allowed value is 500.

# page (Facoltativo)
# The page of results to return. If this argument is omitted, it defaults to 1.




# FOR LOCALIZATION:

# geo_context (Facoltativo)
# Geo context is a numeric value representing the photo's geotagginess beyond latitude and longitude.
# For example, you may wish to search for photos that were taken "indoors" or "outdoors".
# The current list of context IDs is :
# 0, not defined.
# 1, indoors.
# 2, outdoors.
# Geo queries require some sort of limiting agent in order to prevent the database from crying.
# This is basically like the check against "parameterless searches" for queries without a geo component.
#

# A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters
# If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).
# lat (Facoltativo)
# A valid latitude, in decimal format, for doing radial geo queries.
# Geo queries require some sort of limiting agent in order to prevent the database from crying.
# This is basically like the check against "parameterless searches" for queries without a geo component.
# A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters
# If no limiting factor is passed we return only photos added in the last 12 hours
# (though we may extend the limit in the future).

# lon (Facoltativo)
# A valid longitude, in decimal format, for doing radial geo queries.
# Geo queries require some sort of limiting agent in order to prevent the database from crying.
# This is basically like the check against "parameterless searches" for queries without a geo component.
# A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters
# If no limiting factor is passed we return only photos added in the last 12 hours
# (though we may extend the limit in the future).


# radius (Facoltativo)
# A valid radius used for geo queries, greater than zero and less than 20 miles (or 32 kilometers), for use with point-based geo queries. The default value is 5 (km).

# radius_units (Facoltativo)
# The unit of measure when doing radial geo queries. Valid options are "mi" (miles) and "km" (kilometers). The default is "km".



# bbox (Facoltativo)
# A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched.
# The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude,
# minimum_latitude, maximum_longitude, maximum_latitude.
# Longitude has a range of -180 to 180 , latitude of -90 to 90. Defaults to -180, -90, 180, 90 if not specified.
# Unlike standard photo queries, geo (or bounding box) queries will only return 250 results per page.
# Geo queries require some sort of limiting agent in order to prevent the database from crying.
# This is basically like the check against "parameterless searches" for queries without a geo component.
# A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters
# If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).

# accuracy (Facoltativo)
# Recorded accuracy level of the location information. Current range is 1-16 :
# World level is 1
# Country is ~3
# Region is ~6
# City is ~11
# Street is ~16
# Defaults to maximum value if not specified.
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
