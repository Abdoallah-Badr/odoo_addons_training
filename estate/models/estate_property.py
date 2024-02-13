from num2words import num2words

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
        ('canceled', 'Canceled'),
    ], defautl='new', string='Statsu')
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
    price_in_words = fields.Char(string='Price in Words', compute='_compute_price_in_words')

    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

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

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price < 0.9 * rec.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    def _make_offer_readonly(self):
        for rec in self:
            readonly = rec.state in ['offer_accepted', 'sold', 'canceled']
            rec.offer_ids.readonly = readonly

    def write(self, vals):
        # Prevent modification of many2one_field after record creation
        if 'property_type_id' in vals:
            print(vals)
            raise ValidationError("You cannot modify the Many2one field after record creation.")
        return super(EstateProperty, self).write(vals)

    @api.depends('selling_price', 'currency_id')
    def _compute_price_in_words(self):
        for record in self:
            if record.selling_price:
                currency_name = record.currency_id.name or ''
                price_in_words = num2words(record.selling_price, lang='en').title()
                record.price_in_words = f'{price_in_words} {currency_name}'
            else:
                record.price_in_words = ''

    @api.depends('status', 'offer_ids')
    def offer_recived(self):
        for rec in self:
            if len(rec.offer_ids) > 0:
                rec.status = 'offer_recived'
            else:
                rec.status = 'new'

    readonly_offer = fields.Boolean(string='Readonly Offer')

    @api.depends('status')
    def _readonly_status(self):
        for rec in self:
            if rec.status in ('offer_accepted', 'sold', 'canceled'):
                rec.readonly_offer = True
            else:
                rec.readonly_offer = False

    def unlink(self):
        for rec in self:
            if rec.status in ('sold', 'offer_accepted','offer_recived'):
                raise ValidationError('Only new and canceled properties can be deleted.')
        return super().unlink()

