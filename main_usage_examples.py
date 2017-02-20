from flickrDownloader import *


api_key = "INSERT_HERE_YOUR_API_KEY"  # if you want to insert your apikey in source code
api_key = "flickr.apikey"  # if you want to read apikey from file

# If you want to share your code in git, you may want not to share your api key too!
# In that case, insert your api key in the flickr.apikey file and add flickr.apikey in your .gitignore


# Available licenses: (from: https://www.flickr.com/services/api/explore/flickr.photos.licenses.getInfo)
#
# {"id": 0, "name": "All Rights Reserved", "url": ""},
# {"id": 4, "name": "Attribution License", "url": "https:\/\/creativecommons.org\/licenses\/by\/2.0\/"},
# {"id": 6, "name": "Attribution-NoDerivs License", "url": "https:\/\/creativecommons.org\/licenses\/by-nd\/2.0\/"},
# {"id": 3, "name": "Attribution-NonCommercial-NoDerivs License", "url": "https:\/\/creativecommons.org\/licenses\/by-nc-nd\/2.0\/"},
# {"id": 2, "name": "Attribution-NonCommercial License", "url": "https:\/\/creativecommons.org\/licenses\/by-nc\/2.0\/"},
# {"id": 1, "name": "Attribution-NonCommercial-ShareAlike License",  "url": "https:\/\/creativecommons.org\/licenses\/by-nc-sa\/2.0\/"},
# {"id": 5, "name": "Attribution-ShareAlike License", "url": "https:\/\/creativecommons.org\/licenses\/by-sa\/2.0\/"},
# {"id": 7, "name": "No known copyright restrictions", "url": "https:\/\/www.flickr.com\/commons\/usage\/"},
# {"id": 8, "name": "United States Government Work", "url": "http:\/\/www.usa.gov\/copyright.shtml"},
# {"id": 9, "name": "Public Domain Dedication (CC0)", "url": "https:\/\/creativecommons.org\/publicdomain\/zero\/1.0\/"},
# {"id": 10, "name": "Public Domain Mark", "url": "https:\/\/creativecommons.org\/publicdomain\/mark\/1.0\/"}
license_id = 10  # "using public domain mark" license


link_list = flickr_photos_downloader(api_key,
                                     query_text="david michelangelo",
                                     # tags="",
                                     tag_mode=FlickrTagMode.all,
                                     download_path="michelangelo_download",
                                     image_size=FlickrImageSize.square_150x150,
                                     n_images=100,
                                     verbose=True,
                                     license_id=license_id)

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

for i, link in enumerate(only_link):
    print str(i) + "\t-\t" + link

responsesJson = flickr_photos_search(api_key,
                                     n_images=1500,
                                     query_text="Firenze",
                                     tags="Art",
                                     tag_mode=FlickrTagMode.any,
                                     content_type=FlickrContentType.photos,
                                     media=FlickrMedia.photos,
                                     response_format=FlickrResponseFormat.JSON,
                                     license_id=license_id)


