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
import BeautifulSoup

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
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
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
    # Turn a DeviantArt URL into a DeviantArt username.
    # Valid URL examples:
    # http://ssenarrya.deviantart.com/
    # https://nawa88.deviantart.com/art/Pinkie-Pie-s-after-party-at-night-rule-34-313639046
    pattern = r'https?://(.+?)\.deviantart.com'
    username_search = re.search(pattern,url, re.DOTALL | re.IGNORECASE)
    if username_search:
        username = username_search.group(1)
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
    #http://www.pixiv.net/member.php?id=312468
    #http://www.pixiv.net/bookmark.php?id=293363&rest=show&p=3
    #http://www.pixiv.net/member_illust.php?id=2947383
    patterns = [
    r'pixiv\.net/member.\php\?id=(\d+)',
    r'pixiv\.net/bookmark\.php\?id=(\d+)',
    r'pixiv\.net/member_illust\.php\?id=(\d+)'
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

    # Favorite users page
    # http://www.hentai-foundry.com/users/Faves?username=NinjaKitty
    favorite_users_page_search_regex = """hentai\-foundry\.com/users/Faves?username=(.+)$"""
    favorite_users_page_search = re.search(favorite_users_page_search_regex, link)
    if favorite_users_page_search:
        return favorite_users_page_search.group(1)

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
    old_user_gallery_search_regex = """hentai-foundry.com/user_(?:pictures)?(?:stories)-([^\.]+)(?:\.page-\d+)?.php"""
    old_user_gallery_search = re.search(old_user_gallery_search_regex, link)
    if old_user_gallery_search:
        return old_user_gallery_search.group(1)

    # Old user stories gallery
    # http://www.hentai-foundry.com/stories-fab3716.php
    old_user_stories_search_regex = """hentai-foundry.com/stories-([^\.]+)(?:\.page-\d+)?.php"""
    old_user_stories_search = re.search(old_user_stories_search_regex, link)
    if old_user_stories_search:
        return old_user_stories_search.group(1)

    # If all extractors fail, assume already processed
    if "hentai-foundry.com" not in link:
        return link
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
        pixiv_domains = ["pixiv.net","www.pixiv.net"]
        for output_url in link_dict[domain_key]:
            #print 'output_url', output_url
            # Handle DeviantArt
            if domain_key == 'deviantart.com':
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
        # print 'domain_lines', domain_lines
        if len(domain_lines) > 0:
            unique_domain_lines = uniquify(domain_lines)
            output_string = ''
            # Assemble output string from URL strings
            for line in unique_domain_lines:
                output_string += str(line) + '\n'
            # print 'output_string', output_string
            output_path = 'parsed_output/' + output_filename
            save_text(output_path, output_string)

def export_from_file(input_file_path='paste_here.txt'):
    unsorted_data = load_textfile(input_file_path)
    link_dict = build_link_dict(unsorted_data)
    export_usernames_from_dict(link_dict)
    export_urls_from_dict(link_dict)


def main():
    export_from_file()
    print 'Job done.'
    raw_input('Press Return to exit.')

if __name__ == '__main__':
    main()
