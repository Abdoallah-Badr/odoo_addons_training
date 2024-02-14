from odoo import models,fields
class Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'property type model for estate module'

    name = fields.Char('Property Type',required=True)

    _sql_constraints = [
        ('type_name_unique',
         'unique (name)',
         'A type should define only one time.')
    ]