from django.http.response import HttpResponsePermanentRedirect
from urllib.parse import urlsplit, urlunsplit
from .models import Podcast


def podcast_domain_middleware(get_response):
    def middleware(request):
        scheme, domain, path, querystring, fragment = urlsplit(
            request.build_absolute_uri()
        )

        if domain.startswith('www.'):
            return HttpResponsePermanentRedirect(
                urlunsplit(
                    (
                        scheme,
                        domain[4:],
                        path,
                        querystring,
                        fragment
                    )
                )
            )

        for podcast in Podcast.objects.filter(
            domain=domain
        ):
            request.urlconf = 'pico.podcasts.urls'
            request.podcast = podcast

        return get_response(request)

    return middleware
