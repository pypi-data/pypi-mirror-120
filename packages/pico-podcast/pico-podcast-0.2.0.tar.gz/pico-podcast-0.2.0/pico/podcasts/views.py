from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from pico.seo.mixins import (
    SEOMixin, OpenGraphMixin, OpenGraphArticleMixin
)

from .models import Episode, Season, Post, Page, Category


class PodcastMixin(object):
    def get_menu_items(self):
        yield {
            'url': '/',
            'text': 'Home'
        }

        for season in self.request.podcast.seasons.order_by('-number'):
            yield {
                'url': reverse('season', args=(season.number,)),
                'text': str(season)
            }

        if self.request.podcast.blog_posts.exists():
            yield {
                'url': reverse('blogpost_list'),
                'text': 'Blog'
            }

        for page in self.request.podcast.pages.filter(menu_visible=True):
            yield {
                'url': reverse('page_detail', args=(page.slug,)),
                'text': page.menu_title or page.title,
                'highlight': page.cta
            }

    def build_menu(self):
        items = list(self.get_menu_items())

        for item in items:
            if item['url'] == self.request.path:
                item['active'] = True

            item['url'] = self.request.build_absolute_uri(item['url'])

        return items

    def get_context_data(self, **kwargs):
        return {
            'podcast': self.request.podcast,
            'base_url': self.request.build_absolute_uri('/'),
            'menu_items': self.build_menu(),
            **super().get_context_data(**kwargs)
        }

    def get_og_title(self):
        return self.request.podcast.name

    def get_og_description(self):
        return self.request.podcast.subtitle

    def get_og_site_name(self):
        return self.request.podcast.name

    def get_twitter_card(self):
        return self.twitter_card

    def get_twitter_title(self):
        return self.get_og_title()

    def get_twitter_description(self):
        return self.get_og_description()

    def get_twitter_creator(self):
        if self.request.podcast.twitter_username:
            return '@%s' % self.request.podcast.twitter_username

        return super().get_twitter_creator()


class EpisodeListView(PodcastMixin, SEOMixin, OpenGraphMixin, ListView):
    model = Episode
    og_type = 'website'
    paginate_by = 10

    def get_seo_title(self):
        return '%s – %s' % (
            self.request.podcast.name,
            self.request.podcast.subtitle
        )

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            podcast=self.request.podcast
        )

        if self.request.GET.get('category'):
            queryset = queryset.filter(
                categories__slug=self.request.GET['category']
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('category'):
            context['category'] = Category.objects.filter(
                slug=self.request.GET['category']
            ).first()

        return context

    def get_canonical_url(self):
        if self.request.GET.get('category'):
            for category in Category.objects.filter(
                slug=self.request.GET['category']
            ):
                return self.request.build_absolute_uri(
                    category.get_absolute_url()
                )

        return self.request.build_absolute_uri(
            reverse('episode_list')
        )


class SeasonView(EpisodeListView):
    template_name = 'podcasts/season.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            podcast=self.request.podcast,
            season__number=self.kwargs['number']
        )

    def get_context_data(self, **kwargs):
        return {
            'season': get_object_or_404(
                Season,
                podcast=self.request.podcast,
                number=self.kwargs['number']
            ),
            **super().get_context_data(**kwargs)
        }

    def get_canonical_url(self):
        return self.request.build_absolute_uri(
            reverse('season', kwargs=self.kwargs)
        )


class EpisodeDetailView(
    PodcastMixin, SEOMixin, OpenGraphArticleMixin, DetailView
):
    model = Episode
    bonus = False
    trailer = False

    def get_seo_title(self):
        return '%s | %s' % (
            self.object.title,
            self.request.podcast.name
        )

    def get_seo_description(self):
        return self.object.summary

    def get_og_title(self):
        return self.object.title

    def get_og_description(self):
        return self.object.summary

    def get_og_image(self):
        if self.object.artwork:
            return self.object.artwork

        if self.object.season:
            if self.object.season.artwork:
                return self.object.season.artwork

        return self.object.podcast.artwork

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            podcast=self.request.podcast,
            bonus=self.bonus
        )

        if self.kwargs.get('season'):
            queryset = queryset.filter(
                season__number=self.kwargs['season']
            )
        else:
            queryset = queryset.filter(season=None)

        return queryset

    def get_object(self):
        if self.trailer:
            return self.get_queryset().get(
                trailer=True
            )

        return self.get_queryset().get(
            number=self.kwargs['number']
        )


class PostListView(PodcastMixin, SEOMixin, OpenGraphMixin, ListView):
    model = Post
    paginate_by = 10

    def get_seo_title(self):
        return 'Blog – %s' % self.request.podcast.subtitle

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            podcast=self.request.podcast,
            published__lte=timezone.now()
        )

        if self.request.GET.get('category'):
            queryset = queryset.filter(
                categories__slug=self.request.GET['category']
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('category'):
            context['category'] = Category.objects.filter(
                slug=self.request.GET['category']
            ).first()

        return context

    def get_canonical_url(self):
        return self.request.build_absolute_uri(
            reverse('blogpost_list')
        )


class PostDetailView(
    PodcastMixin, SEOMixin, OpenGraphArticleMixin, DetailView
):
    model = Post

    def get_seo_title(self):
        return '%s | %s' % (
            self.object.title,
            self.request.podcast.name
        )

    def get_seo_description(self):
        return self.object.summary

    def get_og_title(self):
        return self.object.title

    def get_og_description(self):
        return self.object.summary

    def get_og_image(self):
        if self.object.image:
            return self.object.image

        return self.object.podcast.artwork

    def get_queryset(self):
        return super().get_queryset().filter(
            podcast=self.request.podcast
        )


class PageDetailView(
    PodcastMixin, SEOMixin, OpenGraphArticleMixin, DetailView
):
    model = Page

    def get_seo_title(self):
        return '%s | %s' % (
            self.object.title,
            self.request.podcast.name
        )

    def get_og_title(self):
        return self.object.title

    def get_og_image(self):
        if self.object.image:
            return self.object.image

        return self.object.podcast.artwork

    def get_queryset(self):
        return super().get_queryset().filter(
            podcast=self.request.podcast
        )


class FeedRedirectView(View):
    def get(self, request):
        return HttpResponsePermanentRedirect(
            request.podcast.rss_feed_url
        )
