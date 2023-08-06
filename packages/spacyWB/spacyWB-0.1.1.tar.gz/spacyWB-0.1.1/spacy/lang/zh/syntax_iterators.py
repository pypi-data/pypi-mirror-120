# coding: utf8
from __future__ import unicode_literals
import re

from ...symbols import NOUN, PROPN, PRON


def noun_chunks(obj):
    """
    Detect base noun phrases from a dependency parse. Works on both Doc and Span.
    """
    #tags = {'ns', 'n', 'vn', 'nz', 'nr', 't', 'b', 'x', 'j', 'a', 'q', 'ng', 'eng'}
    tags = {'NNP', 'NN', 'JJ', 'SFN', 'NR', 'FW'}
    triggers = {'又名', '别名', '别称', '又称', '昵称'}
    doc = obj.doc  # Ensure works on both Doc and Span.

    np_label = doc.vocab.strings.add("NP")
    doc.is_parsed = True

    start_index_found = False
    hash_start_index_found = False
    en_start_index_found = False
    en_chunk_length = 0
    start_index = -1
    english_found = False
    for i, word in enumerate(obj):
        word_text = word.text

        # 1. Identify hash tag content
        if not hash_start_index_found and word_text == '#':
            start_index = i + 1
            if start_index < len(doc):
                curr_token = doc[start_index]
                if curr_token.is_space:
                    start_index_found = False
                    continue
                if curr_token.is_ascii and len(curr_token.text)>1:
                    english_found = True
            hash_start_index_found = True
            continue
        if hash_start_index_found:
            if word_text == '#':
                chunk_length = word.i - start_index
                end = word.i
                if end > start_index and chunk_length <= 5:
                    yield start_index, end, np_label
                hash_start_index_found = False
                start_index_found = False
                en_start_index_found = False
                en_chunk_length = 0
                start_index = -1
                english_found = False
            elif not _is_cjk(word_text) and not english_found:
                hash_start_index_found = False
                start_index = -1
            continue

        # ## 2. Identify English content
        if word.is_ascii and len(word_text) > 1 and not word.like_num and not word.is_punct:
            if not en_start_index_found and not start_index_found:
                start_index = i
                en_start_index_found = True
                start_index_found = True
            en_chunk_length += 1
            english_found = True
            continue
        if english_found:
            if word.is_space:
                next_index = i + 1
                if next_index < len(doc):
                    next_word = doc[next_index]
                    if next_word.is_ascii and len(next_word.text)>1:
                        en_chunk_length += 1
                        if next_index == len(doc) - 1 and start_index >= 0:
                            yield start_index, next_index+1, np_label
                            hash_start_index_found = False
                            start_index_found = False
                            en_start_index_found = False
                            en_chunk_length = 0
                            start_index = -1
                            english_found = False
                        continue
            elif start_index>=0:
                yield start_index, word.i, np_label
                hash_start_index_found = False
                start_index_found = False
                en_start_index_found = False
                en_chunk_length = 0
                start_index = -1
                english_found = False
                continue

        # if en_start_index_found:
        #     if word.is_punct:
        #         curr_index = word.i
        #         chunk_length = curr_index - start_index
        #         found_english = False
        #         if curr_index > start_index and chunk_length <= 6:
        #             yield start_index, curr_index, np_label
        #             found_english = True
        #         if curr_index + 1 == len(doc) and not found_english:
        #             yield start_index, curr_index + 1, np_label
        #         hash_start_index_found = False
        #         en_start_index_found = False
        #         en_chunk_length = 0
        #         start_index_found = False
        #         continue

        # 3. Found ending boundary: case 1
        if word.text in triggers:
            if start_index_found:
                if start_index >= 0:  # and word.i - start_index != 1:
                    if not _bad_token(word):
                        yield start_index, word.i, np_label
                start_index_found = False
                start_index = -1
                en_start_index_found = False
            continue

        # Found ending boundary: case 2
        if word.tag_ not in tags or _bad_token(word):
            if start_index_found:
                if word.i - start_index != 1 and start_index >= 0:
                    yield start_index, word.i, np_label
                start_index_found = False
                start_index = -1
                en_start_index_found = False
            continue

        # Here the starting boundary is found!
        if not start_index_found and not _bad_token(word):
            start_index_found = True
            start_index = i
        elif i == len(doc) - 1 and start_index >= 0:
            if not _bad_token(word):
                yield start_index, word.i + 1, np_label
            start_index_found = False
            start_index = -1
            en_start_index_found = False


def _is_cjk(text):
    if re.search("[\u4e00-\u9FFF]", text):
        return True
    elif text == 'の':
        return True
    return False

def _ascii_or_space(word):
    if word.is_ascii or word.is_space:
        return True
    return False

def _unigram_and_not_space(word):
    return len(word.text) == 1 and not word.is_space

def _bad_token(word):
    if word.is_stop or word.is_punct or word.pos_ == 'PUNCT' or word.shape_ == 'd':
        return True
    return False


SYNTAX_ITERATORS = {"noun_chunks": noun_chunks}
