
from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = "res.users"

    product_filter = fields.Selection([('by_product', 'Products'), ('by_category', 'Category')], default='by_product', string="Based on")
    category_ids = fields.Many2many('product.category', string="Allowed Category")
    product_ids = fields.Many2many('product.product', string='Allowed Product')

    @api.onchange('product_filter')
    def onchange_product_filter(self):
        if self.product_filter == 'by_product':
            self.category_ids = []
        else:
            self.product_ids = []

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        # TDE FIXME: strange
        if self.env.user.product_ids:
            args.append((('id', 'in', self.env.user.product_ids.mapped('product_tmpl_id').ids)))
        if self.env.user.category_ids:
            args.append((('categ_id', 'child_of', self.env.user.category_ids.ids)))
        return super(ProductTemplate, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        # TDE FIXME: strange
        if self.env.user.product_ids:
            args.append((('id', 'in', self.env.user.product_ids.ids)))
        if self.env.user.category_ids:
            args.append((('categ_id', 'child_of', self.env.user.category_ids.ids)))
        return super(ProductProduct, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
