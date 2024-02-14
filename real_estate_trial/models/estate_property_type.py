from odoo import models,fields
class Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'property type model for estate module'
    _order='sequence,name'
    _sql_constraints = [
        ('type_name_unique',
         'unique (name)',
         'A type should define only one time.')
    ]

    name = fields.Char('Property Type',required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence=fields.Integer('Sequence',default=1)