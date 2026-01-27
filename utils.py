import re
import json as jsonlib
from functools import partial

json_dumps = partial(jsonlib.dumps, ensure_ascii=False, separators=(",", ":"))
continuous_break_line_pattern = re.compile(r"\n\n+")


def remove_continuous_break_lines(text: str) -> str:
    return continuous_break_line_pattern.sub("\n\n", text).strip() if text else ""


def remove_continuous_spaces(text: str) -> str:
    return re.sub(r"\s{2,}", " ", text).strip() if text else ""


def truncate_right(text: str, length: int = 20, with_dots: bool = True) -> str:
    if len(text) <= length:
        return text
    if with_dots and length > 3:
        return text[: length - 3] + "..."
    return text[:length]
