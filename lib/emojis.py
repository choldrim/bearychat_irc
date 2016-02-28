#!/usr/bin/python3

import json
import os

class Emojis:
    
    def __init__(self):
        self.cache = None
        emoji_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/emojis.json")
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


    def transfer_sentence_with_unicode_char(self, sentence, start=0):
        _sentence = []
        subsentence = sentence[start:]
        colon_count = subsentence.count(":")
        if colon_count >= 2:
            p1 = sentence.index(":", start)
            p2 = sentence.index(":", p1+1)
            emoji_word = sentence[p1+1:p2]
            emoji_u = self.emoji_word_2_unicode_char(emoji_word)
            if emoji_u:
                _sentence.append(sentence[:p1])
                _sentence.append(emoji_u)
                _sentence.append(sentence[p2+1:])
                _s = "".join(_sentence)
                return self.transfer_sentence_with_unicode_char(_s)
            else:
                # not an emoji word, skip the colon symbol
                return self.transfer_sentence_with_unicode_char(sentence, p2)

        else:
            return sentence

    def check_ascii(self, c):
        if ord(c) < 128 and ord(c) > 0:
            return True
        return False

    def check_chinese(self, c):
        # chinese word
        if ord(c) > 0x4e00 and ord(c) < 0x9fa5:
            return True

        # punctuation
        elif ord(c) > 0x3000 and ord(c) < 0x303f:
            return True

        return False


