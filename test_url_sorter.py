#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      new
#
# Created:     15/06/2013
# Copyright:   (c) new 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import unittest
from url_sorter import *

class TestExtract_Domain(unittest.TestCase):
    def test_overly_long_doamin(self):
        test_url = ("a" * 1000) + ".com"
        domain = extract_domain(test_url)
        self.assertTrue(len(domain) < 200)

    def test_asterisk_at_end_of_url(self):
        # Test to catch bug when asterisk is at end of a url
        test_tuples = [("http://askspotlight.tumblr.com*", "tumblr.com"), ("http://askspotlight.tumblr.com","tumblr.com")]
        for test_tuple in test_tuples:
            test_input = test_tuple[0]
            expected_result = test_tuple[1]
            result = extract_domain(test_input)
            self.assertEqual(result, expected_result)




class TestInkBunnyConvert(unittest.TestCase):
    def test_dot_php(self):
        test_tuples = [("https://inkbunny.net/submissionview.php?id=419422",None), ("https://inkbunny.net/watchlist_process.php?mode=watching&user_id=143254", None), ("https://inkbunny.net/submissionview.php?id=396311&page=3", None)]
        for test_tuple in test_tuples:
            test_input = test_tuple[0]
            expected_result = test_tuple[1]
            result = inkbunny_convert(test_input)
            self.assertEqual(result, expected_result)

    def test_user_pages(self):
        test_tuples = [("https://inkbunny.net/vdk", "vdk"), ("https://inkbunny.net/ButtercupSaiyan", "ButtercupSaiyan"), ("https://inkbunny.net/kevinsano", "kevinsano")]
        for test_tuple in test_tuples:
            test_input = test_tuple[0]
            expected_result = test_tuple[1]
            result = inkbunny_convert(test_input)
            self.assertEqual(result, expected_result)

    def test_front_page(self):
        test_tuples = [("https://inkbunny.net/", None), ("https://inkbunny.net", None), ("http://inkbunny.net", None)]
        for test_tuple in test_tuples:
            test_input = test_tuple[0]
            expected_result = test_tuple[1]
            result = inkbunny_convert(test_input)
            self.assertEqual(result, expected_result)



class TestPixivConvert(unittest.TestCase):
    def test_known_user_pages(self):
        test_tuples = [
        # User homepage
        ("http://www.pixiv.net/member.php?id=527046","527046")
        # User Gallery listing
        ,("http://www.pixiv.net/member_illust.php?id=2675947", "2675947")
        # User bookmarks listing
        ,("http://www.pixiv.net/bookmark.php?id=293363&rest=show&p=3", "293363")]
        for test_tuple in test_tuples:
            test_input = test_tuple[0]
            expected_result = test_tuple[1]
            result = pixiv_convert(test_input)
            self.assertEqual(result, expected_result)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
