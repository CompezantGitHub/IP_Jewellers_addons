from odoo import api, fields, models

class StoneMaster(models.Model):
    _name = 'stone.master'
    _rec_name='rec_name'
    
    name=fields.Char("Stone Name",placeholder="e.g Diamond Rubi",required=True)
    rec_name=fields.Char(compute='_compute_rec_name')
 
    @api.model
    def _compute_rec_name(self):
        for rec in self:
            rec.rec_name=str(rec.name)
    
    def action_set_cost_price(self):
        product_dict = self.env['product.template'].search([])
        for i in product_dict:
            price=self.env['product.template'].browse(i.id).calculation
            self.env['product.template'].browse(i.id).write({'standard_price':price})
            self.env['product.template'].browse(i.id).write({'list_price':price})
    