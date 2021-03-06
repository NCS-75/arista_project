from odoo import fields, models, api, _
from odoo.exceptions import AccessError


class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    def _get_business_type_default(self):
        user_id = self.env['res.users'].browse(self.env.uid)
        return user_id.fal_business_type_id or False

    fal_business_type = fields.Many2one(
        'fal.business.type', 'Business Type',
        default=_get_business_type_default, index=True, readonly=True, required=True,
        help='Let this field empty if this location is shared between business types', domain="[('company_id', '=', company_id)]")

    _sql_constraints = [
        ('warehouse_name_uniq', 'unique(name, company_id, fal_business_type)', 'The name of the warehouse must be unique per company / Business Types!'),
        ('warehouse_code_uniq', 'unique(code, company_id, fal_business_type)', 'The code of the warehouse must be unique per company / Business Types!'),
    ]
