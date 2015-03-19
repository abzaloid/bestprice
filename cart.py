
import json
import logging
import operator


from google.appengine.api import users
from webapp2_extras import sessions

import handler
import models
import caching

class EmptyCart(handler.Handler):
    def get(self):
        self.session["item_count"] = 0
        self.session["add_to_cart_count"] = 0
        self.session["items"] = {}
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.redirect("/")

class AddToCartHandler(handler.Handler):
    def get(self):
        if self.user_info:
            self.response.headers['Content-type'] = 'application/json'
            get_current_add_count = int(self.session.get('add_to_cart_count'))
            tshirt_id = self.request.get("tshirt_id")
            item_title = self.request.get("item_title")
            qty = self.request.get("qty")
            size = self.request.get("size")
            price = 325
            get_current_add_count += 1
            self.session[get_current_add_count] = { "qty" : qty, "size" : size ,
                                                    "item_title": item_title, 
                                                    "tshirt_id" : tshirt_id,
                                                    "cost" : price * int(qty)}

            current_cart_items = int(self.session.get("item_count"))
            updated_cart_items = current_cart_items + int(qty)
            self.session["item_count"] = updated_cart_items
            self.session["add_to_cart_count"] = get_current_add_count
            self.write(json.dumps({"status" : 1, "msg" : "Order added. <a href='/cart'><span class='label label-success'>View Cart</span></a>"}))
        else:
            self.write(json.dumps({"status" : 0, "msg" : "Please <a href='/login'><span class='label label-important'>login</span> </a>to start shopping!"}))


class CartHandler(handler.Handler):
    def get(self):
        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items, cost in item_list:
                logging.error(len(items))
                if items:
                    quantity = int(round(cost / items[0].price))
                    for item in items:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        min_sum = -1
        for store, m_sum in store_sum.items():
            if min_sum == -1:
                min_sum = m_sum
            else:
                min_sum = min(min_sum, m_sum)

        store_list = list(caching.get_stores())
        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        self.render('show_cart.html', subcategories=subcategories, 
                                    categories=categories, 
                                    item_list=item_list, 
                                    store_sum=store_sum, 
                                    store_list=store_list, 
                                    min_sum=min_sum)

class CheckoutHandler(handler.Handler):
    def get(self):
        item_list = self.get_items_from_cart()
        user = self.auth.get_user_by_session()
        if user:
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.session["items"] = {}
            logging.error("Order Added for user: %s" % user['name'])
            self.redirect('/done')

class DoneHandler(handler.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.write("Your order has been recorded. You shortly hear from us regarding payment and delivery details. Thanks for ordering. <a href='/'>Continue shopping</a>")
        self.session["item_count"] = 0
        self.session["add_to_cart_count"] = 0
        self.session["items"] = {}
 

class ListOrdersHandler(handler.Handler):
    def get(self):
        orders = db.GqlQuery("SELECT * FROM Order ORDER BY time_of_order")
        self.response.headers['Content-type'] = 'text/plain'
        self.render("list_orders.html", orders = orders)