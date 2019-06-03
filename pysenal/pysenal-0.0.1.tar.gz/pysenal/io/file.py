# -*- coding: UTF-8 -*-
"""
io related utils functions
"""
import json
import os
from collections import Iterable
import configparser
from ..utils.logger import get_logger

_ENCODING_UTF8 = 'utf-8'

_LINE_BREAKS = '\n\v\x0b\f\x0c\x1c\x1d\x1e\x85\u2028\u2029'
_LINE_BREAK_TUPLE = tuple(_LINE_BREAKS)


def read_lines(filename, encoding=_ENCODING_UTF8, strip=False, skip_empty=False):
    """
    read lines in text file
    :param filename: file path
    :param encoding: encoding of the file, default is utf-8
    :param strip: whether strip every line, default is False
    :param skip_empty: whether skip empty line, when strip is False, judge after strip
    :return: lines
    """
    with open(filename, encoding=encoding) as f:
        if strip:
            if skip_empty:
                return [l.strip() for l in f.read().splitlines() if l.strip()]
            else:
                return [l.strip() for l in f.read().splitlines()]
        else:
            if skip_empty:
                lines = []
                for line in f.read().splitlines(True):
                    line = line.strip(_LINE_BREAKS)
                    if line:
                        lines.append(line)
                return lines
            else:
                return [l.strip(_LINE_BREAKS) for l in f.read().splitlines(True)]


def read_lines_lazy(src_filename, encoding=_ENCODING_UTF8):
    """
    use generator to load files, one line every time
    :param src_filename: source file path
    :param encoding: file encoding
    :return: lines in file
    """
    file = open(src_filename, encoding=encoding)
    for line in file:
        yield line
    file.close()


def read_file(filename, encoding=_ENCODING_UTF8):
    """
    wrap open function to read text in file
    :param filename: file path
    :param encoding: encoding of file, default is utf-8
    :return: text in file
    """
    with open(filename, encoding=encoding) as f:
        return f.read()


def write_file(filename, data, encoding=_ENCODING_UTF8):
    """
    write text into file
    :param filename: file path to save
    :param data: text data
    :param encoding: file encoding
    :return: None
    """
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)


def write_lines(filename, lines, encoding=_ENCODING_UTF8, filter_empty=False, strip=False):
    """
    write lines to file, will add line break for every line automatically
    :param filename: file path to save
    :param lines: lines to save
    :param encoding: file encoding
    :param filter_empty:
    :param strip:
    :return: None
    """
    if isinstance(lines, str):
        raise TypeError('line doesn\'t allow str format')

    if not isinstance(lines, Iterable):
        raise Exception('data can\'t be iterated')

    if strip:
        if filter_empty:
            lines = [l.strip() for l in lines if l.strip()]
        else:
            lines = [l.strip() for l in lines]
    else:
        if filter_empty:
            lines = [l for l in lines if l]

    if not lines:
        raise Exception('lines are empty')

    with open(filename, 'w', encoding=encoding) as f:
        f.write('\n'.join(lines) + '\n')


def read_json(src_filename):
    """
    read json file
    :param src_filename: source file path
    :return: loaded object
    """
    with open(src_filename, encoding=_ENCODING_UTF8) as f:
        return json.load(f)


def write_json(dest_filename, data, serialize_method=None):
    """
    dump json data to file, support non-UTF8 string (will not occur UTF8 hexadecimal code).
    :param dest_filename: destination file path
    :param data: data to be saved
    :param serialize_method: python method to do serialize method
    :return: None
    """
    with open(dest_filename, 'w', encoding=_ENCODING_UTF8) as f:
        if not serialize_method:
            json.dump(data, f, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False, default=serialize_method)


def read_jsonline(src_filename, encoding=_ENCODING_UTF8):
    """
    read jsonl file
    :param src_filename: source file path
    :param encoding: file encoding
    :return: object list, an object corresponding a line
    """
    file = open(src_filename, encoding=encoding)
    items = []
    for line in file:
        items.append(json.loads(line))
    file.close()
    return items


def read_jsonline_lazy(src_filename, encoding=_ENCODING_UTF8, default=None):
    """
    use generator to load jsonl one line every time
    :param src_filename: source file path
    :param encoding: file encoding
    :return: json object
    """
    if default is not None and not os.path.exists(src_filename):
        return default
    file = open(src_filename, encoding=encoding)
    for line in file:
        yield json.loads(line)
    file.close()


def write_jsonline(dest_filename, items, encoding=_ENCODING_UTF8):
    """
    write items to file with json line format
    :param dest_filename: destination file path
    :param items: items to be saved line by line
    :param encoding: file encoding
    :return: None
    """
    if isinstance(items, str):
        raise TypeError('json object list can\'t be str')

    if not dest_filename.endswith('.jsonl'):
        print('json line filename doesn\'t end with .jsonl')

    if not isinstance(items, Iterable):
        raise TypeError('items can\'t be iterable')
    file = open(dest_filename, 'w', encoding=encoding)
    for item in items:
        file.write(json.dumps(item, ensure_ascii=False) + '\n')
    file.close()


def read_ini(src_filename):
    """
    read configs in ini file
    :param src_filename: source file path
    :return: parsed config data
    """
    config = configparser.ConfigParser()
    config.read(src_filename)
    return config


def write_ini(dest_filename, config_data):
    """
    write config into file
    :param dest_filename: destination file
    :param config_data: config data
    :return: None
    """
    config = configparser.ConfigParser()
    for key, val in config_data.items():
        config[key] = val
    with open(dest_filename, 'w') as config_file:
        config.write(config_file)


def append_line(dest_filename, line, encoding=_ENCODING_UTF8):
    """
    append single line to file
    :param dest_filename: destination file path
    :param line: line string
    :param encoding: text encoding to save data
    :return: None
    """
    if not isinstance(line, str):
        raise TypeError('line is not in str type')
    with open(dest_filename, 'a', encoding=encoding) as f:
        f.write(line + '\n')


def append_lines(dest_filename, lines, remove_file=False, encoding=_ENCODING_UTF8):
    """
    append lines to file
    :param dest_filename: destination file path
    :param lines: lines to be saved
    :param remove_file: whether remove the destination file before append
    :param encoding: text encoding to save data
    :return:
    """
    if remove_file and os.path.exists(dest_filename):
        os.remove(dest_filename)
    for line in lines:
        append_line(dest_filename, line, encoding)


def append_jsonline(dest_filename, item, encoding=_ENCODING_UTF8):
    """
    append item as a line of json string to file
    :param dest_filename: destination file
    :param item: item to be saved
    :param encoding: file encoding
    :return: None
    """
    with open(dest_filename, 'a', encoding=encoding) as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def append_jsonlines(dest_filename, items, encoding=_ENCODING_UTF8):
    """
    append item as some lines of json string to file
    :param dest_filename: destination file
    :param items: items to be saved
    :param encoding: file encoding
    :return: None
    """
    with open(dest_filename, 'a', encoding=encoding) as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


class __BaseFile(object):
    """
    basic file abstract class, define read, write and append operations
    """

    def __init__(self, filename, encoding, is_remove=False):
        self.filename = filename
        self.encoding = encoding
        if is_remove not in {True, False}:
            print('')
        if is_remove and os.path.exists(filename):
            os.remove(filename)
        self._file = None
        self.logger = get_logger('IO')

    def read(self):
        self._to_read()

    def write(self, data):
        self._to_write()

    def append(self, data):
        self._to_append()

    def close(self):
        if self._file is not None and not self._file.closed:
            self._file.close()

    def __change_mode(self, mode):
        """
        change file mode of current file property in the object
        :param mode: new file mode
        :return:
        """
        if not self._file:
            self._file = open(self.filename, mode, encoding=self.encoding)
        elif mode == 'r' or self._file.mode != mode:
            self._file.close()
            self._file = open(self.filename, mode, encoding=self.encoding)

    def _to_read(self):
        self.__change_mode('r')

    def _to_write(self):
        self.__change_mode('w')

    def _to_append(self):
        self.__change_mode('a')

    def __del__(self):
        self.close()


class TextFile(__BaseFile):
    """
    define raw text operation
    """

    def __init__(self, filename, encoding=_ENCODING_UTF8, is_remove=False):
        super().__init__(filename, encoding, is_remove)

    def read(self):
        self._to_read()
        return self._file.read()

    def read_lines(self, skip_empty=False, strip=True):
        self._to_read()
        lines = []
        for line in self._file:
            if strip:
                line = line.strip()
            if skip_empty and not line:
                continue
            lines.append(line)
        return lines

    def write(self, data):
        self._to_write()
        self._file.write(data)

    def write_lines(self, lines):
        self._to_write()
        new_lines = []
        for line in lines:
            if not line.endswith(_LINE_BREAK_TUPLE):
                line += '\n'
            new_lines.append(line)
        self._file.writelines(new_lines)

    def append(self, data):
        self._to_append()
        self._file.write(data)

    def append_line(self, line):
        self._to_append()
        if not line.endswith('\n'):
            line += '\n'

    def append_lines(self, lines):
        self._to_append()
        for line in lines:
            if not line.endswith('\n'):
                line += '\n'
            self._file.write(line)


class JsonLineFile(TextFile):
    """
    define basic operation of jsonline file
    """

    def __init__(self, filename, encoding=_ENCODING_UTF8, is_remove=False):
        super().__init__(filename, encoding, is_remove)

    def read(self):
        return super().read()

    def read_line(self):
        self._to_read()
        for line in self._file:
            yield line

    def write(self, data):
        super().write(data)

    def write_line(self, item):
        self._to_write()
        self._file.write(self._to_string(item))

    def write_lines(self, lines):
        for line in lines:
            self.write_line(line)

    def append_line(self, line):
        self._to_append()
        self._file.append(self._to_string(line))

    def append_lines(self, lines):
        for line in lines:
            self.append_line(line)

    def _to_string(self, item, append_line_break=True):
        if not isinstance(item, str):
            item = json.dumps(item, ensure_ascii=False)
        if append_line_break and not item.endswith('\n'):
            item += '\n'
        return item
