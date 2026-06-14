#This is python function take request as agrument and it will return data in dict format
#important note: This file should be register in Templates in settings.py file so that it wil be avaliable in all templates
from .models import Category
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)