from os import makedirs
from os.path import exists, join
from sys import stderr
from traceback import print_exc
from gitbackup.host import GitHost
from pickle import dump, load
from gitbackup.gh import GitHubBackup
from gitbackup.config import HOST_BACKUP_DIR

_host_registry = {}
def _register_host(host_type: type[GitHost]) -> None:
    _host_registry[host_type.name()] = host_type
_register_host(GitHubBackup)

def _host_pickle_file(name: str) -> str:
    host_dir = join(HOST_BACKUP_DIR, name)
    makedirs(host_dir, exist_ok=True)
    return join(host_dir, "state.pickle")

def new_host(name: str) -> GitHost:
    return _host_registry[name]()

def save_host(host: GitHost) -> None:
    pickle_file = _host_pickle_file(host.name())
    with open(pickle_file, "wb") as fh:
        dump(host, fh)

def load_host(name: str) -> GitHost:
    pickle_file = _host_pickle_file(name)
    if exists(pickle_file):
        try:
            with open(pickle_file, "rb") as fh:
                return load(fh)
        except Exception:
            print_exc(file=stderr)
            stderr.flush()
    return new_host(name)
