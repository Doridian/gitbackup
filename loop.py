from time import sleep
from traceback import print_exc
from oneshot import main as oneshot_main

SLEEP_TIME = 24 * 60 * 60

def main():
    while True:
        try:
            oneshot_main()
        except Exception:
            print_exc()
        sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
