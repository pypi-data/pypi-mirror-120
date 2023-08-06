"""Micropub clients (editors)."""

from understory import web
from understory.web import tx

__all__ = ["send"]


def send(properties, endpoint=None, h="entry", token=None):
    """Send a Micropub request to a Micropub server."""
    # TODO FIXME what's in the session?
    if endpoint is None:
        endpoint = tx.user.session["micropub_endpoint"]
    response = web.post(
        endpoint,
        headers={"Authorization": f"Bearer {token}"},
        json={"type": [f"h-{h}"], "properties": properties},
    )
    print(response.status)
    print(response.text)
    return response.location, response.links
