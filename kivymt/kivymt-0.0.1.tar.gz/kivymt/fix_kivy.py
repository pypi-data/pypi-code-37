'''Monkeypatching kivy for some minor bugs'''


# ----- kivy.lang.builder.BuilderBase.load_file -----


import kivy.lang.builder
import os


if os.name == 'nt': # Windows

    def BuilderBase_load_file(self, filename, file_encoding='utf-8', **kwargs):
        '''Insert a file into the language builder and return the root widget
        (if defined) of the kv file.

        :parameters:
            `rulesonly`: bool, defaults to False
                If True, the Builder will raise an exception if you have a root
                widget inside the definition.
            `file_encoding`: str, defaults to 'utf-8'
                the encoding of the file
        '''
        filename = kivy.lang.builder.resource_find(filename) or filename
        if __debug__:
            kivy.lang.builder.trace('Lang: load file %s' % filename)
        with open(filename, 'r', encoding=file_encoding) as fd:
            kwargs['filename'] = filename
            data = fd.read()

            # remove bom ?
            if kivy.lang.builder.PY2:
                if data.startswith((kivy.lang.builder.codecs.BOM_UTF16_LE, kivy.lang.builder.codecs.BOM_UTF16_BE)):
                    raise ValueError('Unsupported UTF16 for kv files.')
                if data.startswith((kivy.lang.builder.codecs.BOM_UTF32_LE, kivy.lang.builder.codecs.BOM_UTF32_BE)):
                    raise ValueError('Unsupported UTF32 for kv files.')
                if data.startswith(kivy.lang.builder.codecs.BOM_UTF8):
                    data = data[len(kivy.lang.builder.codecs.BOM_UTF8):]

            return self.load_string(data, **kwargs)


    kivy.lang.builder.BuilderBase._load_file = kivy.lang.builder.BuilderBase.load_file
    kivy.lang.builder.BuilderBase.load_file = BuilderBase_load_file
