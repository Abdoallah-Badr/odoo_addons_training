from odoo import models,fields,api
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

    # property_offer_ids = fields.One2many('estate.property.offer','property_type_id')
    # offer_count = fields.Integer(compute='_compute_offer_count',default=0,store=True)


    # @api.depends('property_offer_ids')
    # def _compute_offer_count(self):
    #     for rec in self:
    #         offers_length = len(rec.property_offer_ids)
    #         rec.offer_count = offers_length