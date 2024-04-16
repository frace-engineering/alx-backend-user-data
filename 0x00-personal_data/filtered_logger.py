#!/usr/bin/env python3
"""
This module provides a function to obfuscate log messages.
"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns:
        str: The obfuscated log message.
    """
    regex_pattern = '|'.join([f'{fields}=([^;]+)' for field in fields])
    return re.sub(regex_pattern, '=' + redaction, message)
