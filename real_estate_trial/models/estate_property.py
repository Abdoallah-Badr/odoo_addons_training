from odoo import fields,models

class Property(models.Model):
    _name='estate.property'
    _description='property model for estate module'

    title= fields.Char(string='Title',required=True)
    description = fields.Text(string='Description',required=True)
    post_code=fields.Integer(string='Postcode')
    expected_price=fields.Float(string='Expected price')
    bedrooms=fields.Integer(string='Bedrooms',default=4 ,required=True)
    facades=fields.Integer(string='Facades')
    garden=fields.Boolean(string='Garden')
    garden_orien=fields.Selection([('west',"West"),('east','East'),('north','North'),('south',"South")])
    active=fields.Boolean(string='Active')
    available_form=fields.Date(string='Available from')
    sell_price=fields.Float('Selling price')
    living_area = fields.Integer(string='Living area (sqm)')
    garage=fields.Boolean(string='Garage')
    garden_area = fields.Integer(string='Garden area (sqm)')
    status = fields.Selection([('still',"Still"),('new','New')])

