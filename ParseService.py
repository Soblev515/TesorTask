import re
import requests
from ElementModels import Element, IndentElement


def set_conf(config):
    ParserHTML.tags = [x.strip() for x in eval(config["tags"])]
    ParserHTML.skip_tags = [x.strip() for x in eval(config["skip_tags"])]


class ParserHTML:
    tags = []
    skip_tags = []

    def __init__(self, url, config=""):
        self.page = requests.get(url)
        self.url_data = re.search('(?P<scheme>http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*', url)
        self.cur_pos = 0
        self.data = []
        if config != "":
            set_conf(config)

    def parse_page(self):
        self.cur_pos = self.page.text.find("body")
        main_tag = ""
        count_item_save = 0
        href = ""
        tag = ""

        while self.cur_pos != len(self.page.text) and self.cur_pos != -1:
            end_block = self.page.text.find(">", self.cur_pos)
            element_config = self.page.text[self.cur_pos + 1:end_block]
            start_new_block = self.page.text.find("<", end_block)
            if tag in ParserHTML.tags and self.page.text.find(f"</{tag}>",
                                                              end_block) - start_new_block > 1 and main_tag == "":
                Element.is_hard_struct = True
                main_tag = tag
                count_item_save = Element.total
            tag = element_config.split()[0]
            if "/" + main_tag == tag:
                Element.is_hard_struct = False
                main_tag = ""
                if Element.total - count_item_save != 0:
                    self.data.append(IndentElement(tag))
            if tag in ParserHTML.skip_tags or any(x in element_config[len(tag):] for x in ParserHTML.skip_tags):
                self.cur_pos = self.page.text.find(f"</{tag}>", end_block)
                tag = ""
                continue
            elif tag == "a":
                href = self.get_href()
            if start_new_block - end_block > 1 and tag != "":
                self.data.append(Element(tag, self.page.text[end_block + 1:start_new_block], href=href))
                href = ""
            self.cur_pos = start_new_block

    def get_text(self):
        return "".join([data.text for data in self.data])

    def get_href(self):
        href_start = self.page.text.find("href=", self.cur_pos) + 6
        href_end = self.page.text.find("\"", href_start)
        href = self.page.text[href_start:href_end]
        if href[:4] != "http":
            href = self.url_data.group('scheme') + self.url_data.group('host') + self.url_data.group(
                'port') + href
        return href
