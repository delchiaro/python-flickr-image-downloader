from flickrDownloader import *

api_key = "INSERT_HERE_YOUR_API_KEY"  # if you want to insert your apikey in source code
api_key = "flickr.apikey"  # if you want to read apikey from file

# If you want to share your code in git, you may want not to share your api key too!
# In that case, insert your api key in the flickr.apikey file and add flickr.apikey in your .gitignore



link_list = flickr_photos_downloader(api_key,
                                     query_text="david michelangelo",
                                     # tags="",
                                     tag_mode=FlickrTagMode.all,
                                     download_path="michelangelo_download",
                                     image_size=FlickrImageSize.square_150x150,
                                     n_images=100,
                                     verbose=True)

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
                         ignore_errors=False)


only_link = flickr_photos_links(api_key,
                                n_images=1500,
                                query_text="Firenze",
                                tags="Art",
                                tag_mode=FlickrTagMode.any,
                                image_size=FlickrImageSize.longedge_1600,
                                content_type=FlickrContentType.photos,
                                media=FlickrMedia.photos,
                                verbose=True,
                                ignore_errors=False)

for i, link in enumerate(only_link):
    print str(i) + "\t-\t" + link

responsesJson = flickr_photos_search(api_key,
                                     n_images=1500,
                                     query_text="Firenze",
                                     tags="Art",
                                     tag_mode=FlickrTagMode.any,
                                     content_type=FlickrContentType.photos,
                                     media=FlickrMedia.photos,
                                     response_format=FlickrResponseFormat.JSON)


