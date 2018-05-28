# -*- coding: utf-8 -*-
#
import os

def new_filename(data, file_kind, ext):
    '''Returns an available filename.

    :param file_kind: Name under which numbering is recorded, such as 'img' or
                      'table'.
    :type file_kind: str

    :param ext: Filename extension.
    :type ext: str

    :returns: (filename, rel_filepath) where filename is a path in the
              filesystem and rel_filepath is the path to be used in the tex
              code.
    '''

    nb_key = file_kind + 'number'
    if nb_key not in data.keys():
        data[nb_key] = 0

    # Make sure not to overwrite anything.
    file_exists = True
    while file_exists:
        data[nb_key] = data[nb_key] + 1
        name = data['base name'] + '-%03d%s' % (data[nb_key], ext)
        filename = os.path.join(data['output dir'], name)
        file_exists = os.path.isfile(filename)

    if data['rel data path']:
        rel_filepath = os.path.join(data['rel data path'], name)
    else:
        rel_filepath = name

    return filename, rel_filepath
