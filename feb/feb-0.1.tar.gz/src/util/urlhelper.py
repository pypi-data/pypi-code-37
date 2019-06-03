from util.output import Output


class URLHelper(object):
    @staticmethod
    def equal(url1, url2):
        uri1 = URLHelper.get_uri(url1)
        uri2 = URLHelper.get_uri(url2)

        return uri1 == uri2

    @staticmethod
    def get_uri(url):
        if url.startswith("git"):
            uri = URLHelper._parse_git_url(url)
        elif url.startswith("https"):
            uri = URLHelper._parse_https_url(url)
        elif url.startswith("http"):
            uri = URLHelper._parse_http_url(url)
        else:
            uri = url

        if uri.endswith(".git"):
            uri = uri[:-4]

        Output.debug("Reveal uri: {i} -- {o}".format(i=url, o=uri))
        return uri

    @staticmethod
    def _parse_https_url(url):
        """https://xxxx/xx/xx.git"""
        _, uri = url[len("https://"):].split("/", 1)
        return uri

    @staticmethod
    def _parse_http_url(url):
        """http://xxxx/xx/xx.git"""
        _, uri = url[len("http://"):].split("/", 1)
        return uri

    @staticmethod
    def _parse_git_url(url):
        _, uri = url.split(":", 1)
        return uri
