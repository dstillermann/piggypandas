

class Cleanup:

    NONE: int = 0
    UPPER: int = 0x01
    LOWER: int = 0x02
    TITLE: int = 0x03
    _CASE_MASK: int = 0x03
    STRIP: int = 0x04
    WORDS: int = 0x08
    CASE_INSENSITIVE: int = UPPER | STRIP
    CASE_SENSITIVE: int = STRIP

    @staticmethod
    def cleanup(s: str, cleanup_mode: int = CASE_SENSITIVE) -> str:
        if not isinstance(s, str):
            s = str(s)

        case: int = cleanup_mode & Cleanup._CASE_MASK
        if case == Cleanup.UPPER:
            s = s.upper()
        elif case == Cleanup.LOWER:
            s = s.upper()
        elif case == Cleanup.TITLE:
            s = s.title()

        if (cleanup_mode & Cleanup.STRIP) != 0:
            s = s.strip()

        if (cleanup_mode & Cleanup.WORDS) != 0:
            s = " ".join(s.split())

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

