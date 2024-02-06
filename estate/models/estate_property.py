from odoo import models, fields, api, _, exceptions
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstatePropertyDescription'

    name = fields.Char(string='Title', requried=1, size=20)
    status = fields.Selection([('canceled', 'Canceled'), ('new', 'New'), ('sold', 'Sold')], string='Statsu')
    property_tag_id = fields.Many2many('estate.property.tags', string="Property Type")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    postcode = fields.Char(string='Postcode', size=20)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.partner', string="Seller")
    description = fields.Text(string='Description')
    date_availability = fields.Date(string='Date Aavailability')
    expected_price = fields.Float(string='Expected Price', required=True)
    # best_price = fields.Float(string='Best Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='bedrooms')
    living_area = fields.Integer(string='Living Area', default=0)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='garden')
    age = fields.Integer(string='Age', default=6)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
    gardens_area = fields.Integer(string="Garden Area", default=0)
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price', store=True, default=0)

    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.gardens_area

    @api.depends('price')
    def _compute_best_price(self):
        for property_record in self:
            property_record.best_price = max(property_record.offer_ids.mapped('price'), default=0.0)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            # print(rec.offer_ids.mapped('price'))
            # print(max(rec.offer_ids.mapped('price')))
            rec.best_price = max(rec.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def garden_area(self):
        for rec in self:
            if rec.garden:
                rec.gardens_area = 10
                rec.garden_orientation = 'north'
            else:
                rec.gardens_area = 0
                rec.garden_orientation = ''

    def action_do_something(self):
        for record in self:
            record.name = "Something"
        return True

    def cancel_property(self):
        for rec in self:
            rec.status = 'canceled'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click sucess',
                'type': 'rainbow_man'
            }
        }


    def confirm_sale(self):
        for record in self:
            if record.status == 'canceled':
                raise exceptions.UserError("Cannot confirm sale for a canceled item.")
            else:
                record.status='sold'
