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
import json
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import date
import requests
from odoo import models, api,fields, http, SUPERUSER_ID, tools, _
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse
from odoo.fields import Command
from odoo.http import request, route
from odoo.addons.base.models.ir_qweb_fields import nl2br_enclose
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.addons.sale.controllers import portal as sale_portal
from odoo.osv import expression
from odoo.tools import lazy, str2bool
from odoo.tools.json import scriptsafe as json_scriptsafe

_logger = logging.getLogger(__name__)



class WebsiteAuth(WebsiteSale):
    @http.route(['/shop/cart'], type='http', auth="user", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        order = request.website.sale_get_order()
        if order and order.carrier_id:
            # Express checkout is based on the amout of the sale order. If there is already a
            # delivery line, Express Checkout form will display and compute the price of the
            # delivery two times (One already computed in the total amount of the SO and one added
            # in the form while selecting the delivery carrier)
            order._remove_delivery_line()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        request.session['website_sale_cart_quantity'] = order.cart_quantity

        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get('sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get('sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        if order:
            order.order_line.filtered(lambda l: l.product_id and not l.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        values.update(self._cart_values(**post))
        return request.render("website_sale.cart", values)

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(
        self, product_id, add_qty=1, set_qty=0,
        product_custom_attribute_values=None, no_variant_attribute_values=None,
        express=False, **kwargs
    ):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        if product_custom_attribute_values:
            product_custom_attribute_values = json_scriptsafe.loads(product_custom_attribute_values)

        if no_variant_attribute_values:
            no_variant_attribute_values = json_scriptsafe.loads(no_variant_attribute_values)

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kwargs
        )

        request.session['website_sale_cart_quantity'] = sale_order.cart_quantity

        if express:
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")
    
    @http.route('/process-data', auth='public', type='http', methods=['POST'], csrf=False)
    def my_method(self,**kw):
        # The API endpoint
        post_data = json.loads(request.httprequest.data.decode('utf-8'))['value']
        if len(post_data)!=6:
            data = {'message': 'Please enter 6 digit of your area pincode'}
            return json.dumps(data)

        url1 = "https://sequel247.com/api/checkServiceability"

        # Data to be sent
        data1 = {
            "token": "974a83c8c20e7ddb1e49f8abe4382299",
            "pin_code": str(post_data)
        }

        # A POST request to the API
        response1 = requests.post(url1, json=data1) 

        url2="https://sequel247.com/api/shipment/calculateEDD"
        # Data to be sent
        data2 = {
            "origin_pincode": "110005", 
            "destination_pincode": str(post_data), 
            "pickup_date": str(date.today().strftime("%Y-%m-%d")), 
            "token": "974a83c8c20e7ddb1e49f8abe4382299"
        }

        # A POST request to the API
        response2 = requests.post(url2, json=data2) 

        # Print the response
        response_message=str(response1.json()['message'])
        estimated_date=str(response2.json()['data']["estimated_delivery"])
        estimated_day=str(response2.json()['data']["estimated_day"])
        message=response_message+".Expected Delivery On "+estimated_date+","+estimated_day
        if str(response1.json()['status'])=='false':
            message=response_message
        data = {'message': str(message)}
        return json.dumps(data)
        #return "h"
    

        
        