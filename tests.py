#!/usr/bin/python3
# coding=utf-8

import unittest

from bc_api import BC_API
from emojis import Emojis

class TestMethods(unittest.TestCase):

    def test_get_all_robots(self):
        api = BC_API()
        api.login()
        api.get_all_robots()


    def test_get_all_members(self):
        api = BC_API()
        api.login()
        api.get_all_members()


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
        # 1
        word = e.unicode_char_2_emoji_word("😂")
        self.assertEqual(word, "joy")

        # 2
        word = e.unicode_char_2_emoji_word("☺️")
        self.assertEqual(word, "relaxed")


    def test_emoji_word_2_unicode_char(self):
        e = Emojis()
        # 1
        c = e.emoji_word_2_unicode_char("smile")
        self.assertEqual(c, "😄")

        # 2
        c = e.emoji_word_2_unicode_char("relaxed")
        self.assertEqual(c, "☺️")


    def test_check_ascii(self):
        e = Emojis()
        # 1
        rs = e.check_ascii("f")
        self.assertTrue(rs)

        # 2
        rs = e.check_ascii("😈")
        self.assertFalse(rs)


    def test_check_chinese(self):
        e = Emojis()
        # 1
        rs = e.check_chinese("中")
        self.assertTrue(rs)

        # 2
        rs = e.check_chinese("😈")
        self.assertFalse(rs)

        # 3
        rs = e.check_chinese("☺")
        self.assertFalse(rs)

        # 4
        rs = e.check_chinese("。")
        self.assertTrue(rs)


    def test_transfer_sentence_with_plain_word(self):
        e = Emojis()
        # 1
        origin = "hi😈, what are you doing?😅"
        transfered = e.transfer_sentence_with_plain_word(origin)
        expected = "hi:smiling_imp:, what are you doing?:sweat_smile:"
        self.assertEqual(transfered, expected)

        # 2
        origin = "hello, how are you?☺"
        transfered = e.transfer_sentence_with_plain_word(origin)
        expected = "hello, how are you?:relaxed:"
        #self.assertEqual(transfered, expected)
        

    def test_transfer_sentence_with_unicode_char(self):
        e = Emojis()
        # 1
        origin = "hello, :blush: every one! :stuck_out_tongue_winking_eye:"
        transfered = e.transfer_sentence_with_unicode_char(origin)
        expected = "hello, 😊 every one! 😜"
        self.assertEqual(transfered, expected)

        # 2
        origin = "hello:xpp:::iixx:blush:exxx:blush,very one! :stuck_out_tongue_winking_eye::::xx::"
        #origin = "hello:xx:opx:blush:every one! :stuck_out_tongue_winking_eye:"
        transfered = e.transfer_sentence_with_unicode_char(origin)
        expected = "hello:xpp:::iixx😊exxx:blush,very one! 😜:::xx::"
        self.assertEqual(transfered, expected)

        # 3
        origin = "hello, how are you!:relaxed:"
        transfered = e.transfer_sentence_with_unicode_char(origin)
        expected = "hello, how are you!☺️"
        self.assertEqual(transfered, expected)


if __name__ == "__main__":
    unittest.main()
