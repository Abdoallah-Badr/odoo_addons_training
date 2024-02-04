from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='descripe type of property house or castle or .....'

    name=fields.Char(string='Porperty Type',requried=1,size=20)
