from main import main
from signals import register_signals

if __name__ == "__main__":
    register_signals()
    main(one_shot=False)
