from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstateProperty(models.Model):
    _name='estate.property'
    _description='EstatePropertyDescription'

    name=fields.Char(string='Title',requried=1,size=20)
    property_tag_id=fields.Many2many('estate.property.tags',string="Property Type")
    property_type_id=fields.Many2one('estate.property.type',string="Property Type")
    postcode=fields.Char(string='Postcode',size=20)
    buyer_id=fields.Many2one('res.partner',string="Buyer")
    seller_id=fields.Many2one('res.partner',string="Seller")
    description=fields.Text(string='Description' )
    date_availability=fields.Date(string='Date Aavailability' )
    expected_price=fields.Float(string='Expected Price',required=True )
    selling_price=fields.Float(string='Selling Price' )
    bedrooms=fields.Integer(string='bedrooms' )
    living_area=fields.Integer(string='Living Area' )
    facades=fields.Integer(string='Facades' )
    garden_area=fields.Integer(string='Garden Area' )
    garage=fields.Boolean(string='arage' )
    garden=fields.Boolean(string='garden' )
    age=fields.Integer(string='Age',default=6)
    gender=fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ])
    offer_ids=fields.One2many('estate.property.offer','property_id')


