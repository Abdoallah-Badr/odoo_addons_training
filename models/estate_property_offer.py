from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity(Day)")
    date_deadline = fields.Datetime(compute="_compute_date_deadline", string="Deadline",
                                    inverse="_inverse_date_deadline", store=True)
    create_date = fields.Datetime(string="Create Date", default=fields.Datetime.now, readonly=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date).days

    def set_accepted(self):
        for rec in self:
            rec.status = "accepted"
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer = rec.partner_id.id

    def set_refused(self):
        for rec in self:
            rec.status = "refused"
