import os
import urllib2
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError

def string_or_path(string_or_file):
    if os.path.isfile(string_or_file):
        ret = open(string_or_file, 'r').read()
    else:
        ret = string_or_file
    return ret


def web_downloader(link_list, download_path, save_filename_prefix="", save_filename_postfix="_", forced_extension=None,
                   verbose=False, ignore_errors=False):
    # type: (list(str), str, str, str, bool, bool) -> None

    client_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    if download_path != "" and not os.path.isdir(download_path):
        os.mkdir(download_path)

    error_count = 0
    for k, link in enumerate(link_list):

        try:
            req = Request(link, headers=client_header)
            response = urlopen(req)
            if forced_extension is not None:
                extension = forced_extension
            else:
                extension = os.path.splitext(link)[1].lower()
            output_file = open(os.path.join(download_path, save_filename_prefix + save_filename_postfix + str(k)
                                            + extension), 'wb')
            data = response.read()
            output_file.write(data)
            response.close()
            if verbose:
                print("completed ====> " + str(k))

        # IN this saving process we are just skipping the URL if there is any error
        except IOError:  # If there is any IOError
            error_count += 1
            if not ignore_errors:
                print("IOError on image " + str(k))

        except HTTPError:  # If there is any HTTPError
            error_count += 1
            if not ignore_errors:
                print("HTTPError" + str(k))

        except URLError:
            error_count += 1
            if not ignore_errors:
                print("URLError " + str(k))

        except ValueError:
            error_count += 1
            if not ignore_errors:
                print("ValueERROR " + str(k))

    if verbose:
        print("\nAll are downloaded")
    if verbose or not ignore_errors:
        print("Total Errors ----> " + str(error_count) )

    return error_count



import re, urlparse
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


# USE urllib2.quote instead
# def iriToUri(iri):
#     parts= urlparse.urlparse(iri)
#     return urlparse.urlunparse(
#         part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
#         for parti, part in enumerate(parts)
#     )