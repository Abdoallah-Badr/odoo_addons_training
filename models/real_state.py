from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError


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
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])
    total_area = fields.Integer(readonly=True, compute="_compute_total_area", store=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ], default="new")
    property_type_id = fields.Many2one("estate.property.type", string="Type Of Property")

    buyer = fields.Many2one('res.partner', readonly=True)
    salesman = fields.Many2one('res.users')
    tag_ads = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_offer = fields.Float(compute="_compute_best_offer", store=True)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if rec.garden is False:
                rec.garden_area = 0
                rec.garden_orientation = False

    def set_sold_action(self):
        for rec in self:
            if rec.state == "canceled":
                raise UserError("Canceled Property Cannot Sold")
            else:
                rec.state = "sold"

    def set_canceled_action(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError("Sold Property Cannot Canceled")
            else:
                rec.state = "canceled"

    def set_force_action(self):
        for rec in self:
            rec.state = "new"
