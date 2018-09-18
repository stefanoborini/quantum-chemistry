from django import shortcuts
from . import basecontext

def render(request):
    return shortcuts.render_to_response("application/runs.html", { "base" : basecontext.context(), })

