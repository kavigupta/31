import os

from appdirs import user_cache_dir
from permacache.locked_shelf import LockedShelf


def active_process_table():
    return LockedShelf(
        os.path.join(user_cache_dir("s31"), "active_process_table"),
        multiprocess_safe=True,
    )
