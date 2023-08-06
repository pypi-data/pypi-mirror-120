from typing import Optional, List


def _split(text: str) -> List[str]:
    return text.split(".")


def _join(texts: List[str]) -> str:
    return ".".join(texts)


class ExtensionConvertor:
    """ExtensionConvertor can replace file extension to a new specified one.

    Examples:
    ---------
        >>> conv = ExtensionConvertor("hoge.jpg")
        >>> conv.replace_extension("pdf")
        hoge.pdf
        >>> conv.replace_extension("pdf", "_sub")
        hoge_sub.pdf
        >>> conv.add_post_text("_hoge")
        hoge_hoge.jpg
    """
    def __init__(self, base_filename: str):
        self.BASE_FILENAME = base_filename

    def replace_extension(self, new_ext: str, post_text: Optional[str] = None) -> str:
        split = _split(self.BASE_FILENAME)
        base = _join(split[:-1]) + "{}.{}"
        return base.format("", new_ext) if post_text is None else base.format(post_text, new_ext)

    def add_post_text(self, post_text: str) -> str:
        split = _split(self.BASE_FILENAME)
        return _join(split[:-1]) + post_text + f".{split[-1]}"
