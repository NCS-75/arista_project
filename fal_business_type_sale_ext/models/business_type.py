from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class BusinessType(models.Model):
    _inherit = 'fal.business.type'

    sale_sequence_id = fields.Many2one('ir.sequence', string="Sale Sequence", copy=False)

    def generate_sale_sequence(self):
        this_company_seq = self.sale_sequence_id.filtered(lambda s: (s.company_id.id == self._context.get('company_id')))
        if not this_company_seq:
            sequence_env = self.env['ir.sequence']
            generated_sequence = sequence_env.create({
                'code': ''.join(['clu.sale.order.', str(self.id)]),
                'name': ''.join(['Cluedoo sale order ', self.name]),
                'prefix': self.fal_business_prefix,
                'suffix': self.fal_business_suffix,
                'number_increment': 1,
                'implementation': 'standard',
                'padding': 3
            })
            self.sale_sequence_id = generated_sequence.id
            return generated_sequence
        else:
            return this_company_seq
