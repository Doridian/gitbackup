from time import sleep
from host import GitHost
from host_loader import load_host, save_host
from config import GIT_HOSTS

def main(one_shot: bool):
    hosts: list[GitHost] = []
    for name in GIT_HOSTS:
        host = load_host(name)
        hosts.append(host)
        print(f"# HOST {host.name()}")

    print(f"# HOSTS LOADED [{len(hosts)}]")

    while True:
        for host in hosts:
            did_refresh = host.refresh()
            did_pull = host.pull()
            if did_refresh or did_pull:
                save_host(host)
                print(f"# HOST {host.name()}")

        if one_shot:
            break

        sleep(1)
