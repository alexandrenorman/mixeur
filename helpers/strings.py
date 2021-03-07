# -*- coding: utf-8 -*-

import re
import unicodedata


def print_boxed(message):
    print("----------------------------------")
    print(message)
    print("----------------------------------")


def remove_diacritics(s):
    """
    Return string without diacritics (Épice => Epice)
    """
    return "".join(
        (c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    )


def soundex(word, language="fr"):
    if language == "en":
        lang_dict = [
            ("BFPV", "1"),
            ("CGJKQSXZ", "2"),
            ("DT", "3"),
            ("L", "4"),
            ("MN", "5"),
            ("R", "6"),
        ]
    elif language == "fr":
        lang_dict = [
            ("BP", "1"),
            ("CKQ", "2"),
            ("DT", "3"),
            ("L", "4"),
            ("MN", "5"),
            ("R", "6"),
            ("GJ", "7"),
            ("XZS", "8"),
            ("FV", "9"),
        ]
    else:
        return None

    sound = ""
    sound = word.replace(" ", "").upper()

    sound2 = sound[1:]
    for i in "AEIOUYHW":
        sound2 = sound2.replace(i, "")

    for letters in lang_dict:
        for c in letters[0]:
            sound2 = sound2.replace(c, letters[1])

    sound = sound[:1]
    for i in sound2:
        if i != sound[-1:]:
            sound = sound + i

    while len(sound) < 4:
        sound = sound + " "

    return sound[:4]


def truncate_html(string, length, ellipsis="…"):  # NOQA: C901
    """
    Truncate HTML string, preserving tag structure and character entities.
    """
    tag_end_re = re.compile(r"(\w+)[^>]*>")
    entity_end_re = re.compile(r"(\w+;)")

    length = int(length)
    output_length = 0
    i = 0
    pending_close_tags = {}

    while output_length < length and i < len(string):
        c = string[i]

        if c == "<":
            # probably some kind of tag
            if i in pending_close_tags:
                # just pop and skip if it's closing tag we already knew about
                i += len(pending_close_tags.pop(i))
            else:
                # else maybe add tag
                i += 1
                match = tag_end_re.match(string[i:])
                if match:
                    tag = match.groups()[0]
                    i += match.end()

                    # save the end tag for possible later use if there is one
                    match = re.search(
                        r"(</" + tag + "[^>]*>)", string[i:], re.IGNORECASE
                    )
                    if match:
                        pending_close_tags[i + match.start()] = match.groups()[0]
                else:
                    output_length += 1  # some kind of garbage, but count it in

        elif c == "&":
            # possible character entity, we need to skip it
            i += 1
            match = entity_end_re.match(string[i:])
            if match:
                i += match.end()

            # this is either a weird character or just '&', both count as 1
            output_length += 1
        else:
            # plain old characters

            skip_to = string.find("<", i, i + length)
            if skip_to == -1:
                skip_to = string.find("&", i, i + length)
            if skip_to == -1:
                skip_to = i + length

            # clamp
            delta = min(skip_to - i, length - output_length, len(string) - i)

            output_length += delta
            i += delta

    output = [string[:i]]
    if output_length == length:
        output.append(ellipsis)

    for k in sorted(pending_close_tags.keys()):
        output.append(pending_close_tags[k])

    return "".join(output)
