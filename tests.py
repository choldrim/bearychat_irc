#!/usr/bin/python3

import unittest

from bc_api import BC_API
from emojis import Emojis

class TestMethods(unittest.TestCase):

    @ unittest.skip("tmp")
    def test_get_all_robots(self):
        api = BC_API()
        api.login()
        api.get_all_robots()


    @ unittest.skip("tmp")
    def test_get_all_members(self):
        api = BC_API()
        api.login()
        api.get_all_members()


    @ unittest.skip("tmp")
    def test_get_ws_url(self):
        api = BC_API()
        api.login()
        ws_url = api.get_ws_url()
        import re
        r = re.compile("wss://bearychat.com/nimbus/ws:\w+")
        l = len(r.findall(ws_url))
        self.assertNotEqual(l, 0)


    def test_unicode_char_2_emoji_word(self):
        e = Emojis()
        word = e.unicode_char_2_emoji_word("😂")
        #print(word)
        self.assertEqual(word, "joy")


    def test_emoji_word_2_unicode_char(self):
        e = Emojis()
        c = e.emoji_word_2_unicode_char("smile")
        #print(c)
        self.assertEqual(c, "😄")


    def test_check_ascii(self):
        e = Emojis()
        rs = e.check_ascii("f")
        self.assertTrue(rs)

        rs = e.check_ascii("😈")
        self.assertFalse(rs)


    def test_check_chinese(self):
        e = Emojis()
        rs = e.check_chinese("中")
        self.assertTrue(rs)

        rs = e.check_chinese("😈")
        self.assertFalse(rs)

        rs = e.check_chinese("。")
        self.assertTrue(rs)


    def test_transfer_sentence_with_plain_word(self):
        e = Emojis()
        s_origin = "hi😈, what are you doing?😅"
        s_transfered = e.transfer_sentence_with_plain_word(s_origin)
        s_expected = "hi:smiling_imp:, what are you doing?:sweat_smile:"
        #print(s_transfered)
        self.assertEqual(s_transfered, s_expected)
        

    @unittest.skip("incomplete")
    def test_transfer_sentence_with_unicode_char(self):
        e = Emojis()
        s_origin = "hello, :blush: every one! :stuck_out_tongue_winking_eye:"
        s_transfered = e.transfer_sentence_with_unicode_char(s_origin)
        s_expected = "hello, 😊 every one! 😜"
        print(s_transfered)
        self.assertEqual(s_transfered, s_expected)


if __name__ == "__main__":
    unittest.main()
