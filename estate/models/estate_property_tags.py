from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstatePropertyTags(models.Model):
    _name='estate.property.tags'
    _description='descripe tags of property coze  or .....'
    _order = "name"

    name=fields.Char(string='Name',requried=1,default='new house',size=20)

