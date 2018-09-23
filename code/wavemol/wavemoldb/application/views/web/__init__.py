from django.shortcuts import render_to_response

import basecontext

from lib import logger

def render(request):
    log = logger.logger("wavemoldb")
    log.info('Connection')

    return render_to_response('application/index.html', { "base" : basecontext.context() }) 
