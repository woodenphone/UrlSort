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
    soup = BeautifulSoup.BeautifulSoup(html)
    print 'soup', soup
    anchors = soup.findAll('a')
    print 'anchors', anchors
    links = []
    for a in anchors:
        links.append(a['href'])
    return links

def find_url_domain(domain_query):
    # Return the domain from a url string
    domain = urlparse.urlparse(domain_query)
    return domain

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

def save_text(path,data):
    f = open(path,'wu')
    f.write(data)
    f.close()



def sanitize_filename(filename):
    # Sanitize a filename (not a path)
    sanitized_filename = re.sub('[^\./a-zA-Z0-9_-]+', '', filename)
    return sanitzed_filename


def main():
    pass
    unsorted_data = load_textfile('paste_here.txt')
    print 'unsorted_data', unsorted_data
    url_list = extractlinks(unsorted_data)
    print 'url_list', url_list
    sorting_dict = {}# {'DomainOne.com':['url1','url2']}
    for url in url_list:
        print 'url',  url
        url_domain = find_url_domain(url)
        if url_domain not in sorting_dict.keys():
            sorting_dict[url_domain] = []
        sorting_dict[url_domain].append(url)
    for domain_key in sorting_dict.keys():
        print 'domain_key', domain_key
        output_filename = sanitize_filename(domain_key)
        output_data = ''
        for output_url in sorting_dict[domain_key]:
            output_data += (output_url + '\n')
        print 'output_data', output_data








if __name__ == '__main__':
    main()
