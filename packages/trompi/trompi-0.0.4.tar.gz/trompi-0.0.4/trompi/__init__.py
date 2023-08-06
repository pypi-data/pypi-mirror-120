import importlib
import os
import sys
import urllib.request as urllib2

from pyspark.context import SparkContext
from pyspark.sql import SparkSession


class Trompi(object):

    _PYTHON_DIR_PATH = "./.dynamic_python_file_directory_from_file_service"
    _url = '127.0.0.1:8019'
    _base_directory_path = "."
    _spark = SparkSession.builder.getOrCreate()
    _sc = SparkContext.getOrCreate()
    _g = globals()
    @classmethod
    def register_globals(cls, g):
        cls._g = g
    @classmethod
    def register_file_service_(cls, url):
        cls._url = url
    @classmethod
    def register_base_directory_path(cls, path):
        cls._base_directory_path = path
    @classmethod
    def import_(cls, remote_file_path, import_member=False):
        file_name = remote_file_path.split("/")[-1]
        _s = file_name.split(".")
        assert _s.__len__() == 2
        assert _s[-1] == 'py'
        module_name = _s[0]
        local_file_path = f"{cls._PYTHON_DIR_PATH}/{file_name}"
        uri = f"{cls._url}/{cls._base_directory_path}/{remote_file_path}"
        
        if not os.path.exists(cls._PYTHON_DIR_PATH):
            os.mkdir(cls._PYTHON_DIR_PATH)
    
        if cls._PYTHON_DIR_PATH not in sys.path:
            sys.path.insert(0, cls._PYTHON_DIR_PATH)
        with open(local_file_path, 'w') as fw:
            with urllib2.urlopen(uri) as f:
                fw.write(f.read().decode())
        _g1 = globals()
        _g2 = cls._g
        _gs = [_g1, _g2]
        for _g in _gs:
            if module_name in _g:
                module = _g[module_name]
                importlib.reload(module)
            else:
                module = __import__(module_name)
                _g[module_name] = module
            # Not Recommend
            if import_member:
                for key, val in module.__dict__.items():
                    if not key.startswith('_'):
                        _g[key] = val

        cls._sc.addPyFile(local_file_path)

if __name__ == '__main__':
    Trompi.register_file_service_("http://127.0.0.1:8019/")
    Trompi.register_base_directory_path("trompi/test_remote_package")
    Trompi.import_("util.py")
