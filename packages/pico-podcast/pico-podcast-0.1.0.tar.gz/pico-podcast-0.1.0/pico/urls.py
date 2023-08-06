from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from .views import PodcastListView, PodcastPingView


urlpatterns = (
    path('admin/rq/', include('django_rq.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('~/ping/', csrf_exempt(PodcastPingView.as_view()), name='api_ping'),
    path('', PodcastListView.as_view(), name='podcast_list')
)


if settings.DEBUG:
    from django.views.static import serve as static_serve

    urlpatterns += (
        re_path(
            r'^media/(?P<path>.*)$',
            static_serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
    )
