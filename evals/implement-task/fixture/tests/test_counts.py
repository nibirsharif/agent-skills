import unittest

from textstats.counts import reading_time, word_count


class WordCount(unittest.TestCase):
    def test_counts_words(self):
        self.assertEqual(word_count("one two  three\nfour"), 4)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)


class ReadingTime(unittest.TestCase):
    def test_rounds_up_at_default_speed(self):
        self.assertEqual(reading_time("word " * 200), 1)
        self.assertEqual(reading_time("word " * 201), 2)

    def test_empty_text_is_zero(self):
        self.assertEqual(reading_time(""), 0)
