# coding=utf-8


import webapp2
import json
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import mail


import handler
import caching

### CONTROLLERS ###

items_per_page = 20
pagination_count = 10
categories = [u'Бакалея',
            u'Чай. Кофе. Какао',
            u'Молочные продукты',
            u'Напитки']

subcategories = {}
subcategories[u'Бакалея'] = [u'Крупы',u'Макаронные Изделия',u'Соль',u'Сахар']
subcategories[u'Чай. Кофе. Какао'] = [u'Чай']
subcategories[u'Напитки'] = [u'Напитки']
subcategories[u'Молочные продукты'] = [u'Молоко',u'Майонез']


class MainPage(handler.Handler):
    def get(self):
        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())
        item_cart = self.session.get('items')
        self.render("home.html",{'subcategories':subcategories, 
            'categories':categories, 
            'item_cart':item_cart, 
            'cat_num':-1, 
            'is_home': 1,
            'shop_list_data':self.session.get('shop_list_data'),})

class LoginHandler(handler.Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.session["items"] = {}
            self.session["store_total"] = {}
            self.session['quantity'] = {}
            self.session['shop_list_data'] = ""
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ShowCategoryWithPaginationHandler(handler.Handler):
    def get(self, category_id, current_page):       
        current_store = self.request.get('store')

        items = caching.get_items_with_category(category_id)
        total_items_size = len(items)
        start_from = int(current_page)*items_per_page
        items = items[start_from:min(len(items),start_from+items_per_page)]

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())

        store_total = self.session.get('store_total')

        self.render("main.html", {'current_page':int(current_page), 
            'subcategories':subcategories,
            'current_store':current_store,
            'pagination_count':pagination_count, 
            'items_per_page':items_per_page, 
            'total_items_size':total_items_size, 
            'items':items, 
            'items_size':len(items)-1, 
            'categories':categories, 
            'item_cart':item_cart, 
            'cat_num':int(category_id),
            'store_total':store_total,
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,})


class ShowCategoryHandler(handler.Handler):
    def get(self, category_id):
        current_store = self.request.get('store')

        items = caching.get_items_with_category(category_id)
        total_items_size = len(items)
        items = items[:min(len(items),items_per_page)]

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())

        store_total = self.session.get('store_total')


        self.render("main.html", {'current_page':0,
            'subcategories':subcategories, 
            'pagination_count':pagination_count, 
            'current_store':current_store,
            'items_per_page':items_per_page, 
            'total_items_size':total_items_size, 
            'items':items, 
            'items_size':len(items)-1, 
            'categories':categories, 
            'item_cart':item_cart, 
            'cat_num':int(category_id),
            'store_total':store_total,
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,})

class ShowSubCategoryHandler(handler.Handler):
    def get(self, category_id, subcategory_id):

        current_store = self.request.get('store')

        items = caching.get_items_with_subcategory(subcategory_id)
        total_items_size = len(items)
        items = items[:min(len(items),items_per_page)]

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())

        item_cart = self.session.get('items')
        store_total = self.session.get('store_total')

        dates = {}
        for i in items:
            dates[i._id] = i.added_date.strftime('%d-%m-%y %H:%M:%S')

        self.render("main.html", {'current_page':0,
            'subcategories':subcategories, 
            'pagination_count':pagination_count, 
            'items_per_page':items_per_page, 
            'total_items_size':total_items_size, 
            'items':items, 
            'dates':dates,
            'current_store':current_store,
            'items_size':len(items)-1, 
            'categories':categories, 
            'item_cart':item_cart, 
            'cat_num':int(category_id),
            'store_total':store_total,
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,
            'shop_list_data':self.session.get('shop_list_data'),})

class ShowSubCategoryWithPaginationHandler(handler.Handler):
    def get(self, category_id, subcategory_id, current_page):       

        user_name = "None"
        if self.user_info:
            my_user=self.user
            user_name = my_user.auth_ids[0]

        current_store = self.request.get('store')
        if current_store is None or current_store == "":
            if memcache.get('current_store' + user_name):
                current_store = memcache.get('current_store' + user_name)
            else:
                if user_name != "None":
                    current_store = caching.get_store_with_id(caching.get_user(user_name, update=True).store_id)
                else:
                    current_store = caching.get_store_with_id(0)
                memcache.set('current_store' + user_name, current_store)
        else:
            current_store = caching.get_store_with_id(int(current_store))
            memcache.set('current_store' + user_name, current_store)

        items = caching.get_items_with_subcategory(subcategory_id)
        total_items_size = len(items)
        start_from = int(current_page)*items_per_page
        items = items[start_from:min(len(items),start_from+items_per_page)]

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())
        store_total = self.session.get('store_total')
        dates = {}
        for i in items:
            dates[i._id] = i.added_date.strftime('%d-%m-%y %H:%M:%S')

        self.render("main.html", {'current_page':int(current_page), 
            'subcategories':subcategories,
            'pagination_count':pagination_count, 
            'items_per_page':items_per_page, 
            'current_store':current_store,
            'total_items_size':total_items_size, 
            'items':items, 
            'dates':dates,
            'items_size':len(items)-1, 
            'categories':categories, 
            'item_cart':item_cart, 
            'cat_num':int(category_id),
            'subcat_num':int(subcategory_id),
            'store_total':store_total,
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,
            'shop_list_data':self.session.get('shop_list_data'),})


class AboutHandler(handler.Handler):
    def get(self):
        self.render("about.html")

class SecureHandler(handler.Handler):
    def get(self):
        if users.get_current_user():
            self.write("Welcome to secure page. session value= %s" % self.session.get("foo"))
        else:
            self.write("you need to login to see this page")

class LogoutHandler(handler.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.redirect(users.create_logout_url('/'))



class SubCategoryAJAX(handler.Handler):
    def get(self, subcategory_id):

        current_store = self.request.get('store')
        if current_store is None or current_store == "":
            if memcache.get('current_store'):
                current_store = memcache.get('current_store')
            else:
                if self.user_info:
                    my_user=self.user
                    user_name = my_user.auth_ids[0]
                    logging.error(user_name)
                    current_store = caching.get_store_with_id(caching.get_user(user_name, update=True).store_id)
                else:
                    current_store = 0
                memcache.set('current_store', current_store)
        else:
            current_store = caching.get_store_with_id(int(current_store))
            memcache.set('current_store', current_store)

        logging.error("SUBCATEGORY AJAX")
        logging.error(self.session.get('used_category'))

        if 'used_category' not in self.session:
            logging.error('FUCK')
            self.session['used_category'] = []

        if subcategory_id not in self.session['used_category']:
            self.session['used_category'] += subcategory_id

        items = []
        for subcategory in self.session['used_category']:
            logging.error(subcategory)
            items += caching.get_items_with_subcategory(subcategory)

        total_items_size = len(items)

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())

        store_total = self.session.get('store_total')
        dates = {}
        for i in items:
            dates[i._id] = i.added_date.strftime('%d-%m-%y %H:%M:%S')

        self.render("main.html", {'current_page':0,
            'subcategories':subcategories, 
            'pagination_count':-1, 
            'items_per_page':items_per_page, 
            'total_items_size':total_items_size, 
            'items':items, 
            'items_size':len(items)-1, 
            'categories':categories, 
            'item_cart':item_cart, 
            'dates':dates,
            'current_store':current_store,
            'store_total':store_total,
            'active_subcategories':self.session['used_category'],
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,
            'shop_list_data':self.session.get('shop_list_data'),})

class SubCategoryAJAXExcept(handler.Handler):
    def get(self, subcategory_id):

        user_name = "None"
        if self.user_info:
            my_user=self.user
            user_name = my_user.auth_ids[0]

        current_store = self.request.get('store')
        if current_store is None or current_store == "":
            if memcache.get('current_store' + user_name):
                current_store = memcache.get('current_store' + user_name)
            else:
                if user_name != "None":
                    current_store = caching.get_store_with_id(caching.get_user(user_name, update=True).store_id)
                else:
                    current_store = caching.get_store_with_id(0)
                memcache.set('current_store' + user_name, current_store)
        else:
            current_store = caching.get_store_with_id(int(current_store))
            memcache.set('current_store' + user_name, current_store)

        if 'used_category' not in self.session:
            self.session['used_category'] = []

        if subcategory_id in self.session['used_category']:
            index = 0
            temp = []
            for i in self.session['used_category']:
                if i != subcategory_id:
                    temp.append(i)
            self.session.pop('used_category')
            self.session['used_category'] = temp

        items = []
        for subcategory in self.session['used_category']:
            logging.error(subcategory)
            items += caching.get_items_with_subcategory(subcategory)

        total_items_size = len(items)

        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())

        store_total = self.session.get('store_total')
        dates = {}
        for i in items:
            dates[i._id] = i.added_date.strftime('%d-%m-%y %H:%M:%S')

        self.render("main.html", {'current_page':0,
            'subcategories':subcategories, 
            'pagination_count':-1, 
            'items_per_page':items_per_page, 
            'total_items_size':total_items_size, 
            'items':items, 
            'dates':dates,
            'items_size':len(items)-1, 
            'current_store':current_store,
            'categories':categories, 
            'item_cart':item_cart, 
            'store_total':store_total,
            'active_subcategories':self.session['used_category'],
            'store_sum':store_sum,
            'store_list':store_list,
            'item_list':item_list,
            'shop_list_data':self.session.get('shop_list_data'),})
