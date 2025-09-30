from dataclasses import dataclass
from sys import stderr
from traceback import print_exc
from typing import Union
from github import Github, AuthenticatedUser, NamedUser, Organization, Repository, PaginatedList
from os import environ
from itertools import chain
from gitbackup.config import HOST_BACKUP_DIR

from gitbackup.git import GitBackup
from gitbackup.host import GitHost
from gitbackup.signals import should_run

@dataclass
class GitHubRepoHolder:
    repo: str
    login: str
    url: str
    only_clone: bool

class GitHubBackup(GitHost):
    _token: str
    _orgs: list[str]
    _client: Github

    repos: dict[str, list[Repository.Repository]]

    def __init__(self) -> None:
        super().__init__()
        self.repos = {}

    def _reload(self) -> None:
        super()._reload()
        self._token = environ["GITHUB_TOKEN"]
        self._orgs = environ["GITHUB_ORGANIZATIONS"].split(",")
        self._client = Github(self._token)
    
    @staticmethod
    def _get_holders(ctx: Union[AuthenticatedUser.AuthenticatedUser, NamedUser.NamedUser, Organization.Organization], repos: PaginatedList.PaginatedList) -> list[Repository.Repository]:
        return [GitHubRepoHolder(
            repo=repo.name,
            login=ctx.login,
            url=f"https://github.com/{ctx.login}/{repo.name}",
            only_clone=repo.archived,
        ) for repo in repos]

    def refresh(self, force: bool = False) -> bool:
        did_refresh = False

        known_repos: set[str] = set()

        id = "user:"
        known_repos.add(id)
        if force or self.should_refresh(id):
            did_refresh = True
            print("+ USER", flush=True)
            try:
                u = self._client.get_user()
                self.repos[id] = self._get_holders(u, u.get_repos(affiliation="owner"))
                self.report_refresh(id, True)
            except Exception:
                print_exc(file=stderr)
                stderr.flush()
                self.report_refresh(id, False)
            print("- USER", flush=True)

        for org in self._orgs:
            id = f"org:{org}"
            known_repos.add(id)

            if not should_run():
                return did_refresh

            if not force and not self.should_refresh(id):
                continue

            did_refresh = True
            print(f"+ ORG {org}", flush=True)
            try:
                o = self._client.get_organization(org)
                self.repos[id] = self._get_holders(o, o.get_repos())
                self.report_refresh(id, True)
            except Exception:
                print_exc(file=stderr)
                stderr.flush()
                self.report_refresh(id, False)
            print(f"- ORG {org}", flush=True)

        for id in list(self.repos.keys()):
            if id not in known_repos:
                del self.repos[id]
                did_refresh = True

        return did_refresh

    def pull(self, force: bool = False):
        did_pull = False
        for repo in chain(*self.repos.values()):
            if not should_run():
                break

            if not force and not self.should_pull(repo.url):
                continue
            did_pull = True

            success = self._pull_repository(repo)
            self.report_pull(repo.url, success)

        return did_pull

    def _pull_repository(self, holder: GitHubRepoHolder) -> bool:
        print(f"+ REPO {holder.login}/{holder.repo}", flush=True)
        backup = GitBackup(
            repo=f"https://github.com/{holder.login}/{holder.repo}",
            dir=f"{HOST_BACKUP_DIR}/github/{holder.login}/{holder.repo}",
            username="pat",
            password=self._token,
            only_initial=holder.only_clone,
        )
        success = backup.pull()
        print(f"- REPO {holder.login}/{holder.repo}", flush=True)
        return success

    def name(*args) -> str:
        return "github"
