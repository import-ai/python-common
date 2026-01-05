import re
import json as jsonlib
from functools import partial

json_dumps = partial(jsonlib.dumps, ensure_ascii=False, separators=(",", ":"))
continuous_break_line_pattern = re.compile(r"\n\n+")


def remove_continuous_break_lines(text: str) -> str:
    return continuous_break_line_pattern.sub("\n\n", text).strip() if text else ""
