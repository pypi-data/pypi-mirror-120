from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View
from django.views.generic.list import ListView
from pico.conf import settings
from pico.podcasts.models import Podcast
from pico.podcasts.tasks import update_feed
from pico.seo.mixins import SEOMixin, OpenGraphMixin
import re


LINK_REGEX = re.compile(r'^\<([^\>]+)\>')


class PodcastListView(SEOMixin, OpenGraphMixin, ListView):
    model = Podcast
    template_name = 'index.html'

    def get_seo_title(self):
        network_name = settings.NETWORK_NAME
        network_subtitle = settings.network_subtitle

        if network_subtitle:
            return '%s - %s' % (
                network_name,
                network_subtitle
            )

        return network_name


class PodcastPingView(View):
    def get(self, request):
        topic = request.GET.get('hub.topic')
        mode = request.GET.get('hub.mode')
        challenge = request.GET.get('hub.challenge')

        for podcast in Podcast.objects.filter(
            rss_feed_url=topic
        ):
            if mode in ('subscribe', 'unsubscribe') and challenge:
                return HttpResponse(challenge)

        return HttpResponseBadRequest('FAIL')

    def post(self, request):
        topic = request.META.get('HTTP_LINK')

        if topic:
            match = LINK_REGEX.match(topic)
            if match is not None:
                url = match.groups()[0]

                for podcast in Podcast.objects.filter(
                    rss_feed_url=url
                ):
                    update_feed.delay(podcast.pk, request.body)
                    return HttpResponse('OK')

        return HttpResponseBadRequest('FAIL')
