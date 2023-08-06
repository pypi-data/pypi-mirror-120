import importlib
import os
import sys
import urllib.request as urllib2

from pyspark.context import SparkContext
from pyspark.sql import SparkSession
import inspect

class Trompi(object):

    _PYTHON_DIR_PATH = "./.dynamic_python_file_directory_from_file_service"
    _url = None
    _base_directory_path = '.'
  
    @classmethod
    def register_file_service_(cls, url):
        cls._url = url
    @classmethod
    def register_base_directory_path(cls, path):
        cls._base_directory_path = path

    @classmethod
    def register(cls, url, path="."):
        cls.register_file_service_(url)
        cls.register_base_directory_path(path)

    @classmethod
    def import_(cls, remote_file_path, import_member=False):
        file_name = remote_file_path.split("/")[-1]
        _s = file_name.split(".")
        assert _s.__len__() == 2
        assert _s[-1] == 'py'
        module_name = _s[0]
        if cls._url:
            
            local_file_path = f"{cls._PYTHON_DIR_PATH}/{file_name}"
            uri = f"{cls._url}/{cls._base_directory_path}/{remote_file_path}"
            
            if not os.path.exists(cls._PYTHON_DIR_PATH):
                os.mkdir(cls._PYTHON_DIR_PATH)
        
            if cls._PYTHON_DIR_PATH not in sys.path:
                sys.path.insert(0, cls._PYTHON_DIR_PATH)

            with open(local_file_path, 'w') as fw:
                with urllib2.urlopen(uri) as f:
                    fw.write(f.read().decode())
            
            SparkContext.getOrCreate().addPyFile(local_file_path)
        # Call the globals dictionary of the environment where the import_ is located
        _g = inspect.stack()[1][0].f_globals 
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

        

if __name__ == '__main__':
    Trompi.register_file_service_("http://127.0.0.1:8019/")
    Trompi.register_base_directory_path("trompi/test_remote_package")
    Trompi.import_("util.py")
