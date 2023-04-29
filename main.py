import re
import sys
from FileService import FileManager
from ParseService import ParserHTML


def is_valid_url(url):
    regex = re.compile(
        r'^https?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' 
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


if __name__ == '__main__':
    url = sys.argv[1]
    if is_valid_url(url):
        file_service = FileManager()
        parser = ParserHTML(url, file_service.config["ParserHTML"])
        parser.parse_page()
        file_service.save_text_page(url, parser.get_text())
        print("Ok")
    else:
        print("Incorrect url")
