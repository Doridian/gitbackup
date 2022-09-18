from host import GitHost
from host_loader import load_host, save_host
from config import GIT_HOSTS
from signals import safe_sleep, should_run

def main(one_shot: bool):
    hosts: list[GitHost] = []
    for name in GIT_HOSTS:
        host = load_host(name)
        hosts.append(host)
        print(f"# HOST LOADED [{host.name()}]", flush=True)

    print(f"# HOSTS LOADED [{len(hosts)}]", flush=True)

    while should_run():
        was_idle = True

        for host in hosts:
            did_refresh = host.refresh()
            did_pull = host.pull()
            if did_refresh or did_pull:
                save_host(host)
                print(f"# HOST {host.name()}", flush=True)
                was_idle = False

            if not should_run():
                return

        if one_shot:
            break

        if was_idle:
            safe_sleep(1)
