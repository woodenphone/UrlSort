#-------------------------------------------------------------------------------
# Name:        linksorter
# Purpose:      Sorting urls from a file into lists for each site
#
# Author:      new
#
# Created:     20/03/2013
# Copyright:   (c) new 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import re
import urlparse
import os
import fnmatch
import logging




def uniquify(seq, idfun=None):
    # List uniquifier from
    # http://www.peterbe.com/plog/uniqifiers-benchmark
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


def extractlinks(html):
    # Copied from:
    # http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python
    # old regex http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    links = re.findall(url_regex,html, re.DOTALL)
    return links


def load_textfile(filepath):
    # Return data in specified file, if no file found create it.
    new_file_text = 'Put text containing URLs here'
    if os.path.exists(filepath):
        f = open(filepath,'rU')
        file_data = f.read()
        f.close()
        print 'File loaded'
        return file_data
    else:
        f = open(filepath,'w')
        f.write(new_file_text)
        f.close()


def save_text(filepath,data):
    #print 'save_text:filepath', filepath
    save_dir = os.path.dirname(filepath)
    #print 'save_text:save_dir', save_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    f = open(filepath,'w')
    f.write(data)
    f.close()
    #print 'save_text:Saved data to file', filepath


def extract_domain(url):
    #return the domain from given url
    # print 'extract_domain:url', url
    full_domain = urlparse.urlparse(url).netloc
    # print 'extract_domain:full_domain', full_domain
    domain = re.sub('^www\.','',full_domain)
    domain = sanitize_dict_name(domain)
    # Handle known problem cases
    # DeviantArt.com
    if 'deviantart.com' in domain:
        short_domain = re.sub('.+deviantart.com', 'deviantart.com', domain)
        return short_domain
    # Tumblr.com
    elif '.tumblr.com' in domain:
        short_domain = re.sub('.+tumblr.com', 'tumblr.com', domain)
        return short_domain
    # Too long
    elif len(domain) > 200:
        return "TOO_LONG"
    else:
        return domain


def sanitize_filename(filename):
    # Sanitize a filename (not a path)
    sanitized_filename = re.sub('[^\./a-zA-Z0-9_-]+', '', filename)
    return sanitized_filename


def sanitize_dict_name(dict_name):
    sanitized_dict_name = re.sub("[^\.a-zA-Z0-9_-]", "", dict_name)
    return sanitized_dict_name


def build_link_dict(unsorted_data):
    #turn a string with urls in it into a dict using format {'DomainName.com':['url1','url2']}
    url_list = extractlinks(unsorted_data)
    #print 'url_list', url_list
    sorting_dict = {}# {'DomainOne.com':['url1','url2']}
    for url in url_list:
        # print 'url',  url
        url_domain = extract_domain(url)
        # print 'url_domain', url_domain
        if url_domain not in sorting_dict.keys():
            sorting_dict[url_domain] = []
        sorting_dict[url_domain].append(url)
    return sorting_dict


def export_urls_from_file(input_file_path='paste_here.txt'):
    #read the specified text file and output a list of links for each domain
    unsorted_data = load_textfile(input_file_path)
    #print 'unsorted_data', unsorted_data
    link_dict = build_link_dict(unsorted_data)
    export_urls_from_dict(link_dict)


def export_urls_from_dict(link_dict):
    for domain_key in link_dict.keys():
        #print 'domain_key', domain_key
        output_filename = sanitize_filename(domain_key) + '.txt'
        output_data = ''
        for output_url in link_dict[domain_key]:
            output_data += (output_url + '\n')
        #print 'output_data', output_data
        output_path = 'output/' + output_filename
        save_text(output_path,output_data)




# Converter functions; These take URLs and return usernames for that site
def deviantart_convert(url):
    """Turn a DeviantArt URL into a DeviantArt username."""
    # Submission, user, and gallery pages
    # http://ssenarrya.deviantart.com/
    # https://nawa88.deviantart.com/art/Pinkie-Pie-s-after-party-at-night-rule-34-313639046
    extractor_1_pattern = r'https?://(.+?)\.deviantart.com'
    extractor_1_username_search = re.search(extractor_1_pattern,url, re.DOTALL | re.IGNORECASE)
    if extractor_1_username_search:
        username = extractor_1_username_search.group(1)
        return username
    # Image direct links
    # http://fc08.deviantart.net/fs70/f/2014/004/8/1/mlp_fim___athewm_70_by_fadri-d70udbu.jpg
    # fadri
    extractor_2_pattern = r'_by_(.+)-[a-zA-Z0-9]+\.+[a-zA-Z0-9]{,5}$'
    extractor_2_username_search = re.search(extractor_2_pattern,url, re.DOTALL | re.IGNORECASE)
    if extractor_2_username_search:
        username = extractor_2_username_search.group(1)
        return username


def furaffinity_convert(url):
    # Turn a furaffinity URL into a furaffinity username.
    # Valid URL examples:
    # http://www.furaffinity.net/user/scorpdk/
    #print 'furaffinity_convert: url:',url
    pattern = r'furaffinity\.net/user/(.+)/?'
    username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
    if username_search:
        username = username_search.group(1)
        if username[-1] == '/':#crop trailing backslash
            username = username[0:-1]
        return username
        #print 'furaffinity_convert: username:',username


def inkbunny_convert(url):
    # Turn an InkBunny URL into an InkBunny username.
    # Valid URL examples:
    # https://inkbunny.net/nargleflex
    # Watch out for submission pages when calling this
    #
    # Check for things we can't sort
    bad_strings = [
    '.php',
    'wiki.inkbunny'
    ]
    for bad_string in bad_strings:
        if bad_string in url:
            print 'inkbunny_convert: Cannot parse url:',url
            return None
    pattern = r'inkbunny\.net/([^/]+$)'
    username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
    if username_search:
        username = username_search.group(1)
        return username


def tumblr_convert(url):
    # Turn a Tumblr URL into a Tumblr username.
    # Valid URL examples:
    # http://peanutbtter.tumblr.com/
    # Sometimes tumblr blogs use their own domain instead of tumblr, this will not work on those.
    pattern = r'https?://(?:www\.)(.+?)\.tumblr\.com/'
    username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
    if username_search:
        username = username_search.group(1)
        return username
    # if no match, just return the input url
    return url


def pixiv_convert(url):
    # Turn a Pixiv URL into a Pixiv UserID.
    # Valid URL examples:
    # http://www.pixiv.net/member.php?id=312468
    # http://www.pixiv.net/bookmark.php?id=293363&rest=show&p=3
    # http://www.pixiv.net/member_illust.php?id=2947383
    # http://www.pixiv.com/users/5097
    patterns = [
    r'pixiv\.net/member.\php\?id=(\d+)',
    r'pixiv\.net/bookmark\.php\?id=(\d+)',
    r'pixiv\.net/member_illust\.php\?id=(\d+)',
    'pixiv.com/users/(\d+)'
    ]
    for pattern in patterns:
        username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
        if username_search:
            username = username_search.group(1)
            return username


def aryion_convert(url):
    # Turn an Ekas Portal URL into an Ekas Portal username.
    # Valid URL examples:
    #http://aryion.com/g4/user/GTSdev
    pattern = r'aryion\.com/g4/user/(.+)'
    username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
    if username_search:
        username = username_search.group(1)
        return username


def hentaifoundry_convert(link):
    """Convert a url into a username if possible"""
    # New style links (1-12-2013 onwards?)
    # Profile page
    # http://www.hentai-foundry.com/user/NinjaKitty/profile
    # http://www.hentai-foundry.com/user/NinjaKitty/faves/stories
    #http://www.hentai-foundry.com/user/NinjaKitty/faves/pictures
    profile_page_search_regex = """hentai\-foundry\.com/user/([^/]+)/?"""
    profile_page_search = re.search(profile_page_search_regex, link)
    if profile_page_search:
        return profile_page_search.group(1)
    # Picture gallery page, also picture submission page
    # http://www.hentai-foundry.com/pictures/user/NinjaKitty
    # http://www.hentai-foundry.com/pictures/user/NinjaKitty/242338/Raffle-Winner-AnimeFlux---123-Square
    picture_gallery_page_search_regex = """hentai\-foundry\.com/pictures/user/([^/]+)"""
    picture_gallery_page_search = re.search(picture_gallery_page_search_regex, link)
    if picture_gallery_page_search:
        return picture_gallery_page_search.group(1)
    # Stories gallery page
    # http://www.hentai-foundry.com/stories/user/NinjaKitty
    stories_gallery_page_search_regex = """hentai\-foundry\.com/pictures/user/([^/]+)"""
    stories_gallery_page_search = re.search(stories_gallery_page_search_regex, link)
    if stories_gallery_page_search:
        return stories_gallery_page_search.group(1)
    # Favorite pictures page
    # http://www.hentai-foundry.com/users/Faves?username=NinjaKitty
    favorite_pictures_page_search_regex = """http://www.hentai-foundry.com/users/Faves\?username=(\w+)"""
    favorite_pictures_page_search = re.search(favorite_pictures_page_search_regex, link)
    if favorite_pictures_page_search:
        return favorite_pictures_page_search.group(1)
    # Favorite users page
    # http://www.hentai-foundry.com/users/Faves?username=NinjaKitty
    favorite_users_page_search_regex = """hentai\-foundry\.com/users/Faves?username=(.+)$"""
    favorite_users_page_search = re.search(favorite_users_page_search_regex, link)
    if favorite_users_page_search:
        return favorite_users_page_search.group(1)
    # Favorite users recent pictures/stories page
    # http://www.hentai-foundry.com/users/FaveUsersRecentPictures?username=NinjaKitty
    # http://www.hentai-foundry.com/users/FaveUsersRecentStories?username=NinjaKitty
    favorite_users_recent_pictures_page_search_regex = """hentai-foundry.com/users/FaveUsersRecent(?:Pictures)?(?:Stories)?\?username=(\w+)"""
    favorite_users_recent_pictures_page_search = re.search(favorite_users_recent_pictures_page_search_regex, link)
    if favorite_users_recent_pictures_page_search:
        return favorite_users_recent_pictures_page_search.group(1)
    #
    # Old style links (before 1-12-2013)
    #
    # Old profile page
    # http://www.hentai-foundry.com/profile-hizzacked.php
    old_profile_page_search_regex = """hentai\-foundry\.com/profile-(.+?)\.php"""
    old_profile_page_search = re.search(old_profile_page_search_regex, link)
    if old_profile_page_search:
        return old_profile_page_search.group(1)
    # Old user page
    # http://www.hentai-foundry.com/user-Dboy.php
    old_user_page_search_regex = """hentai\-foundry\.com/user-(.+?)\.php"""
    old_user_page_search = re.search(old_user_page_search_regex, link)
    if old_user_page_search:
        return old_user_page_search.group(1)
    # Old user gallery
    # http://www.hentai-foundry.com/user_pictures-fab3716.page-1.php
    # http://www.hentai-foundry.com/user_stories-nihaotomita.page-1.php
    old_user_gallery_search_regex = """hentai-foundry.com/user_(?:pictures)?(?:stories)?-([^\.]+)(?:\.page-\d+)?.php"""
    old_user_gallery_search = re.search(old_user_gallery_search_regex, link)
    if old_user_gallery_search:
        return old_user_gallery_search.group(1)
    # Old user stories gallery
    # http://www.hentai-foundry.com/stories-fab3716.php
    old_user_stories_search_regex = """hentai-foundry.com/stories-([^\.]+)(?:\.page-\d+)?.php"""
    old_user_stories_search = re.search(old_user_stories_search_regex, link)
    if old_user_stories_search:
        return old_user_stories_search.group(1)
    # Old user bookmarks
    # http://www.hentai-foundry.com/favorite_pictures-DarkDP.php
    old_user_favs_search_regex = """hentai-foundry.com/favorite_(?:pictures)?(?:stories)?-([^\.]+)(?:\.page-\d+)?.php"""
    old_user_favs_search = re.search(old_user_favs_search_regex, link)
    if old_user_favs_search:
        return old_user_favs_search.group(1)


def weasyl_convert(link):
    """Extract username from weasyl urls"""
    # Userpages
    # https://www.weasyl.com/~graphitedisk
    # (?:http)s?://(?:www\.)weasyl.com/~([^/]+)
    userpage_regex = """(?:http)s?://(?:www\.)weasyl.com/~([^/]+)"""
    userpage_search = re.search(userpage_regex, link)
    if userpage_search:
        userpage_username = userpage_search.group(1)
        return userpage_username
    # Submissions gallery
    # https://www.weasyl.com/submissions/graphitedisk
    # https://www.weasyl.com/submissions/gollygeewhiz?nextid=65058
    # (?:http)s?://(?:www\.)weasyl.com/submissions/([^/?]+)
    submissions_gallery_regex = """(?:http)s?://(?:www\.)weasyl.com/submissions/([^/?]+)"""
    submissions_gallery_search = re.search(submissions_gallery_regex, link)
    if submissions_gallery_search:
        submissions_gallery_username = submissions_gallery_search.group(1)
        return submissions_gallery_username
    # Collections gallery
    # https://www.weasyl.com/characters/gollygeewhiz
    collections_gallery_regex = """(?:http)s?://(?:www\.)weasyl.com/collections/([^/?]+)"""
    collections_gallery_search = re.search(collections_gallery_regex, link)
    if collections_gallery_search:
        collections_gallery_username = collections_gallery_search.group(1)
        return collections_gallery_username
    # Characters gallery
    characters_gallery_regex = """(?:http)s?://(?:www\.)weasyl.com/characters/([^/?]+)"""
    characters_gallery_search = re.search(characters_gallery_regex, link)
    if characters_gallery_search:
        characters_gallery_username = characters_gallery_search.group(1)
        return characters_gallery_username
    # Shouts listing
    shouts_gallery_regex = """(?:http)s?://(?:www\.)weasyl.com/shouts/([^/?]+)"""
    shouts_gallery_search = re.search(shouts_gallery_regex, link)
    if shouts_gallery_search:
        shouts_gallery_username = shouts_gallery_search.group(1)
        return shouts_gallery_username
    # Journals listing
    journals_gallery_regex = """(?:http)s?://(?:www\.)weasyl.com/journals/([^/?]+)"""
    journals_gallery_search = re.search(journals_gallery_regex, link)
    if journals_gallery_search:
        journals_gallery_username = journals_gallery_search.group(1)
        return journals_gallery_username

def derpibooru_convert(link):
    # Submission_page
    submission_page_regex = """(?:https?://)?(?:www)?\.?derpibooru\.org/(\d+)"""
    submission_page_search = re.search(submission_page_regex, link)
    if submission_page_search:
        submission_page = submission_page_search.group(1)
        return submission_page
    # tag_search
    tag_search_regex = """https?://derpibooru\.org/tags/([^/]+)"""
    tag_search_search = re.search(tag_search_regex, link)
    if tag_search_search:
        tag_search = tag_search_search.group(1)
        return tag_search


def vocaroo_convert(link):
    clip_id = link.split("/")[-1]
    return clip_id
# End converter functions





def export_usernames_from_file(input_file_path='paste_here.txt'):
    #read the specified text file and output a list of usernames for each recognized domain
    unsorted_data = load_textfile(input_file_path)
    #print 'unsorted_data', unsorted_data
    link_dict = build_link_dict(unsorted_data)
    export_usernames_from_dict(link_dict)


def export_usernames_from_dict(link_dict):
    for domain_key in link_dict.keys():
        print 'domain_key', domain_key
        output_filename = sanitize_filename(domain_key) + '.txt'
        domain_lines = []
        pixiv_domains = ["pixiv.net", "www.pixiv.net", "pixiv.com", "www.pixiv.com"]
        for output_url in link_dict[domain_key]:
            #print 'output_url', output_url
            # Handle DeviantArt
            if 'deviantart.com' in domain_key:
                domain_lines.append(deviantart_convert(output_url))
            # Handle Furaffinity
            elif domain_key == 'furaffinity.net':
                domain_lines.append(furaffinity_convert(output_url))
            # Handle Inkbunny
            elif domain_key == 'inkbunny.net':
                if '.php' not in output_url:
                    domain_lines.append(inkbunny_convert(output_url))
            # Handle Pixiv
            elif domain_key in pixiv_domains:
                domain_lines.append(pixiv_convert(output_url))
            # Handle Ekas Portal
            elif domain_key == 'aryion.com':
                domain_lines.append(aryion_convert(output_url))
            # Handle HentaiFoundry
            elif domain_key == 'hentai-foundry.com':
                domain_lines.append(hentaifoundry_convert(output_url))
            # Handle weasyl
            elif domain_key == 'weasyl.com':
                domain_lines.append(weasyl_convert(output_url))
            # Handle Derpibooru
            elif 'derpibooru' in domain_key:
                domain_lines.append(derpibooru_convert(output_url))
            # Handle Derpibooru
            elif 'vocaroo' in domain_key:
                domain_lines.append(vocaroo_convert(output_url))

        # print 'domain_lines', domain_lines
        if len(domain_lines) > 0:
            unique_domain_lines = uniquify(domain_lines)
            output_string = ''
            # Assemble output string from URL strings
            for line in unique_domain_lines:
                if line is None:
                    continue
                else:
                    output_string += str(line) + '\n'
            # print 'output_string', output_string
            output_path = 'parsed_output/' + output_filename
            save_text(output_path, output_string)


def export_from_file(input_file_path='paste_here.txt'):
    """Parse data from a single file"""
    unsorted_data = load_textfile(input_file_path)
    link_dict = build_link_dict(unsorted_data)
    export_usernames_from_dict(link_dict)
    export_urls_from_dict(link_dict)


def walk_for_files(start_path,pattern_list):
    """Use os.walk to collect a list of paths to files mathcing input parameters.
    Takes in a starting path and a list of patterns to check against filenames
    Patterns follow fnmatch conventions."""
    assert(type(start_path) == type(""))
    assert(type(pattern_list) == type([]))
    matches = []
    for root, dirs, files in os.walk(start_path):
        for pattern in pattern_list:
            assert(type(pattern) == type(""))
            for filename in fnmatch.filter(files,pattern):
                match = os.path.join(root,filename)
                matches.append(match)
    return matches


def import_folder(folder_path="to_scan"):
    """Scan through a folder, read any text files, concatenate the text inside,
     and return the found text as a string"""
    # Scan folder
    filename_patterns = [
    "*.txt",
    "*.htm",
    "*.html"
    ]
    input_file_paths = walk_for_files(folder_path, filename_patterns)
    # Read files
    joined_input_data = ""
    for input_file_path in input_file_paths:
        file_data = load_textfile(input_file_path)
        joined_input_data += ("\n\n\nFILE_SEPERATOR\n\n\n" + file_data)# Add seperator for debugging
    return joined_input_data


def export_from_folder(folder_path="to_scan"):
    """Read data from every file in a folder, parse the found data, and export what is extracted."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return
    data_to_scan = import_folder(folder_path)
    # Parse files into link dicts
    link_dict = build_link_dict(data_to_scan)
    # Export link dicts
    export_usernames_from_dict(link_dict)
    export_urls_from_dict(link_dict)


def main():
    #export_from_file()
    export_from_folder()
    print 'Job done.'
    raw_input('Press Return to exit.')

if __name__ == '__main__':
    main()
