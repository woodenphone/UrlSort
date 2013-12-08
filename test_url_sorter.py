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



class TestHentaiFoundryConvert2013(unittest.TestCase):
    # Profile
    def test_known_2013_profile(self):
        test_input= "http://www.hentai-foundry.com/user/NinjaKitty/profile"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    # Galleries
    def test_known_2013_picture_gallery(self):
        test_input= "http://www.hentai-foundry.com/pictures/user/NinjaKitty"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_picture_gallery_pg2(self):
        test_input= "http://www.hentai-foundry.com/pictures/user/NinjaKitty/page/2"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_stories_gallery(self):
        test_input= "http://www.hentai-foundry.com/pictures/user/NinjaKitty"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    # Favs
    def test_known_2013_picture_favs(self):
        test_input= "http://www.hentai-foundry.com/user/NinjaKitty/faves/pictures"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_picture_favs_recent(self):
        test_input= "http://www.hentai-foundry.com/users/FaveUsersRecentPictures?username=NinjaKitty"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_stories_favs(self):
        test_input= "http://www.hentai-foundry.com/user/NinjaKitty/faves/stories"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_stories_favs_recent(self):
        test_input= "http://www.hentai-foundry.com/users/FaveUsersRecentStories?username=NinjaKitty"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_2013_user_favs(self):
        test_input= "http://www.hentai-foundry.com/users/Faves?username=NinjaKitty"
        expected_result = "NinjaKitty"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)



class TestHentaiFoundryConvertOld(unittest.TestCase):
    def test_known_old_bookmarks(self):
        test_input= "http://www.hentai-foundry.com/favorite_pictures-DarkDP.php"
        expected_result = "DarkDP"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_old_stories_gallery_1(self):
        test_input= "http://www.hentai-foundry.com/stories-fab3716.php"
        expected_result = "fab3716"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_old_stories_gallery_2(self):
        test_input= "http://www.hentai-foundry.com/user_stories-nihaotomita.page-1.php"
        expected_result = "nihaotomita"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_old_user_page(self):
        test_input= "http://www.hentai-foundry.com/user-Dboy.php"
        expected_result = "Dboy"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_known_old_profile_page(self):
        test_input= "http://www.hentai-foundry.com/profile-hizzacked.php"
        expected_result = "hizzacked"
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

class TestHentaiFoundryConvertBadInput(unittest.TestCase):
    def test_empty_string(self):
        test_input= ""
        expected_result = ""
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    # Regex from development
    def test_dev_regex_1(self):
        test_input= "http://www.hentai-foundry\.com/\w+-\d+\.html"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_dev_regex_2(self):
        test_input= "http://www.hentai-foundry.com/pictures/user/([^/]+)"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_dev_regex_3(self):
        test_input= "http://www.hentai-foundry.com/user/([^/]+)/profile"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    # Login
    def test_login_page(self):
        test_input= "http://www.hentai-foundry.com/site/login"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_login_request(self):
        test_input= "http://www.hentai-foundry.com/site/login?YII_CSRF_TOKEN=ede775e6a6b0c0abe420c32e0e6069b4e7e1442f&LoginForm%5Busername%5D=foo&LoginForm%5Bpassword%5D=bar&LoginForm%5BrememberMe%5D=0&yt0=Login"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_site_root(self):
        test_input= "http://www.hentai-foundry.com"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_clickthrough_1(self):
        test_input= "http://www.hentai-foundry.com/enter_agree.php"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_clickthrough_2(self):
        test_input= "http://www.hentai-foundry.com/?enterAgree=1&size=1550"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_site_index(self):
        test_input= "http://www.hentai-foundry.com/site/index"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_fav_pictures_no_user(self):
        test_input= "http://www.hentai-foundry.com/favorite_pictures-"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_fav_stories_no_user(self):
        test_input= "http://www.hentai-foundry.com/favorite_stories-"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_user_stories_no_user(self):
        test_input= "http://www.hentai-foundry.com/user_stories-"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_user_pictures_no_user(self):
        test_input= "http://www.hentai-foundry.com/user_pictures-"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_user_scraps_no_user(self):
        test_input= "http://www.hentai-foundry.com/scraps-"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_old_picture_page(self):
        test_input= "http://www.hentai-foundry.com/pic-105917.html"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_old_story_page(self):
        test_input= "http://www.hentai-foundry.com/story-6431.html"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

    def test_old_story_chapter(self):
        test_input= "http://www.hentai-foundry.com/chapter-5972.html"
        expected_result = None
        result = hentaifoundry_convert(test_input)
        self.assertEqual(result, expected_result)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
