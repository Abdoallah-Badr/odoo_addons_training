from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.constrains("price")
    def positive_price(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError("The Selling Price should be positive")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date).days

    def set_accepted(self):
        for rec in self:
            if rec.price >= rec.property_id.expected_price * 0.9:
                rec.status = "accepted"
                rec.property_id.selling_price = rec.price
                rec.property_id.buyer = rec.partner_id.id
                rec.property_id.state = "offer_accepted"
            else:
                raise ValidationError("the selling price cannot be lower than 90% of the expected price.")

    def set_refused(self):
        for rec in self:
            rec.status = "refused"

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer_received"
        return super().create(vals)
