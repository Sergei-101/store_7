from pages.models import StaticPage

def menu_pages(request):
    pages = StaticPage.objects.filter(in_menu=True)
    return {'menu_pages': pages}
