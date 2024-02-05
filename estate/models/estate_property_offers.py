from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='.....'

    price=fields.Integer(string='Price',requried=1,default=0)
    validity=fields.Integer(string='Validity',default=7)
    date_deadline=fields.Date(string='Date Deadline',compute='_compute_validation_date',inverse='_inverse',default=datetime.now())
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ],string='Status')
    buyer_id = fields.Many2one('res.partner', string="Buyer",requried=True)
    seller_id = fields.Many2one('res.partner', string="Seller",requried=True)


    property_id=fields.Many2one('estate.property',string="Property")

    @api.depends('validity')
    def _compute_validation_date(self):
        for rec in self:
                if rec.validity:
                    rec.date_deadline = datetime.now() + timedelta(days=rec.validity)
                else:
                    rec.date_deadline=datetime.now()
                    print(rec.date_deadline)

    @api.depends('date_deadline')
    def _inverse(self):
        for record in self:
            start_datetime =datetime.now()
            end_datetime = fields.Datetime.from_string(record.date_deadline)

            # Calculate the difference in days
            difference_days = (end_datetime - start_datetime).days
            record.validity = difference_days