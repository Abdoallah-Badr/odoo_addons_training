from odoo import models,fields

class Property(models.Model):
    _name ='realestate.property',
    _description = " property models for realestate module "

    property_id = fields.Char(string='Property ID',required=True)
    description = fields.Text(string='Description',required=True)

