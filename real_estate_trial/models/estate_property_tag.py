from odoo import models,fields
class Property_Tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'property tag model for estate module'

    name = fields.Char('Property tag',required=True)

