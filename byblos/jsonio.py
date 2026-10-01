"""Unambiguous finite JSON at every file ingestion boundary."""
import json
import math
from pathlib import Path


def loads(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field: ' + key)
            result[key] = value
        return result

    def constant(value):
        raise ValueError('Nonfinite JSON number: ' + value)

    def number(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError('Nonfinite JSON number: ' + value)
        return parsed

    return json.loads(text, object_pairs_hook=unique, parse_constant=constant, parse_float=number)


def read_json(path):
    return loads(Path(path).read_text(encoding='utf-8'))
