from genericpath import exists
from os import environ, makedirs
from subprocess import check_call, DEVNULL


class GitBackup:
    def __init__(self, repo, dir, username, password):
        self.repo = repo
        self.dir = dir
        self.username = username
        self.password = password

    def run(self):
        git_cmd = ["git", "-c", "credential.helper=", "-c", "credential.helper=!f() { printf \"username=${GIT_USER}\\npassword=${GIT_PASS}\"; }; f"]

        git_env = {"GIT_USER": self.username, "GIT_PASS": self.password, "PATH": environ["PATH"]}

        if exists(f"{self.dir}/HEAD"):
            check_call(git_cmd + ["fetch", "--all"], cwd=self.dir, env=git_env, stdout=DEVNULL, stderr=DEVNULL)
            return

        makedirs(self.dir, exist_ok=True)
        check_call(git_cmd + ["clone", "--mirror", self.repo, "."], cwd=self.dir, env=git_env, stdout=DEVNULL, stderr=DEVNULL)
