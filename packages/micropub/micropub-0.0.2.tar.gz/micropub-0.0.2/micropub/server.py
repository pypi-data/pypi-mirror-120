"""A Micropub server."""

import pathlib
import random

import pendulum
import vobject
from understory import sql, web
# from understory.indieweb.util import discover_post_type
from understory.web import tx

# from ... import webmention

__all__ = ["get_config"]


class PostNotFoundError(Exception):
    """Post could not be found."""


model = sql.model(
    __name__,
    resources={
        "permalink": "TEXT UNIQUE",
        "version": "TEXT UNIQUE",
        "resource": "JSON",
    },
    deleted_resources={
        "permalink": "TEXT UNIQUE",
        "version": "TEXT UNIQUE",
        "resource": "JSON",
    },
    media={"mid": "TEXT", "sha256": "TEXT UNIQUE", "size": "INTEGER"},
    syndication={"destination": "JSON NOT NULL"},
)

# TODO supported_types = {"RSVP": ["in-reply-to", "rsvp"]}


def get_config():
    """"""
    syndication_endpoints = []
    # TODO "channels": generate_channels()}
    return {
        "q": ["category", "contact", "source", "syndicate-to"],
        "media-endpoint": f"https://{tx.host.name}/pub/media",
        "syndicate-to": syndication_endpoints,
        "visibility": ["public", "unlisted", "private"],
        "timezone": "America/Los_Angeles",
    }


def generate_vcard(nickname):
    """"""
    card = tx.pub.get_card(nickname)
    vcard = vobject.vCard()
    vcard.add("prodid").value = "-//Canopy//understory 0.0.0//EN"
    vcard.add("uid").value = card["uid"][0]
    vcard.add("fn").value = card["name"][0]
    return vcard.serialize()

    # TODO # TODO if identity["type"] == "identity":
    # TODO n = card.add("n")
    # TODO names = {}
    # TODO for name_type in ("prefix", "given", "additional",
    #                        "family", "suffix"):
    # TODO     if identity[name_type]:
    # TODO         names[name_type] = identity[name_type].split(";")
    # TODO n.value = vobject.vcard.Name(**names)
    # TODO # TODO else:
    # TODO # TODO     card.add("n")
    # TODO # TODO     card.add("org").value = [identity["name"]]

    # TODO # TODO card.add("nickname").value = identity["name"]
    # TODO card.add("sort_string").value = identity["sort_string"]

    # TODO for number, types in identity["telephones"]:
    # TODO     entry = card.add("tel")
    # TODO     entry.value = number
    # TODO     if types:
    # TODO         entry.params["TYPE"] = types

    # TODO for url, types in identity["websites"]:
    # TODO     entry = card.add("url")
    # TODO     entry.value = url
    # TODO     if types:
    # TODO         entry.params["TYPE"] = types

    # TODO try:
    # TODO     photo_id = identity["photos"][0]
    # TODO except IndexError:
    # TODO     pass
    # TODO else:
    # TODO     photo_data = \
    # TODO         canopy.branches["images"].photos.get_photo_data(id=photo_id)
    # TODO     photo = card.add("photo")
    # TODO     photo.value = photo_data
    # TODO     photo.encoding_param = "b"
    # TODO     photo.type_param = "JPEG"

    # item_index = 0
    # for vals in card.contents.values():
    #     for val in vals:
    #         if val.group:
    #             item_index = int(val.group[4:])

    # for related, types in get_relationships(identity["id"]):
    #     uri = "https://{}/identities/{}/{}.vcf".format(tx.host.name,
    #                                                related["identifier"],
    #                                                related["slug"])
    #     rel = card.add("related")
    #     rel.value = uri
    #     rel.params["TYPE"] = types
    #     for type in types:
    #         group_name = "item{}".format(item_index)
    #         rel_name = card.add("x-abrelatednames")
    #         rel_name.value = related["name"]
    #         rel_name.group = group_name
    #         rel_uri = card.add("x-aburi")
    #         rel_uri.value = uri
    #         rel_uri.group = group_name
    #         rel_type = card.add("x-ablabel")
    #         rel_type.value = "_$!<{}>!$_".format(type)
    #         rel_type.group = group_name
    #         item_index += 1


@model.control
def create(db, resource_type, **resource):
    """Create a resource."""
    for k, v in resource.items():
        if not isinstance(v, list):
            resource[k] = [v]
        flat_values = []
        for v in resource[k]:
            if isinstance(v, dict):
                if not ("html" in v or "datetime" in v):
                    v = dict(**v["properties"], type=[v["type"][0].removeprefix("h-")])
            flat_values.append(v)
        resource[k] = flat_values

    config = get_config()
    # TODO deal with `updated`/`drafted`?
    if "published" in resource:
        # TODO accept simple eg. published=2020-2-20, published=2020-2-20T02:22:22
        # XXX resource["published"][0]["datetime"] = pendulum.from_format(
        # XXX     resource["published"][0]["datetime"], "YYYY-MM-DDTHH:mm:ssZ"
        # XXX )
        # XXX published = resource["published"]
        pass
    else:
        resource["published"] = [
            {
                "datetime": web.utcnow().isoformat(),
                "timezone": config["timezone"],
            }
        ]
    published = pendulum.parse(
        resource["published"][0]["datetime"],
        tz=resource["published"][0]["timezone"],
    )

    resource["visibility"] = resource.get("visibility", ["public"])
    # XXX resource["channel"] = resource.get("channel", [])
    mentions = []
    urls = resource.pop("url", [])
    if resource_type == "card":
        slug = resource.get("nickname", resource.get("name"))[0]
        urls.insert(0, f"/pub/cards/{web.textslug(slug)}")
    elif resource_type == "feed":
        name_slug = web.textslug(resource["name"][0])
        try:
            slug = resource["slug"][0]
        except KeyError:
            slug = name_slug
        resource.update(uid=[slug if slug else name_slug])
        resource.pop("channel", None)
        # XXX urls.insert(0, f"/{slug}")
    elif resource_type == "entry":
        #                                         REQUEST URL
        # 1) given: url=/xyz                        => look for exact match
        #     then: url=[/xyz, /2021/3/5...]
        # 2) given: channel=abc, slug=foo           => construct
        #     then: url=[/2021/3/5...]
        # 3) given: no slug                         => only via permalink
        #     then: url=[/2021/3/5...]
        post_type = "article"  # TODO FIXME discover_post_type(resource)
        slug = None
        if post_type == "article":
            slug = resource["name"][0]
        elif post_type == "bookmark":
            mentions.append(resource["bookmark-of"][0])
        elif post_type == "like":
            mentions.append(resource["like-of"][0])
        elif post_type == "rsvp":
            mentions.append(resource["in-reply-to"][0])
        # elif post_type == "identification":
        #     identifications = resource["identification-of"]
        #     identifications[0] = {"type": "cite",
        #                           **identifications[0]["properties"]}
        #     textslug = identifications[0]["name"]
        #     mentions.append(identifications[0]["url"])
        # elif post_type == "follow":
        #     follows = resource["follow-of"]
        #     follows[0] = {"type": "cite", **follows[0]["properties"]}
        #     textslug = follows[0]["name"]
        #     mentions.append(follows[0]["url"])
        #     tx.sub.follow(follows[0]["url"])
        # TODO user indieauth.server.get_identity() ??
        # XXX author_id = list(tx.db.select("identities"))[0]["card"]
        # XXX author_id = get_card()tx.db.select("resources")[0]["card"]["version"]
        resource.update(author=[tx.origin])
    # elif resource_type == "event":
    #     slug = resource.get("nickname", resource.get("name"))[0]
    #     urls.insert(0, f"/pub/cards/{web.textslug(slug)}")
    #     # if resource["uid"] == str(web.uri(tx.host.name)):
    #     #     pass
    resource.update(url=urls, type=[resource_type])
    permalink_base = f"/{web.timeslug(published)}"

    def generate_trailer():
        letterspace = "abcdefghijkmnopqrstuvwxyz23456789"
        trailer = "".join([random.choice(letterspace) for i in range(2)])
        if trailer in ("bs", "ok", "hi", "oz", "lb"):
            return generate_trailer()
        else:
            return trailer

    while True:
        permalink = f"{permalink_base}/{generate_trailer()}"
        resource["url"].append(permalink)
        try:
            tx.db.insert(
                "resources",
                permalink=permalink,
                version=web.nbrandom(10),
                resource=resource,
            )
        except tx.db.IntegrityError:
            continue
        break

    web.publish("/recent", ".feed[-0:-0]", resource)
    for mention in mentions:
        web.enqueue(webmention.send, f"{tx.origin}{permalink}", mention)
    # TODO web.publish(mention, ".responses[-1:-1]", resource)
    # for subscriber in subscribers:
    #     web.enqueue(websub.publish)
    return permalink


@model.control
def read(self, url):
    """Return an entry with its metadata."""
    if not url.startswith(("http://", "https://")):
        url = f"/{url.strip('/')}"
    try:
        resource = tx.db.select(
            "resources",
            where="""json_extract(resources.resource, '$.url[0]') == ?""",
            vals=[url],
        )[0]
    except IndexError:
        resource = tx.db.select(
            "resources",
            where="""json_extract(resources.resource, '$.alias[0]') == ?""",
            vals=[url],
        )[0]
    r = resource["resource"]
    if "entry" in r["type"]:
        r["author"] = tx.identities.get_identity(r["author"][0])["card"]
    return resource


def update(self, url, add=None, replace=None, remove=None):
    """Update a resource."""
    permalink = f"/{url.strip('/')}"
    resource = tx.db.select("resources", where="permalink = ?", vals=[permalink])[0][
        "resource"
    ]
    if add:
        for prop, vals in add.items():
            try:
                resource[prop].extend(vals)
            except KeyError:
                resource[prop] = vals
    if replace:
        for prop, vals in replace.items():
            resource[prop] = vals
    if remove:
        for prop, vals in remove.items():
            del resource[prop]
    resource["updated"] = web.utcnow()
    tx.db.update(
        "resources", resource=resource, where="permalink = ?", vals=[permalink]
    )
    # TODO web.publish(url, f".{prop}[-0:-0]", vals)


@model.control
def delete(self, url):
    """Delete a resource."""
    resource = self.read(url)
    with tx.db.transaction as cur:
        cur.insert("deleted_resources", **resource)
        cur.delete("resources", where="permalink = ?", vals=[url])


@model.control
def search(self, query):
    """Return a list of resources containing `query`."""
    where = """json_extract(resources.resource,
                   '$.bookmark-of[0].url') == ?
               OR json_extract(resources.resource,
                   '$.like-of[0].url') == ?"""
    return tx.db.select("resources", vals=[query, query], where=where)


@model.control
def get_identity(self, version):
    """Return a snapshot of an identity at given version."""
    return self.get_version(version)


@model.control
def get_version(self, version):
    """Return a snapshot of resource at given version."""
    return tx.db.select("resources", where="version = ?", vals=[version])[0]


@model.control
def get_entry(self, path):
    """"""


@model.control
def get_card(self, nickname):
    """Return the card with given nickname."""
    resource = tx.db.select(
        "resources",
        vals=[nickname],
        where="""json_extract(resources.resource,
                                         '$.nickname[0]') == ?""",
    )[0]
    return resource["resource"]


@model.control
def get_event(self, path):
    """"""


@model.control
def get_entries(self, limit=20, modified="DESC"):
    """Return a list of entries."""
    return tx.db.select(
        "resources",
        order=f"""json_extract(resources.resource,
                                      '$.published[0]') {modified}""",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'entry'""",
        limit=limit,
    )


@model.control
def get_cards(self, limit=20):
    """Return a list of alphabetical cards."""
    return tx.db.select(
        "resources",  # order="modified DESC",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'card'""",
    )


@model.control
def get_rooms(self, limit=20):
    """Return a list of alphabetical rooms."""
    return tx.db.select(
        "resources",  # order="modified DESC",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'room'""",
    )


@model.control
def get_channels(self):
    """Return a list of alphabetical channels."""
    return tx.db.select(
        "resources",  # order="modified DESC",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'feed'""",
    )


@model.control
def get_categories(self):
    """Return a list of categories."""
    return [
        r["value"]
        for r in tx.db.select(
            "resources, json_each(resources.resource, '$.category')",
            what="DISTINCT value",
        )
    ]


@model.control
def get_posts(self):
    """."""
    for post in tx.db.select(
        "resources",
        where="""json_extract(resources.resource, '$.channel[0]') IS NULL AND
                 json_extract(resources.resource, '$.type[0]') != 'card'""",
        order="""json_extract(resources.resource, '$.published[0]') DESC""",
    ):
        r = post["resource"]
        if "entry" in r["type"]:
            r["author"] = tx.identities.get_identity(r["author"][0])["card"]
        yield r


@model.control
def get_posts_by_channel(self, uid):
    """."""
    return tx.db.select(
        "resources",
        vals=[uid],
        where="""json_extract(resources.resource,
                                     '$.channel[0]') == ?""",
        order="""json_extract(resources.resource,
                                     '$.published[0]') DESC""",
    )


# def get_channels(self):
#     """Return a list of channels."""
#     return [r["value"] for r in
#             tx.db.select("""resources,
#                            json_tree(resources.resource, '$.channel')""",
#                          what="DISTINCT value", where="type = 'text'")]


@model.control
def get_year(self, year):
    return tx.db.select(
        "resources",
        order="""json_extract(resources.resource,
                                     '$.published[0].datetime') ASC""",
        where=f"""json_extract(resources.resource,
                                      '$.published[0].datetime')
                                      LIKE '{year}%'""",
    )


@model.control
def get_media(self):
    """Return a list of media filepaths."""
    try:
        filepaths = list(pathlib.Path(tx.host.name).iterdir())
    except FileNotFoundError:
        filepaths = []
    return filepaths


@model.control
def get_filepath(self, filename):
    """Return a media file's path."""
    return pathlib.Path(tx.host.name) / filename
