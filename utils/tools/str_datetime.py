from loguru import logger
import datetime
from typing import Optional


def convert(value: str, validator_name: str, format_str: str = "%Y-%m-%dT%H:%M:%S%z",
            alert: bool = True) -> Optional[datetime.datetime]:
    try:
        value = datetime.datetime.strptime(value, format_str)
    except (TypeError, ValueError) as e:
        if alert is True:
            logger.warning(f"[VALIDATION CONVERT] {validator_name}: " + str(e))
        else:
            pass
    else:
        return value
    return None
