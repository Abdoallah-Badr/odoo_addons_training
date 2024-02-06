from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='.....'

    price=fields.Integer(string='Price',requried=1,default=0)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ],string='Status')
    buyer_id = fields.Many2one('res.partner', string="Buyer",requried=True)
    seller_id = fields.Many2one('res.partner', string="Seller",requried=True)


    property_id=fields.Many2one('estate.property',string="Property")