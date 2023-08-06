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

    def get_menu_items(self):
        if settings.DOMAINS_OR_SLUGS == 'slugs':
            yield {
                'url': '/',
                'text': 'Home'
            }

            for podcast in Podcast.objects.all():
                yield {
                    'url': '/%s/' % podcast.slug,
                    'text': podcast.name
                }

            return

    def build_menu(self):
        items = list(self.get_menu_items())

        for item in items:
            if item['url'] == self.request.path:
                item['active'] = True

            item['url'] = self.request.build_absolute_uri(item['url'])

        return items

    def get_seo_title(self):
        network_name = settings.NETWORK_NAME
        network_subtitle = settings.network_subtitle

        if network_subtitle:
            return '%s - %s' % (
                network_name,
                network_subtitle
            )

        return network_name

    def get_context_data(self, **kwargs):
        return {
            'menu_items': self.build_menu(),
            **super().get_context_data(**kwargs)
        }


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
