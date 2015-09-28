#!/usr/bin/python3

import json
import os

class Emojis:
    
    def __init__(self):
        self.cache = None
        emoji_file = os.path.join(os.path.dirname(__file__), "emojis.json")
        with open(emoji_file) as fp:
            self.cache = json.load(fp)


    def unicode_char_2_emoji_word(self, c):
        for n, d in self.cache.items():
            _c = d.get("char")
            if c == _c:
                return n
        return ""


    def emoji_word_2_unicode_char(self, word):
        for n, d in self.cache.items():
            if n == word:
                return d.get("char")
        return ""


    def transfer_sentence_with_plain_word(self, sentence):
        _sentence = []
        for c in sentence:
            if not self.check_ascii(c) and not self.check_chinese(c):
                word = self.unicode_char_2_emoji_word(c)
                if word:
                    word = ":%s:" % word
                else:
                    # continue
                    word = c
                _sentence.append(word)
            else:
                _sentence.append(c)

        _sentence = "".join(_sentence)
        return _sentence


    def transfer_sentence_with_unicode_char(self, sentence):
        return sentence

        # incompleted
        _sentence = []
        items = sentence.split(":")
        i = 0
        for item in items:
            if i == 0:
                _sentence.append(item)
                i += 1
                continue
            if i == len(items) - 1:
                _sentence.append(item)
                break

        return _sentence


    def check_ascii(self, c):
        if ord(c) > 128 or ord(c) < 0:
            return False
        return True

    def check_chinese(self, c):
        if ord(c) > 40869 or ord(c) < 19968:
            return False
        return True


