from datetime import timedelta

REFRESH_TIME_OK = timedelta(hours=24)
REFRESH_TIME_FAIL = timedelta(hours=1)
PULL_TIME_OK = timedelta(hours=1)
PULL_TIME_FAIL = timedelta(minutes=15)

GIT_HOSTS = ["github"]
