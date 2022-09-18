from traceback import print_exc
from github import Github
from os import environ

from git import GitBackup

class GitHubBackup:
    def __init__(self):
        self.token = environ["GITHUB_TOKEN"]
        self.orgs = environ["GITHUB_ORGANIZATIONS"].split(",")
        self.client = Github(self.token)

    def get_contexts(self):
        contexts = [self.client.get_user()]
        for org in self.orgs:
            contexts.append(self.client.get_organization(org))

        return contexts

    def backup_context(self, ctx):
        outdir_base = f"backups/github/{ctx.login}"

        repos = None
        try: 
            repos = ctx.get_repos(affiliation="owner")
        except TypeError:
            repos = ctx.get_repos()

        for repo in repos:
            print(f"Backing up {ctx.login}/{repo.name}")
            backup = GitBackup(
                repo=f"https://github.com/{ctx.login}/{repo.name}",
                dir=f"{outdir_base}/{repo.name}",
                username="pat",
                password=self.token,
            )
            try:
                backup.run()
            except Exception:
                print_exc()
