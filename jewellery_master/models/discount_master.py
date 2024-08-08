
from odoo import models, fields, api


class discountRewardAddons(models.Model):
    _inherit = ['loyalty.reward']

    #By Compezant
    reward_on_item = fields.Selection([
        ('overall_product', 'Overall Product(Sales Price)'),
        ('making_cost', 'Making Cost'),
        ('stone_value_code', 'Stone Price')],
        default='overall_product', required=True)
    
   
    