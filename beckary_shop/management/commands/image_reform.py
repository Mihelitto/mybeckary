from io import BytesIO

from django.core.management.base import BaseCommand
from ...models import Section, Category, Product
import requests

from django.core.files import File


class Command(BaseCommand):
    help = 'Upload images by links'


    def handle(self, *args, **options):
        print('Start command')
        cats = Section.objects.all()
        for item in cats:
            print(item.img)
            if item.img:
                #response = request.urlopen(item.img)

                #file = open(item.slug+'.jpg', 'wb')
                #print(file)
                #image = path.basename()
                get_img = requests.get(item.img)
                buf = BytesIO()
                buf.write(get_img.content)
                item.img = File(buf, item.slug+'.jpg')
                item.save()
            else:
                img = 'empty'
            #img = ImageFile(get_img.content)
            #img.save(item.slug+'.jpg',get_img.content)


