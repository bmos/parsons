import re

__all__ = ["redact_credentials"]


def redact_credentials(sql):
    """
    Redact any credentials explicitly represented in SQL (e.g. COPY statement)
    """
    pattern = "credentials\\s+'(.+\n?)+[^(\\)]'"
    return re.sub(pattern, "CREDENTIALS REDACTED", sql, flags=re.IGNORECASE)
