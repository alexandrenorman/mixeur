# -*- coding: utf-8 -*-
import os
import unicodedata


def remove_diacritics(value):
    """
    Return string without diacritics (Épice => Epice)
    """
    return "".join(
        (
            c
            for c in unicodedata.normalize("NFD", value)
            if unicodedata.category(c) != "Mn"
        )
    )


def decode_base64_file(data):
    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if "data:" in data and ";base64," in data:
            # Break out the header from the base64 content
            header, data = data.split(";base64,")

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError("invalid_image")

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = f"{file_name}.{file_extension}"

        return ContentFile(decoded_file, name=complete_file_name)


def unique_filename_in_path(path, filename):
    """
    Return an unique filename in path.
    If file exists, add -number to base name
    file.txt -> file-1.txt -> file-2.txt
    """
    valid_filename = filename
    count = 0
    filepath = os.path.join(path, filename)
    while os.path.isfile(filepath):
        base, ext = os.path.splitext(filename)
        count += 1
        valid_filename = f"{base}-{count}{ext}"
        filepath = os.path.join(path, valid_filename)
    return valid_filename
