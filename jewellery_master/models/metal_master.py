from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MetalMaster(models.Model):
    _name = 'metal.master'
    _inherit='purity.units'
    _rec_name='rec_name'

    name=fields.Char("Metal Name",placeholder="e.g Gold or Silver",required=True)
    purity=fields.Many2one("purity.units")
    rate=fields.Float("Rate",placeholder="Set a Today rate for this metal",required=True)
    rec_name=fields.Char(compute='_compute_rec_name')

    __sql_constraints = [
        ('name_uniq', 'unique (name,purity)','This metal is already there. pls change the rate')
    ]
 
    @api.model
    def _compute_rec_name(self):
        for rec in self:
            if (rec.purity == False) or (rec.name==False):
                rec.rec_name=""
            else:
                rec.rec_name=str(rec.name)+'  '+str(rec.purity.rec_name)
    def action_set_cost_price(self):
        product_dict = self.env['product.template'].search([])
        for i in product_dict:
            price=self.env['product.template'].browse(i.id).calculation
            self.env['product.template'].browse(i.id).write({'standard_price':price})
            self.env['product.template'].browse(i.id).write({'list_price':price})
