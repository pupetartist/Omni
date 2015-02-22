def ensure_extension(filename, extension):
    extension = '.%s' % extension
    if not filename.endswith(extension):
        filename += extension
    return filename
