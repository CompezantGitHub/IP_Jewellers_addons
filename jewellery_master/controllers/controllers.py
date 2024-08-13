# -*- coding: utf-8 -*-
# from odoo import http


# class Odoo(http.Controller):
#     @http.route('/odoo/odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo/odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo.listing', {
#             'root': '/odoo/odoo',
#             'objects': http.request.env['odoo.odoo'].search([]),
#         })

#     @http.route('/odoo/odoo/objects/<model("odoo.odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteAuth(WebsiteSale):
    @http.route(['/shop/cart'], type='http', auth="user", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        return super(WebsiteAuth, self).cart(access_token=None, revive='', **post)
    
    @http.route('/web/send_otp', auth='public', type='json')
    def web_send_otp(self, **kw):
        return "Arya"
        
        