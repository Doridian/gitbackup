from gitbackup.main import main as gb_main
from gitbackup.signals import register_signals

def main():
    register_signals()
    gb_main(one_shot=False)

if __name__ == "__main__":
    main()
