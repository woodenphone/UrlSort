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
    print 'save_text:filepath', filepath
    save_dir = os.path.dirname(filepath)
    print 'save_text:save_dir', save_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    f = open(filepath,'w')
    f.write(data)
    f.close()
    print 'save_text:Saved data to file', filepath

def extract_domain(url):
    #return the domain from given url
    print 'extract_domain:url', url
    full_domain = urlparse.urlparse(url).netloc
    print 'extract_domain:full_domain', full_domain
    # Handle known problem cases
    # DeviantArt.com
    if 'deviantart.com' in full_domain:
        short_domain = re.sub('.+deviantart.com', 'deviantart.com', full_domain)
        return short_domain
    # Tumblr.com
    elif '.tumblr.com' in full_domain:
        short_domain = re.sub('.+tumblr.com', 'tumblr.com', full_domain)
        return short_domain
    else:
        return full_domain


def sanitize_filename(filename):
    # Sanitize a filename (not a path)
    sanitized_filename = re.sub('[^\./a-zA-Z0-9_-]+', '', filename)
    return sanitized_filename

def build_link_dict(unsorted_data):
    #turn a string with urls in it into a dict using format {'DomainName.com':['url1','url2']}
    url_list = extractlinks(unsorted_data)
    print 'url_list', url_list
    sorting_dict = {}# {'DomainOne.com':['url1','url2']}
    for url in url_list:
        print 'url',  url
        url_domain = extract_domain(url)
        print 'url_domain', url_domain
        if url_domain not in sorting_dict.keys():
            sorting_dict[url_domain] = []
        sorting_dict[url_domain].append(url)
    return sorting_dict


def export_urls_from_file(input_file_path='paste_here.txt'):
    #read the specified text file and output a list of links for each domain
    unsorted_data = load_textfile(input_file_path)
    print 'unsorted_data', unsorted_data
    link_dict = build_link_dict(unsorted_data)
    for domain_key in link_dict.keys():
        print 'domain_key', domain_key
        output_filename = sanitize_filename(domain_key) + '.txt'
        output_data = ''
        for output_url in link_dict[domain_key]:
            output_data += (output_url + '\n')
        print 'output_data', output_data
        output_path = 'output/' + output_filename
        save_text(output_path,output_data)


def main():
    export_urls_from_file()

if __name__ == '__main__':
    main()
