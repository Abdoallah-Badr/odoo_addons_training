from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Availability",
                                    default=lambda self: (datetime.now() + relativedelta(months=3)).date())
    expected_price = fields.Float(required=True, copy=False)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ], default="north")
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ], default="new")
    property_type_id = fields.Many2one("estate.property.type", strting="Type Of Property")

    buyer = fields.Many2one('res.users')
    salesperson = fields.Many2one('res.partner')
