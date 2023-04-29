import os
import configparser

from FormatterService import TextFormatter


class FileManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.abspath("setting.conf"))
        self.main_dir = self.config["Main"]["save_folder"]
        TextFormatter.width = int(self.config["TextFormatter"]["width"])

    def save_text_page(self, url, text):
        basedir = self.main_dir + os.path.dirname(url[url.find("/") + 1:])
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        file_path = basedir + "/index.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as fp:
            new_text = TextFormatter.formate_text(text)
            fp.write(new_text)
            fp.close()

    def get_conf(self, service_name):
        return self.main_dir[service_name]