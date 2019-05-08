import click
from slugify import slugify

from ..utils import (
    make_url,
    make_request,
    create_post_content,
    read_credentials,
    get_authentication_header,
)
from ..settings import POSTS_SUFFIX


@click.command()
@click.argument("title")
@click.argument("markup")
@click.pass_obj
def add_post(options, title, markup):
    site_url = options.url
    timeout = options.timeout
    rest_url = make_url(site_url, POSTS_SUFFIX)
    last_post = make_request(method="get", url=rest_url, timeout=timeout)[0]
    click.echo(make_request(
        method="post",
        url=rest_url,
        timeout=timeout,
        headers=get_authentication_header(site_url),
        data={
            #"date": "",
            #"date_gmt", "",
            "slug": slugify(title),
            "status": "draft",
            #"password": None,
            "title": title,
            "content": create_post_content(site_url, markup),
            #"author": 3,
            #"excerpt": last_post["excerpt"],
            #"featured_media": last_post["featured_media"],
            #"comment_status": last_post["comment_status"],
            #"ping_status": last_post["ping_status"],
            #"format": last_post["format"],
            "meta": last_post["meta"],
            #"sticky": last_post["sticky"],
            "template": last_post["template"],
        },
    ))
