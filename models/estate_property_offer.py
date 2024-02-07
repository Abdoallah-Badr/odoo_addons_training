from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ("accepted,", "Accepted,"),
        ("Refused,", "Refused,"),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity(Day)")
    date_deadline = fields.Date(compute="_compute_date_deadline", string="Deadline",
                                inverse="_inverse_date_deadline", store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (fields.Datetime.from_string(rec.date_deadline) - rec.create_date).days
