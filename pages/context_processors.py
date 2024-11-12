from pages.models import StaticPage

def menu_pages(request):
    pages = StaticPage.objects.filter(in_menu=True).order_by('menu_position')
    return {'menu_pages': pages}
