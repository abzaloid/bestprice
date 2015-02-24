
import json
import logging

from google.appengine.api import users
from webapp2_extras import sessions

import handler
import models

class AddToCartHandler(handler.Handler):
    def get(self):
        if users.get_current_user():
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
        self.render('show_cart.html', item_list = item_list)

class CheckoutHandler(handler.Handler):
    def get(self):
        item_list = self.get_items_from_cart()
        user = users.get_current_user()
        if user:
            user_email = user.email()
            if item_list:
                for i in item_list:
                    order = models.Order(qty = int(i["qty"]), 
                                  user_email = user_email,
                                  size = i["size"],
                                  tshirt_id = int(i["tshirt_id"]))
                    order.put()
                    logging.error("Attempt to put in database")
            else:
                logging.error("Updation to Order Model missed")
        else:
            self.redirect('/')
        logging.error("Order Added for user: %s" % user.email())
        self.session["add_to_cart_count"] = 0
        self.redirect('/done')

class DoneHandler(handler.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.write("Your order has been recorded. You shortly hear from us regarding payment and delivery details. Thanks for ordering. <a href='/'>Continue shopping</a>")
 

class ListOrdersHandler(handler.Handler):
    def get(self):
        orders = db.GqlQuery("SELECT * FROM Order ORDER BY time_of_order")
        self.response.headers['Content-type'] = 'text/plain'
        self.render("list_orders.html", orders = orders)