from os.path import dirname, abspath, exists
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
    def __init__(self, base_filename: str, to_abs: bool = True):
        """
        Arguments:
        ----------
            base_filename {str} -- base file name

        Keyword Arguments:
        ------------------
            to_abs {bool} -- whether convert base file name to absolute path or not (default: True)
        """
        assert exists(base_filename)
        self.BASE_FILENAME = abspath(base_filename) if to_abs else base_filename

    def replace_extension(self, new_ext: str, post_text: Optional[str] = None) -> str:
        """ replace extension

        Arguments:
        ----------
            new_ext {str} -- new extension

        Keyword Arguments:
        ------------------
            post_text {Optional[str]} -- post text if you want

        Returns:
        --------
            {str} -- file name which extension is replaced
        """
        split = _split(self.BASE_FILENAME)
        base = _join(split[:-1]) + "{}.{}"
        return base.format("", new_ext) if post_text is None else base.format(post_text, new_ext)

    def add_post_text(self, post_text: str) -> str:
        """ add post text, without replacing extension

        Arguments:
        ----------
            post_text {str} -- post text

        Returns:
        --------
            {str} -- file name which post text is added
        """
        split = _split(self.BASE_FILENAME)
        return _join(split[:-1]) + post_text + f".{split[-1]}"

    @property
    def folder(self) -> str:
        """ get the folder name which contains base file

        Returns:
        --------
            {str} -- folder name
        """
        return dirname(self.BASE_FILENAME)

    @property
    def extension(self) -> str:
        """ get extension of base file

        Returns:
        --------
            {str} -- extension
        """
        return _split(self.BASE_FILENAME)[-1]
