from odoo import models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            property_record = self.env['estate.property'].browse(property_id)
            if property_record.state == 'sold':
                raise UserError("This property is already sold.")
        return super(EstatePropertyOffer, self).create(vals)
