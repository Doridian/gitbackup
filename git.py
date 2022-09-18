from genericpath import exists
from os import environ, makedirs
from subprocess import CalledProcessError, check_call, DEVNULL
from traceback import print_exc
from shutil import rmtree

class GitBackup:
    repo: str
    dir: str
    username: str
    password: str
    only_clone: bool

    def __init__(self, repo: str, dir: str, username: str, password: str, only_initial: bool) -> None:
        self.repo = repo
        self.dir = dir
        self.username = username
        self.password = password
        self.only_clone = only_initial

    def pull(self) -> bool:
        try:
            self._pull()
            return True
        except CalledProcessError:
            print_exc()
        return False

    def _pull(self) -> None:
        git_cmd = ["git", "-c", "credential.helper=", "-c", "credential.helper=!f() { printf \"username=${GIT_USER}\\npassword=${GIT_PASS}\"; }; f"]

        git_env = {"GIT_USER": self.username, "GIT_PASS": self.password, "PATH": environ["PATH"]}

        clone_ok_file = f"{self.dir}/clone_ok"

        if exists(clone_ok_file):
            if self.only_clone:
                return
            check_call(git_cmd + ["fetch", "--all"], cwd=self.dir, env=git_env, stdout=DEVNULL, stderr=DEVNULL)
            return

        rmtree(self.dir, ignore_errors=True)
        makedirs(self.dir, exist_ok=True)
        check_call(git_cmd + ["clone", "--mirror", self.repo, "."], cwd=self.dir, env=git_env, stdout=DEVNULL, stderr=DEVNULL)
        with open(clone_ok_file, "w") as fh:
            fh.write("Initial clone OK. Do not delete or edit this file!")
