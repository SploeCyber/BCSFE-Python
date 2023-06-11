from typing import Any
from aenum import NamedConstant  # type: ignore
import colored  # type: ignore
from bcsfe.core import locale_handler


class ColorHex(NamedConstant):
    GREEN = "#008000"
    G = GREEN
    RED = "#FF0000"
    R = RED
    DARK_YELLOW = "#D7C32A"
    DY = DARK_YELLOW
    BLACK = "#000000"
    BL = BLACK
    WHITE = "#FFFFFF"
    W = WHITE
    CYAN = "#00FFFF"
    C = CYAN
    DARK_GREY = "#A9A9A9"
    DG = DARK_GREY
    BLUE = "#0000FF"
    B = BLUE
    YELLOW = "#FFFF00"
    Y = YELLOW
    MAGENTA = "#FF00FF"
    M = MAGENTA
    DARK_BLUE = "#00008B"
    DB = DARK_BLUE
    DARK_CYAN = "#008B8B"
    DC = DARK_CYAN
    DARK_MAGENTA = "#8B008B"
    DM = DARK_MAGENTA
    DARK_RED = "#8B0000"
    DR = DARK_RED
    DARK_GREEN = "#006400"
    DGN = DARK_GREEN
    LIGHT_GREY = "#D3D3D3"
    LG = LIGHT_GREY

    @staticmethod
    def from_name(name: str) -> str:
        if name == "":
            return ""
        return getattr(ColorHex, name.upper())


class ColoredText:
    def __init__(self, string: str, end: str = "\n") -> None:
        string = string.replace("\\n", "\n")
        self.string = string
        self.end = end
        self.display(string)

    def display(self, string: str) -> None:
        text_data = self.parse(string)
        for i, (text, color) in enumerate(text_data):
            if i == len(text_data) - 1:
                text += self.end
            if color == "":
                print(text, end="")
            else:
                try:
                    fg = colored.fg(color)  # type: ignore
                except KeyError:
                    print(text, end="")
                    continue
                print(colored.stylize(text, fg), end="")  # type: ignore

    @staticmethod
    def localize(string: str, **kwargs: Any) -> "ColoredText":
        text = locale_handler.LocalManager().get_key(string)
        try:
            text = text.format(**kwargs)
        except TypeError:
            pass
        return ColoredText(text)

    def parse(self, txt: str) -> list[tuple[str, str]]:
        # example: "This is a <red>red</red> text"
        # output: [("This is a ", ""), ("red", "#FF0000"), (" text", "")]
        # example: "This is a <red>red</red> text with <green>green</green> text"
        # output: [("This is a ", ""), ("red", "#FF0000"), (" text with ", ""), ("green", "#00FF00"), (" text", "")]
        # example: "This is a <#FF0000>red</#FF0000> text with <#00FF00>green</#00FF00> text"
        # output: [("This is a ", ""), ("red", "#FF0000"), (" text with ", ""), ("green", "#00FF00"), (" text", "")]
        # example: "<red>This is a <white>white</white> red text</red>"
        # output: [("This is a ", "#FF0000"), ("white", "#FFFFFF"), (" red text", "#FF0000")]

        # allow escaping of < and > with \, so that \\<red\\> is not parsed as a color tag
        txt += "</>"
        output: list[tuple[str, str]] = []
        i = 0
        tags: list[str] = []
        inside_tag = False
        in_closing_tag = False
        tag_text = ""
        text = ""
        while i < len(txt):
            char = txt[i]
            if char == "\\":
                i += 1
                char = txt[i]
                text += char
                i += 1
                continue
            if tags:
                tag = tags[-1]
            else:
                tag = ""
            if char == ">" and inside_tag:
                inside_tag = False
                if not in_closing_tag:
                    tags.append(tag_text)
                if in_closing_tag:
                    in_closing_tag = False
                tag_text = ""
            if char == "<" and not inside_tag:
                inside_tag = True
                if text:
                    if not tag.startswith("#"):
                        try:
                            hex_code = ColorHex.from_name(tag)
                        except KeyError:
                            hex_code = tag
                    else:
                        hex_code = tag
                    output.append((text, hex_code))
                    text = ""
                    tag_text = ""
            if char == "/" and inside_tag:
                in_closing_tag = True
                if tags:
                    tags.pop()
            if not inside_tag and char != ">" and char != "<":
                text += char
            if inside_tag and char != "<" and char != ">":
                tag_text += char
            i += 1
        return output


class ColoredInput:
    def __init__(self, end: str = "") -> None:
        self.end = end

    def get(self, display_string: str) -> str:
        ColoredText(display_string, end=self.end)
        return input()

    def get_int(
        self,
        display_string: str,
        error_message: str = "<red>Please enter a valid number</>",
    ) -> int:
        while True:
            try:
                return int(self.get(display_string))
            except ValueError:
                ColoredText(error_message)

    def get_bool(
        self,
        display_string: str,
        true_string: str = "y",
        false_string: str = "n",
    ):
        while True:
            result = self.get(display_string).lower()
            if result == true_string:
                return True
            if result == false_string:
                return False