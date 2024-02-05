from odoo import fields,models

class Property(models.Model):
    _name='estate.property'
    _description='property model for estate module'

    title= fields.Char(string='Title',required=True)
    description = fields.Text(string='Description',required=True)
    post_code=fields.Integer(string='Postcode')
    expected_price=fields.Float(string='Expected price')
