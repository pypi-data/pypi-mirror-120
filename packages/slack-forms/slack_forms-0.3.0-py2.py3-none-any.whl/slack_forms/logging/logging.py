import sys
import logging
import json_logging  # type: ignore


def getLogger(name):
    json_logging.init_non_web(enable_json=True)
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(sys.stdout))
    return log
