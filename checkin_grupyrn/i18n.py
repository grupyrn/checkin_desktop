import gettext
import os

import pkg_resources

path = 'locale'  # always use slash
filepath = pkg_resources.resource_filename(__name__, path)

localedir = os.path.abspath(filepath)

pt = gettext.translation('messages', localedir=localedir, languages=['pt'], fallback=True)
pt.install()
# _ = lambda s: s