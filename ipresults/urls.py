"""ipresults URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from home.sitemaps import StaticViewSitemap, robot
from django.contrib.auth.models import Group,User
from django.conf import settings
from django.conf.urls.static import static
sitemaps = {
    'static': StaticViewSitemap
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', robot),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "Result Explorer"
admin.site.site_title = "Result Explorer"
admin.site.index_title = "Result Explorer Admin Portal"

admin.site.unregister(Group)
admin.site.unregister(User)

handler404 = 'home.views.er404'
handler500 = 'home.views.er500'