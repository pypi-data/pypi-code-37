##############################################
#  2019. 05. 26 ConfigHelper 0.1v
#  Can use it to save or recall preferences from Python.
##############################################

import json, os

class ConfigHelper:
    def __init__(self, data=None):
        if isinstance(data, str):
            self._from_file_(data)
        elif isinstance(data, dict):
            self._from_dict_(data)
        elif isinstance(data, type):
            self._from_obj_(data())
        elif data is not None:
            self._from_obj_(data)

    def __str__(self):
        return self.toJSON()

    def _from_obj_(self, data):
        for key in list(vars(data).keys()):
            self.setValue(key, self.getValue(key, data))

    def _from_file_(self, data:str):
        with open(data) as data_file:    
            _data = json.load(data_file)
        self._from_dict_(_data)

    def _from_dict_(self, data:dict):
        for key in list(data.keys()):
            setattr(self, key, data[key])

    def _get_obj_(self, obj):
        if obj is None or isinstance(obj, str):
            obj = self
        return obj

    def _set_path_(self, path):
        path = path.replace("\\", "/")
        if path[0] != '/' and path[1] != ':':
            path = os.getcwd().replace("\\", "/") + "/" + path
        return path

    def _create_folder_(self, path):
        path = self._set_path_(path)
        if path[-1] == '/':
            path = path[0:len(path)-1]
        try:
            if os.path.isdir(path) is False:
                os.mkdir(path)
        except Exception as e:
            print("create Folder : ", e)
            repath = str(path).split("/")[-1]
            repath = str(path).split("/"+repath)[0]
            self._create_folder_(repath)
            self._create_folder_(path)
        if path[-1] is not '/':
            path = path+"/"
        return path

    def getValue(self, key, obj=None):
        obj = self._get_obj_(obj)
        return getattr(obj, key, None)

    def setValue(self, key, value, obj=None):
        obj = self._get_obj_(obj)
        setattr(obj, key, value)
    
    def newObject(self, cls):
        obj = self._get_obj_(cls())
        for key in list(vars(obj).keys()):
            if key in list(vars(self).keys()):
                self.setValue(key, self.getValue(key), obj)
        return obj

    def setObject(self, obj):
        obj = self._get_obj_(obj)
        for key in list(vars(obj).keys()):
            if key in list(vars(self).keys()):
                self.setValue(key, self.getValue(key), obj)

    def toDict(self):
        data = {}
        for key in list(vars(self).keys()):
            data.update({key:self.getValue(key)})
        return data
    
    def toJSON(self):
        return json.dumps(self.toDict(), indent='\t', sort_keys=True)
    
    def toFile(self, path):
        file_name = path.split("/")[-1]
        path = self._create_folder_(path.split(file_name)[0])
        with open(path+file_name, "w") as outfile:
            json.dump(self.toDict(), outfile, indent='\t', sort_keys=True)