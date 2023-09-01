# noinspection PyClassHasNoInit
class Cleanup:

    NONE: int = 0
    UPPER: int = 0x01
    LOWER: int = 0x02
    TITLE: int = 0x03
    CASEFOLD: int = 0x04
    _CASE_MASK: int = 0x07
    STRIP: int = 0x08
    WORDS: int = 0x10
    _WHITESPACE_MASK: int = 0x18
    CASE_INSENSITIVE: int = CASEFOLD | STRIP
    CASE_SENSITIVE: int = STRIP

    @staticmethod
    def cleanup(s: str, cleanup_mode: int = CASE_SENSITIVE) -> str:
        if not isinstance(s, str):
            s = str(s)

        case_mode: int = cleanup_mode & Cleanup._CASE_MASK
        if case_mode == Cleanup.UPPER:
            s = s.upper()
        elif case_mode == Cleanup.LOWER:
            s = s.upper()
        elif case_mode == Cleanup.TITLE:
            s = s.title()
        elif case_mode == Cleanup.CASEFOLD:
            s = s.casefold()
        elif case_mode != 0:
            raise ValueError(f"bad cleanup/case mode {cleanup_mode}")

        whitespace_mode: int = cleanup_mode & Cleanup._WHITESPACE_MASK
        if whitespace_mode == Cleanup.STRIP:
            s = s.strip()
        elif whitespace_mode == Cleanup.WORDS:
            s = " ".join(s.split())
        elif whitespace_mode != 0:
            raise ValueError(f"bad cleanup/whitespace mode {cleanup_mode}")

        return s

    @staticmethod
    def eq(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) == Cleanup.cleanup(s2, cleanup_mode)

    @staticmethod
    def ne(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) != Cleanup.cleanup(s2, cleanup_mode)

    @staticmethod
    def gt(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) > Cleanup.cleanup(s2, cleanup_mode)

    @staticmethod
    def ge(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) >= Cleanup.cleanup(s2, cleanup_mode)

    @staticmethod
    def lt(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) < Cleanup.cleanup(s2, cleanup_mode)

    @staticmethod
    def le(s1: str, s2: str, cleanup_mode: int = CASE_SENSITIVE) -> bool:
        return Cleanup.cleanup(s1, cleanup_mode) <= Cleanup.cleanup(s2, cleanup_mode)

