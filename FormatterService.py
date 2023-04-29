class TextFormatter:
    width = 80

    @staticmethod
    def formate_text(text):
        result_text = ""
        for line in text.split("\n\n"):
            if len(line) >= TextFormatter.width:
                result_text += TextFormatter.formate_big_line(line)
            else:
                result_text += line
            result_text += "\n\n"
        return result_text

    @staticmethod
    def formate_big_line(big_line):
        res_line = ""
        len_line = 0
        for word in big_line.split():
            if len_line + len(word) > TextFormatter.width:
                res_line += "\n"
                len_line = 0
            res_line += word + " "
            len_line += len(word) + 1
        return res_line[: len(res_line) - 1]