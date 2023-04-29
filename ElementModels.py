import re


class Element:
    total = 0
    is_hard_struct = False

    def __init__(self, tag, text, href=""):
        self.tag = tag
        self.text = self.clear_text(text)
        if href != "":
            self.text += f"[{href}]"
        Element.total += 1

    @staticmethod
    def clear_text(text):
        result = text.replace("\n", "").replace("\t", "")
        spec_symbols = re.findall(r"&\w+;", text)
        for spec_symbol in spec_symbols:
            result.replace(spec_symbol,"")
        return result


class IndentElement(Element):
    def __init__(self, tag):
        super(IndentElement, self).__init__(tag, "")
        self.text = "\n\n"
