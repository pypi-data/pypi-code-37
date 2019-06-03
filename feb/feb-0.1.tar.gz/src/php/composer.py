import json

from php.libmap import DataStore, LibMap
from util.output import Output
from util.urlhelper import URLHelper


class Composer(object):
    FILE_DEFAULT = './composer.json'
    PHP_VERSION_DEFAULT = '7.0.6'

    KEY_REQUIRE = 'require'
    KEY_REQUIRE_DEV = 'require-dev'
    KEY_REPOSITORIES = 'repositories'
    KEY_REPOSITORIES_URL = 'url'
    KEY_REPOSITORIES_TYPE = 'type'
    KEY_CONFIG = 'config'
    KEY_CONFIG_PLATFORM = 'platform'
    KEY_CONFIG_PLATFORM_PHP = 'php'

    @staticmethod
    def pre_check(name, url):
        if LibMap.get_uri(name, url) is None:
            Output.error(
                "We can't match between lib name and repo url, so:\n\n"
                "1. you should use -u/--url to point out the exactly match rule\n"
                "2. or add the relationship between name/repo-url to bellow config repo\n\n"
                "> https://git.xiaojukeji.com/fangjunda/cc/blob/master/feb/libmap.json",
                True
            )
            exit(1)

    @staticmethod
    def reveal(file):
        with open(file) as f:
            data = json.loads(f.read())
            return data

    @staticmethod
    def build_repo(data):
        if Composer.KEY_REPOSITORIES not in data or 0 == len(data[Composer.KEY_REPOSITORIES]):
            Output.notice("No repo in you composer.json")
            return DataStore.store

        if Composer.KEY_REQUIRE not in data and Composer.KEY_REQUIRE_DEV not in data:
            Output.notice("No require and require-dev in you composer.json")
            return DataStore.store

        Composer._fill_repo(data[Composer.KEY_REPOSITORIES])
        Composer._fill_require(data[Composer.KEY_REQUIRE_DEV], True)
        Composer._fill_require(data[Composer.KEY_REQUIRE])
        return DataStore.store

    @staticmethod
    def _fill_repo(repo):
        for item in repo:
            if Composer.KEY_REPOSITORIES_TYPE not in item or Composer.KEY_REPOSITORIES_URL not in item:
                Output.warn("Incomplete repo config {item}".format(item=json.dumps(item)))
                continue
            name = LibMap.get_name(item["url"])
            if name is None:
                Output.error("Mismatch name/repo_url by url: {url}".format(url=item["url"]))
                exit(0)
            DataStore.set(name, {"url": item["url"]})

    @staticmethod
    def _fill_require(require, dev=False):
        for name, version in require.items():
            if not version.startswith("dev-"):
                continue
            branch, as_version = version[4:].split(" as ")
            DataStore.set(name, {"branch": branch, "as_version": as_version, "dev": dev})

    @staticmethod
    def add(data, item):
        if Composer.KEY_REQUIRE not in data:
            data[Composer.KEY_REQUIRE] = {}
        if Composer.KEY_REPOSITORIES not in data:
            data[Composer.KEY_REPOSITORIES] = []

        data[Composer.KEY_REQUIRE][item["name"]] = "dev-{branch} as {as_version}".format(
            branch=item["branch"], as_version=item["as_version"]
        )
        data[Composer.KEY_REPOSITORIES].append({"type": item["type"], "url": item["url"]})
        return data

    @staticmethod
    def save(data, file, suffix=""):
        file += suffix
        if Composer.KEY_REPOSITORIES in data:
            data[Composer.KEY_REPOSITORIES] = Composer._clean_repeat_repo(data[Composer.KEY_REPOSITORIES])
        with open(file, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4))
        Output.notice("Update successfully, please check: {file}".format(file=file), True)

    @staticmethod
    def _clean_repeat_repo(repo):
        repo_tb = {}
        for item in repo:
            index = item["url"]
            if index in repo_tb:
                Output.notice("Clean repeat repo item: {item}".format(item=json.dumps(item)))
                continue
            repo_tb[item["url"]] = item

        return list(repo_tb.values())

    @staticmethod
    def set_php_version(data, version):
        if Composer.KEY_CONFIG not in data:
            data[Composer.KEY_CONFIG] = {}
        if Composer.KEY_CONFIG_PLATFORM not in data[Composer.KEY_CONFIG]:
            data[Composer.KEY_CONFIG][Composer.KEY_CONFIG_PLATFORM] = {}
        data[Composer.KEY_CONFIG][Composer.KEY_CONFIG_PLATFORM]["php"] = version
        return data

    @staticmethod
    def delete(data, item):
        if Composer.KEY_REQUIRE not in data or Composer.KEY_REQUIRE_DEV not in data:
            Output.error("No 'require' field in your composer.json", True)
            return data

        if Composer.KEY_REPOSITORIES not in data:
            Output.error("No 'repositories' field in your composer.json", True)
            return data

        data[Composer.KEY_REQUIRE] = Composer._delete_require(data[Composer.KEY_REQUIRE], item)
        data[Composer.KEY_REQUIRE_DEV] = Composer._delete_require(data[Composer.KEY_REQUIRE_DEV], item)
        data[Composer.KEY_REPOSITORIES] = Composer._delete_repo(data[Composer.KEY_REPOSITORIES], item)

        if len(data[Composer.KEY_REQUIRE]) <= 0:
            del data[Composer.KEY_REQUIRE]
            Output.notice("Delete empty require")

        if len(data[Composer.KEY_REQUIRE_DEV]) <= 0:
            del data[Composer.KEY_REQUIRE_DEV]
            Output.notice("Delete empty require-dev")

        if len(data[Composer.KEY_REPOSITORIES]) <= 0:
            del data[Composer.KEY_REPOSITORIES]
            Output.notice("Delete empty repositories")

        return data

    @staticmethod
    def _delete_require(require, item):
        if item["name"] in require:
            require[item["name"]] = item["version"]
            Output.notice("Act require[-dev] {name} to version {version}".format(
                name=item["name"], version=item["version"]
            ))
        return require

    @staticmethod
    def _delete_repo(repo_ls, item):
        result_ls = []
        for repo in repo_ls:
            if URLHelper.equal(repo["url"], item["url"]):
                Output.notice("Delete repo {name}".format(name=item["url"]))
                continue
            result_ls.append(repo)

        return result_ls
