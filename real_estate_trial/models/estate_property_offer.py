from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
import datetime


class Property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer model'
    _order = 'price desc'

    price = fields.Float('Price', store=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, store=True)
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer(string='Validity', default=7)
    deadline = fields.Date(string='Deadline', compute='_compute_deadline')

    property_type_id = fields.Many2one('estate.property.type')

    _sql_constraints = [
        ('no_of_price_positive', 'CHECK(price > 0)', 'The offer price must be positive.'),
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for rec in self:
            rec.deadline = datetime.date.today() + datetime.timedelta(days=rec.validity)

    @api.constrains('price')
    def offer_price_constrains(self):
        for rec in self:
            offer_price = rec.price
            property = rec.property_id
            expected_price = property.expected_price
            ninety_percentage = expected_price * 0.9
            comparison_result = float_compare(offer_price, ninety_percentage, 4)
            if comparison_result < 0:
                raise ValidationError('the offer must be more than 90% of expected price')
            else:
                pass

    def action_property_accept(self):
        for rec in self:
            if rec.status == 'refused':
                raise UserError('this offer refused before')
            else:
                rec.status = 'accepted'
                if rec.property_id:
                    property = rec.property_id
                    property.write({'sell_price': rec.price})

    def action_property_refuse(self):
        for rec in self:
            if rec.status == 'accepted':
                raise UserError('this offer accepted before')
            else:
                rec.status = 'refused'

        return False

    @api.model
    def create(self, vals):
        if vals.get('property_id') and vals.get('price'):
            property= self.env['estate_property'].browse(vals['property_id'])
            max_price = max(property.mapped('offer_ids.price'))
            if float_compare(vals["price"], max_price, precision_rounding=0.01) <= 0:
                raise UserError('the offer lower than expected')

            self.env['estate.property'].browse(vals['property_id']).write({'status': 'received'})
        return super().create(vals)
