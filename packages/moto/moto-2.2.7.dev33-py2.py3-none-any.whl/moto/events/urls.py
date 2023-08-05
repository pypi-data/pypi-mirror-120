from __future__ import unicode_literals

from .responses import EventsHandler

url_bases = [r"https?://events\.(.+)\.amazonaws\.com"]

url_paths = {"{0}/": EventsHandler.dispatch}
