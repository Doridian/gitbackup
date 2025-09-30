from datetime import timedelta
from os import getenv

HOST_BACKUP_DIR = getenv("BACKUP_ROOT", "./backups")
REFRESH_TIME_OK = timedelta(hours=24)
REFRESH_TIME_FAIL = timedelta(hours=1)
PULL_TIME_OK = timedelta(hours=1)
PULL_TIME_FAIL = timedelta(minutes=15)

GIT_HOSTS = ["github"]
