from io import BytesIO

from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import Section, Category, Product
import requests

import bs4

class Command(BaseCommand):
    help = 'Parsing shop'


    def handle(self, *args, **options):
        print('Start parsing')
        pars = BakeryParser()
        pars.getSections(pars.getPage('magazin'))
        print(pars.sections)
        print(pars.types)




class BakeryParser():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.url = 'magazin/folder/pirozhnyye'
        self.baseUrl = 'https://tbkspb.ru/'
        self.catalog = dict.fromkeys(['name', 'img', 'price', 'description', 'composition'])
        self.products = list()
        self.sections = list()
        self.types = list()
        Category.objects.all().delete()
        Section.objects.all().delete()
        Product.objects.all().delete()



    def getPage(self, url):
        #self.pageText = (self.session.get(self.baseUrl + self.url)).text
        #self.parsePage((self.session.get(self.baseUrl + self.url)).text)
        return (self.session.get(self.baseUrl + url)).text

    def getSections(self, pageText):
        soup = bs4.BeautifulSoup(pageText, 'lxml')
        container = soup.find('ul', 'new-folders-menu')
        hrefs = container.find_all('a')
        for item in hrefs:
            href = item['href']
            slug = item['href'].split('/')[-1]

            try:
                img_src = self.baseUrl + item.select_one('a>img').get('src')
            except:
                print('Ошибка, нет картинки!?')
                img_src = ''

            if img_src:
                r = requests.get(img_src)
                buf = BytesIO(r.content)
                img = File(buf, 'section/'+slug+'.jpg')
            else:
                img = 'not_found.jpg'



            sec = Section(url = item['href'], img = img, name = item.text.strip(), slug = slug)
            sec.save()

            self.sections.append([item.text.strip(), item['href'], img_src])
            self.getCategory(self.getPage(href), slug)
        #self.parsePage(self.getPage(self.url))
        return

    def getCategory(self, pageText, sec_slug):

        soup = bs4.BeautifulSoup(pageText, 'lxml')
        container = soup.find('ul', 'new-folders-menu')
        hrefs = container.find_all('a')

        for item in hrefs:
            href = item['href']
            try:
                img_src = self.baseUrl + item.select_one('a>img').get('src')
            except:
                print('Ошибка, нет картинки!?')
                img_src = ''

            slug = item['href'].split('/')[-1]

            if img_src:
                r = requests.get(img_src)
                buf = BytesIO(r.content)
                img = File(buf, 'category/'+slug+'.jpg')
            else:
                img = 'not_found.jpg'

            cat = Category(
                url = item['href'],
                img = img,
                name = item.text.strip(),
                slug = slug,
                section_id = Section.objects.get(slug = sec_slug).id)
            cat.save()
            self.types.append([item.text.strip(), item['href'], img_src])
            self.parsePage(self.getPage(href), slug)
        # self.parsePage(self.getPage(self.url))
        return

    def parsePage(self, pageText, cat_slug):
        soup = bs4.BeautifulSoup(pageText, 'lxml')
        container = soup.select('form.shop2-product-item.shop-product-item')
        #print('item_', container)

        if container:
            for item in container:
                temp = self.parseBlock(item)
                print(temp)
                slug = temp['url'].split('/')[-1]

                if temp['img']:
                    r = requests.get(temp['img'])
                    buf = BytesIO(r.content)
                    img = File(buf, 'product/' + slug + '.jpg')
                else:
                    img = 'not_found.jpg'

                if (not Product.objects.filter(slug = slug).exists()):
                    prod = Product(
                        name = temp['name'],
                        img = img,
                        price = temp['price'],
                        slug = slug,
                        url = temp['url'],
                        description= temp['description'],
                        category_id = Category.objects.get(slug = cat_slug).id
                    )
                    prod.save()
                    self.products.append(temp)
        next_page = soup.find('li', 'page-next')
        if next_page:
            self.parsePage(self.getPage(next_page.a['href']), cat_slug)


    def parseBlock(self, item):

        try:
            name = item.select_one('div.product-name>a').text
        except:
            print('Ошибка, нет имени!?')
            name = None

        try:
            href = item.select_one('div.product-name>a').get('href')
        except:
            print('Ошибка, нет ссылки!?')
            href = ''

        try:
            img_src = self.baseUrl + item.select_one('a.product-image-img>img').get('src')
        except:
            print('Ошибка, нет картинки!?')
            img_src = ''



        try:
            price = item.select_one('div.price-current>strong').text
        except:
            print('Ошибка, нет цены!?')
            price = 'NULL'

        product_href = (self.session.get(self.baseUrl + href)).text
        description, composition = self.parseProduct(product_href)
        return {'name':name,'img':img_src,'price':float(''.join(price.split())), 'description':description, 'composition':composition, 'url': href}

    def parseProduct(self, product_href):
        soup = bs4.BeautifulSoup(product_href, 'lxml')
        description_block = soup.find('div','product-description-wrapper')
        description = ''
        try:
            description_gen = description_block.find('div', 'product-description-body').p.stripped_strings
            for str in description_gen:
                description += str
                description += '\n'
        except:
            description = ''




        #if 'состав' in str(description).lower():
        #    description = ''

        try:
            composition_ = description_block.find('div','product-description-body').ul.stripped_strings
        except:
            composition = ''
        else:
            composition_list=list()
            for item in composition_:
                composition_list.append(item.replace(';', ''))
                #composition_list.append(item)
            composition = '_'.join(composition_list)
        return description, composition

