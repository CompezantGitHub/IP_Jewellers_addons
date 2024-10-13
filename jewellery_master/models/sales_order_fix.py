from odoo import models, fields, http
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        # Check if the sales order is not in draft status
        if 'state' in vals and vals['state'] != 'draft':
            # Redirect to the login page
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'params': {
                    'next': '/shop/cart',  # Redirect URL
                },
            }
        # Call the super method if the state is draft
        return super(SaleOrder, self).write(vals)