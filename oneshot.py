from traceback import print_exc
from gh import GitHubBackup

def main():
    gh = GitHubBackup()

    contexts = gh.get_contexts()
    for context in contexts:
        print(f"Backing up {context.login}")
        try:
            gh.backup_context(context)
            print("Backup OK")
        except Exception:
            print_exc()

if __name__ == "__main__":
    main()
