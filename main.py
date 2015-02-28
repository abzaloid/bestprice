import os
import sys
import webapp2
import jinja2

import database
import search
import controllers
import admin
import cart
import calculate

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
### Configuration ###
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([('/', controllers.MainPage),
                               ('/logout', controllers.LogoutHandler),
                               ('/login', controllers.LoginHandler), 
                               ('/item/add', admin.AddItemHandler), 
                               ('/item/edit', admin.EditItemHandler), 
                               ('/cart/add', cart.AddToCartHandler),
                               ('/about', controllers.AboutHandler),
                               ('/done', cart.DoneHandler),
                               ('/mainpage', controllers.MainPage),
                               ('/cart', cart.CartHandler),
                               ('/all.json', controllers.JSONHandler),
                               ('/checkout', cart.CheckoutHandler),
                               ('/sendmail', admin.EmailHandler),
                               ('/listorders', cart.ListOrdersHandler),
                               ('/secure', controllers.SecureHandler),
                               ('/tshirt/(\d+)', controllers.ShowItemHandler),
                               ('/update_database', database.UpdateDatabase),
                               ('/search', search.SearchItem),
                               ('/lookfor', search.LookForItem),
                               ('/additem', calculate.addItemToCart)], 
                               config=config, debug=True)
