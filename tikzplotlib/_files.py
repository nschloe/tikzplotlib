import pathlib


def _gen_filepath(data, nb_key, ext):
    name = data["base name"] + f"-{data[nb_key]:03d}{ext}"
    return pathlib.Path(data["output dir"]) / name


def new_filepath(data, file_kind, ext):
    """Returns an available filepath.

    :param file_kind: Name under which numbering is recorded, such as 'img' or
                      'table'.
    :type file_kind: str

    :param ext: Filename extension.
    :type ext: str

    :returns: (filepath, rel_filepath) where filepath is a path in the
              filesystem and rel_filepath is the path to be used in the tex
              code.
    """

    nb_key = file_kind + "number"
    if nb_key not in data.keys():
        data[nb_key] = -1

    data[nb_key] = data[nb_key] + 1
    filepath = _gen_filepath(data, nb_key, ext)
    if not data["override externals"]:
        # Make sure not to overwrite anything.
        file_exists = filepath.is_file()
        while file_exists:
            data[nb_key] = data[nb_key] + 1
            filepath = _gen_filepath(data, nb_key, ext)
            file_exists = filepath.is_file()

    if data["rel data path"]:
        rel_filepath = pathlib.Path(data["rel data path"]) / filepath
    else:
        rel_filepath = filepath.name

    rel_filepath_str = str(rel_filepath).replace("\\", "/")

    return filepath, rel_filepath, rel_filepath_str
