from odoo import models,fields
class Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'property type model for estate module'

    name = fields.Char('Property Type',required=True)

