import json
import requests


baseurl = "https://api.github.com"


class Entry:
    def __init__(self, args):
        self.__dict__.update(args)

    def __repr__(self):
        return f"Entry< path='{self.path}' type='{self.type}' size={self.size} url='{self.download_url}' >"


def _getheaders(auth):
    headers = {"User-Agent": "pygg" if auth is None else auth[0]}
    return headers


def getfolder(url, auth=None):

    headers = _getheaders(auth)
    with requests.get(url, auth=auth, headers=headers) as r:

        if r.status_code != 200:
            raise Exception("can not load data", url, r.headers)

        raw = r.content
        body = raw.decode()
        data = json.loads(body)

        all = {}

        for entry in data:
            if isinstance(entry, str):
                raise Exception(data, r.headers)

            e = Entry(entry)
            all[e.path] = e

        return all


def getfolders(repourl, auth=None):

    all = {}
    entries = getfolder(repourl, auth=auth)

    for path, entry in entries.items():

        if entry.type == "dir":
            sub = getfolders(entry.url, auth=auth)
            all.update(sub)
        else:
            all[path] = entry

    return all


def download_file(url, dest=None, auth=None):
    try:
        headers = _getheaders(auth)

        with requests.get(url, auth=auth, headers=headers) as r:

            if r.status_code != 200:
                print(r.url)
                raise Exception("can not load data", url, r.status_code, r.headers)

            data = r.content

            if dest != None:
                with open(dest, "wb") as f:
                    f.write(data)

                    return True
            else:
                return data

    except Exception as ex:
        print("error: ", ex)

    return False if dest != None else None


def download_json(url, dest=None, auth=None):
    content = download_file(url, auth=auth)
    o = json.loads(content)
    if dest != None:
        with open(dest, "w") as f:
            f.write(json.dumps(o, indent=4))
    return o


def getallpages(url, auth):

    page = 1
    elems = []

    while True:

        try:

            repourl = f"{url}?page={page}"

            print("download page", page)
            o = download_json(repourl, auth=login)

            if len(o) == 0:
                break

            elems.extend(o)

            page += 1

        except Exception as ex:
            print("error: ", ex)
            raise

    return elems


def sort_name(olist, skey=None):
    if skey == None:
        skey = "name"
    olist.sort(key=lambda x: x[skey].lower())


def getrepos(auth, dest=None):

    repourl = f"{baseurl}/user/repos"

    repos = getallpages(repourl, auth)

    sort_name()

    if dest != None:
        with open(dest, "w") as f:
            f.write(json.dumps(repos, indent=4))

    print("repos", len(repos))

    return repos


def getrepo(repo, auth, owner=None, dest=None):

    if owner == None:
        owner = auth[0]

    repourl = f"{baseurl}/repos/{owner}/{repo}"

    o = download_json(repourl, auth=login, dest=dest)

    return o


def getcontents(repo, auth, dest=None):

    name = repo["name"]
    owner = repo["owner"]["login"]

    repourl = f"https://api.github.com/repos/{owner}/{name}/contents/"
    o = download_json(repourl, auth=login, dest=dest)

    sort_name(o)

    return o
