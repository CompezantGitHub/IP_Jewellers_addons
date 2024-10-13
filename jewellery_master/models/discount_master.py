
from odoo import models, fields, api


class discountRewardAddons(models.Model):
    _inherit = ['product.pricelist.item']

    #By Compezant
    base = fields.Selection(
        selection=[
            ('making_cost', 'Making Cost'),
            ('stone_price', 'On Stone'),
            ('list_price', 'Sales Price'),
            ('standard_price', 'Cost'),
            ('pricelist', 'Other Pricelist')
        ],
        string="Based on",
        default='list_price',
        required=True,
        help="Base price for computation.\n"
             "Sales Price: The base price will be the Sales Price.\n"
             "Cost Price: The base price will be the cost price.\n"
             "Other Pricelist: Computation of the base price based on another Pricelist.")
    on_making_cost=fields.Float(string="On Making cost")
    on_stone_cost=fields.Float(string="On Stone cost")

    def _compute_base_price(self, product, quantity, uom, date, currency):
        """ Compute the base price for a given rule

        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param currency: currency in which the returned price must be expressed

        :returns: base price, expressed in provided pricelist currency
        :rtype: float
        """
        currency.ensure_one()

        rule_base = self.base or 'list_price'
        if rule_base == 'pricelist' and self.base_pricelist_id:
            price = self.base_pricelist_id._get_product_price(
                product, quantity, currency=self.base_pricelist_id.currency_id, uom=uom, date=date
            )
            src_currency = self.base_pricelist_id.currency_id
        elif rule_base == "making_cost":
            src_currency = product.cost_currency_id
            db= product
            

            #Multipier
            sm=""
            if db.categ_id.id==7:
                sm='DMUL'
            elif db.categ_id.id==8:
                sm='PMUL'
            else:
                sm='GMUL'
            multipier_code_value=self.env['purity.units'].sudo().search([('name','=',sm)])
            mul_code=55.0
            for i in multipier_code_value:
                mul_code=float(self.env['purity.units'].sudo().browse(i.id).unit)
                break

            stone_code_multiple=mul_code*db.stone_value_code 
            new_making_cost=db.making_cost*round(1-(self.price_discount/100),6) #Discount
            new_per_gram_making=int(float(db.making_cost_per_gram)*float(mul_code))

            new_value=round((float(db.metal_rate)*float(db.metal_weight))*(1+round((new_making_cost)/100,6)),6)+stone_code_multiple+new_per_gram_making
            increased_new_value=int(new_value/float(1-round(self.price_discount/100,6)))    
            price=int(increased_new_value)
            
        elif rule_base == "stone_price":
            src_currency = product.cost_currency_id
            db= product

            #Multipier
            sm=""
            if db.categ_id.id==7:
                sm='DMUL'
            elif db.categ_id.id==8:
                sm='PMUL'
            else:
                sm='GMUL'
            multipier_code_value=self.env['purity.units'].sudo().search([('name','=',sm)])
            mul_code=55.0
            for i in multipier_code_value:
                mul_code=float(self.env['purity.units'].sudo().browse(i.id).unit)
                break

            mul_code=mul_code*round(1-(self.price_discount/100),6) 
            stone_code_multiple=mul_code*db.stone_value_code 
            new_stone_code_multiple=stone_code_multiple#Discount
            new_value=round((float(db.metal_rate)*float(db.metal_weight))*(1+round((db.making_cost)/100,6)),6)+new_stone_code_multiple+int(float(db.making_cost_per_gram)*float(mul_code))
            increased_new_value=int(new_value/float(1-round(self.price_discount/100,6)))    
            price=int(increased_new_value)
            
        elif rule_base == "standard_price":
            src_currency = product.cost_currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]
        else: # list_price
            src_currency = product.currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]

        if src_currency != currency:
            price = src_currency._convert(price, currency, self.env.company, date, round=False)

        return price
    
    
   
    