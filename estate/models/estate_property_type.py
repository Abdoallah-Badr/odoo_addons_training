from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='descripe type of property house or castle or .....'
    _order = "name"

    name=fields.Char(string='Porperty Type',requried=1,size=20)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property','type_id', string="Properties")

