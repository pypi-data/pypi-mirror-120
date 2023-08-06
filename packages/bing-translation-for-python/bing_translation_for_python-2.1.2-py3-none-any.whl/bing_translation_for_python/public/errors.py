class TargetLanguageNotSupported(Exception):
    pass


class EmptyTextError(Exception):
    pass


class EqualTextLanguage(Exception):
    pass


class CannotFindToken(Exception):
    pass


class MaxLengthOver(Exception):
    pass
