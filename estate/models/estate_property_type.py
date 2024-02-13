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
    offer_ids=fields.One2many('estate.property.offer','property_type_id',string='Offers IDs')
    offer_count=fields.Integer(compute='_count_offers',string='Offer Counts')

    @api.depends('offer_ids')
    def _count_offers(self):
        for rec in self:
            rec.offer_count=len(rec.offer_ids)

