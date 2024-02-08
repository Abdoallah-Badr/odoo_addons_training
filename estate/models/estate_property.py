from odoo import models, fields, api, _, exceptions
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstatePropertyDescription'
    _order = "id desc"

    name = fields.Char(required=True, size=20, string='Title')
    status = fields.Selection([
        ('new', 'New'),
        ('offer_recived', 'OFFER RECIVED'),
        ('offer_accepted', 'OFFER ACCEPTED'),
        ('sold', 'Sold'),
        ('draft', 'Draft'),
        ('canceled', 'Canceled'),
    ], string='Statsu')
    property_tag_id = fields.Many2many('estate.property.tags', string="Property Tag")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    postcode = fields.Char(string='Postcode', size=20)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.partner', string="Seller")
    description = fields.Text(string='Description')
    date_availability = fields.Date(string='Date Aavailability')
    expected_price = fields.Float(required=True, string='Expected Price', )
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
    type_id = fields.Many2one('estate.property.type', string='Offers Type')

    _sql_constraints = [
        ('check_price', 'CHECK(expected_price > 0 AND selling_price > 0 )',
         'Price must be greater than zero.'),
        ('property_name_must_unique', 'unique(name)', 'Property name already exists')
    ]

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
                record.status = 'sold'

    @api.depends('')
    def confirm_price(self):
        for rec in self:
            if rec.offer_ids.status == 'accepted':
                rec.selling_price = rec.offer_ids.price
            else:
                rec.selling_price = 0

    def accept_offer(self):
        searched = self.env['estate.property'].search([])
        for rec in self:
            mapped = rec.offer_ids.mapped('status')
            if 'accepted' in mapped:
                print()

        # mapped = searched.mapped('offer_ids')
        # print('gj;kedgjkfdgjk;', mapped)
        # # if 'accepted' in mapped:
        # #     raise exceptions.UserError("Cannot accept this offer as u already accept one.")
        # # else:
        # #     for rec in self:
        # #         rec.status='accepted'

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price < 0.9 * rec.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
