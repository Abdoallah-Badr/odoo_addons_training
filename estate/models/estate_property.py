from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstatePropertyDescription'

    name = fields.Char(string='Title', requried=1, size=20)
    property_tag_id = fields.Many2many('estate.property.tags', string="Property Type")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    postcode = fields.Char(string='Postcode', size=20)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.partner', string="Seller")
    description = fields.Text(string='Description')
    date_availability = fields.Date(string='Date Aavailability')
    expected_price = fields.Float(string='Expected Price', required=True)
    best_price = fields.Float(string='Best Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='bedrooms')
    living_area = fields.Integer(string='Living Area', default=0)
    facades = fields.Integer(string='Facades')
    garden_area = fields.Integer(string='Garden Area', default=0)
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='garden')
    age = fields.Integer(string='Age', default=6)
    gender = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price', store=True,default=0)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area



    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            # print(rec.offer_ids.mapped('price'))
            # print(max(rec.offer_ids.mapped('price')))
            rec.best_price = max(rec.offer_ids.mapped('price'),default=0)


