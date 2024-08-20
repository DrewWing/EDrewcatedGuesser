#
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    print("python_settings.py should not be called as main!")


#import pathlib
import os

def get_var_value(line: str):
    return line[line.index("=")+1:-1]


class PythonSettings():
    def __init__(self):
        self.path_to_ftcapi = None
        self.debug_level = None
        self.event_code = None
        self.field_mode = None

        dir_path = str(os.path.dirname(os.path.realpath(__file__)))
        settings_path = str(
            dir_path + 
            ("\\" if "\\" in dir_path else "/") + # Accomodate forwardslash paths and backslash paths
            "settings.config"
        )
        
        # gather the settings from the settings.config file
        with open(settings_path,"r") as thefile:
            for line in thefile.readlines():
                if "path_to_ftcapi" in line:
                    self.path_to_ftcapi = get_var_value(line)
                
                if "event_code" in line:
                    self.event_code = get_var_value(line)
                
                if "debug_level" in line:
                    self.debug_level = int(get_var_value(line))
                
                if "field_mode" in line:
                    self.field_mode = bool(get_var_value(line))
        


        if (self.path_to_ftcapi == None or self.debug_level == None or self.event_code == None or self.field_mode == None):
            raise Warning("Some settings variable not found in settings.config! "+
                          f"path_to_ftcapi={self.path_to_ftcapi}  "+
                          f"debug_level={self.debug_level}  "+
                          f"event_code={self.event_code}  "+
                          f"field_mode={self.field_mode}"
                          )
        

if __name__ == "__main__":
    settings = PythonSettings()
    print(settings.debug_level)
    print(settings.event_code)
    print(settings.path_to_ftcapi)