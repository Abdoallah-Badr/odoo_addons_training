from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = '.....'
    _order = "price desc"

    price = fields.Integer(string='Price', requried=True)
    state = fields.Selection([
        ('accepted', 'Accepted'),
        ('draft', 'Draft'),
        ('refused', 'Refused'),
    ], string='Status', default='draft')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date Deadline', compute='_compute_validation_date', inverse='_inverse',
                                default=datetime.now())
    buyer_id = fields.Many2one('res.partner', string="Buyer", requried=True)
    seller_id = fields.Many2one('res.partner', string="Seller", requried=True, compute='_determine_seller',
                                readoonly=False)

    property_id = fields.Many2one('estate.property',requried=True, string="Property")
    property_type_id=fields.Many2one("estate.property.type", related='property_id.property_type_id' , string='Property Type ID' ,store=1)

    @api.depends('property_id')
    def _determine_seller(self):
        for rec in self:
            rec.seller_id = rec.property_id.seller_id

    @api.depends('validity')
    def _compute_validation_date(self):
        for rec in self:
            if rec.validity:
                rec.date_deadline = datetime.now() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = datetime.now()
                print(rec.date_deadline)

    @api.depends('date_deadline')
    def _inverse(self):
        for record in self:
            start_datetime = datetime.now()
            end_datetime = fields.Datetime.from_string(record.date_deadline)

            # Calculate the difference in days
            difference_days = (end_datetime - start_datetime).days
            record.validity = difference_days

    def accept_offer(self):
        for offer in self:
            if offer.state != 'draft':
                raise exceptions.ValidationError("This offer cannot be accepted.")
            property_offers = self.env['estate.property.offer'].search(
                [('property_id', '=', offer.property_id.id), ('state', '=', 'accepted')])
            print('_________________________________________________________________________-')
            print('all offers  ==>  ', self.env['estate.property.offer'].search([]))
            print('offers for selected property only  ==>  ',
                  self.env['estate.property.offer'].search([('property_id', '=', offer.property_id.id)]))
            print('property_id  ==>  ', offer.property_id)
            print('property_id.d  ==>  ', offer.property_id.id)
            print('_________________________________________________________________________-')

            if property_offers:
                print('before raising error')
                raise exceptions.ValidationError("Another offer has already been accepted for this property.")
            offer.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.buyer_id.id
            offer.property_id.status = 'offer_accepted'
            print('offer.property_id.buyer_id=====>',offer.property_id.buyer_id)
            print('buyer_id.id=====>',offer.buyer_id.id)
            print('buyer_id=====>',offer.buyer_id)

    def refuse_offer(self):
        for offer in self:
            if offer.state != 'draft':
                raise exceptions.ValidationError("This offer cannot be refused.")
            offer.state = 'refused'

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0 )',
         'Price must be greater than zero.'),
    ]




    @api.onchange('property_id.status')
    def _onchange_property_state(self):
        for offer in self:
            if offer.property_id.state in ('offer_accepted', 'sold', 'canceled'):
                offer.property_id.readonly = True
            else:
                offer.property_id.readonly = False

