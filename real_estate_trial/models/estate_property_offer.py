from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime


class Property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer model for estate module'

    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    deadline = fields.Date(string='Deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        self.deadline = datetime.date.today() + datetime.timedelta(days=self.validity)

    def action_property_accept(self):
        for rec in self:
            if rec.status == 'refused':
                raise UserError('this offer refused before')
            else:
                rec.status = 'accepted'
                return


    def action_property_refuse(self):
        for rec in self:
            if rec.status == 'accepted':
                raise UserError('this offer accepted before')
            else:
                rec.status = 'refused'
                return
