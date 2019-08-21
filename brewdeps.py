import subprocess
import json
import sys

def run_cmd(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE)
    return r.stdout.decode('utf-8')


def get_osx_version():
    _osx = {
        '10.14': 'mojave',
        '10.13': 'high_sierra',
        '10.12': 'sierra'
    }

    t = run_cmd(["sw_vers", "-productVersion"]).split(".")
    return _osx[".".join([t[0], t[1]])]


def get_dependencies(pkgname):
    urls = set()
    osx_version = get_osx_version()
    data = json.loads(run_cmd(["brew", "info", "--json", pkgname]))[0]
    urls.add(data["bottle"]["stable"]["files"][osx_version]["url"])

    for dep in data["dependencies"]:
        urls.update(frozenset(get_dependencies(dep)))
    return urls

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Use: {sys.argv[0]} <pkgname>")
        raise SystemExit(1)

    print(f"[+] Getting dependencies for package {sys.argv[1]}. This could take a while...")
    deps = get_dependencies(sys.argv[1])

    for url in deps:
        print(f"curl -O {url}")

    for url in deps:
        paths = url.split("/")
        print(f"brew install {paths[-1]}")
