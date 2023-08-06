import os
from typing import Dict, Tuple

import numpy as np
import pandas as pd

src_path = os.path.dirname(__file__)


def _to_dict(df: pd.DataFrame) -> Dict[str, int]:
    names = list(df["name"])
    counts = list(df["count"])
    return {names[i]: counts[i] for i in range(len(names))}


_first_df = pd.read_feather(os.path.join(src_path, "data/first_name.ft"))
_first_all_count = np.sum(_first_df["count"])
_first = _to_dict(_first_df)

_last_df = pd.read_feather(os.path.join(src_path, "data/last_name.ft"))
_last_all_count = np.sum(_last_df["count"])
_last = _to_dict(_last_df)


def _score(last: str, first: str) -> np.float64:
    first_count = _first[first] if first in _first.keys() else 0
    last_count = _last[last] if last in _last.keys() else 0
    return np.log((first_count + 1) / _first_all_count) + np.log((last_count + 1) / _last_all_count)


def split_name(name: str) -> Tuple[str, str]:
    candidates = [(name[:i], name[i:]) for i in range(1, len(name))]
    candidates += [(name[i:], name[:i]) for i in range(1, len(name))]
    scores = [_score(x, y) for x, y in candidates]
    if len(scores) == 0:
        return name, ""
    candidate = candidates[np.argmax(scores)]
    return candidate[0], candidate[1]
