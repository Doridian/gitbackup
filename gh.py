from dataclasses import dataclass
from traceback import print_exc
from typing import Union
from github import Github, AuthenticatedUser, NamedUser, Organization, Repository, PaginatedList
from os import environ
from itertools import chain

from git import GitBackup
from host import GitHost

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

    def refresh(self) -> bool:
        did_refresh = False

        id = "user:"
        if self.should_refresh(id):
            did_refresh = True
            print("+ USER")
            try:
                u = self._client.get_user()
                self.repos[id] = self._get_holders(u, u.get_repos(affiliation="owner"))
                self.report_refresh(id, True)
            except Exception:
                print_exc()
                self.report_refresh(id, False)
            print("- USER")

        for org in self._orgs:
            id = f"org:{org}"
            if not self.should_refresh(id):
                continue

            did_refresh = True
            print(f"+ ORG {org}")
            try:
                o = self._client.get_organization(org)
                self.repos[id] = self._get_holders(o, o.get_repos())
                self.report_refresh(id, True)
            except Exception:
                print_exc()
                self.report_refresh(id, False)
            print(f"- ORG {org}")

        return did_refresh

    def pull(self):
        did_pull = False
        for repo in chain(*self.repos.values()):
            if not self.should_pull(repo.url):
                continue
            did_pull = True

            success = self._pull_repository(repo)
            self.report_pull(repo.url, success)

        return did_pull

    def _pull_repository(self, holder: GitHubRepoHolder) -> bool:
        print(f"+ REPO {holder.login}/{holder.repo}")
        backup = GitBackup(
            repo=f"https://github.com/{holder.login}/{holder.repo}",
            dir=f"backups/github/{holder.login}/{holder.repo}",
            username="pat",
            password=self._token,
            only_initial=holder.only_clone,
        )
        success = backup.pull()
        print(f"- REPO {holder.login}/{holder.repo}")
        return success

    def name(*args) -> str:
        return "github"
