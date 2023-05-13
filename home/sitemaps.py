from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse, render
class StaticViewSitemap(Sitemap):
    def items(self):
        priority = 1.0
        changefreq = 'yearly'
        return ['home', 'search', 'result', 'aboutus', 'notice', 'rank']
    def location(self, item):
        return reverse(item)
        
def robot(request):
    return render(request, 'robots.txt')
