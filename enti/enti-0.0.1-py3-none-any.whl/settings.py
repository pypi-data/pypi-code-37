from os import getenv, makedirs
from os.path import exists, join, dirname, realpath


class Config:
    DEBUG_ENABLED = getenv("ENTI_DEBUG_ENABLED", False)
    DEBUG_LEVEL = getenv("ENTI_DEBUG_ENABLED", 10)
    PROJECT_DIR = dirname(realpath(__file__))
    DATA_DIR = getenv("ENTI_DATA_DIR",join("/tmp", "enti", "data"))
    TMP_DIR = getenv("ENTI_TMP_DIR",join("/tmp", "enti", "tmp"))
    if not getenv("ENTI_DATA_DIR") and not exists(DATA_DIR):
        makedirs(DATA_DIR)
    if not getenv("ENTI_TMP_DIR") and not exists(TMP_DIR):
        makedirs(TMP_DIR)
    CORE_NLP_HOME = getenv(
        "CORE_NLP_HOME", join(DATA_DIR,"stanford-corenlp-full-2018-10-05")
    )
