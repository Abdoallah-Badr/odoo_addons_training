from odoo import models,fields,api
import datetime
class Property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer model for estate module'

    price = fields.Float('Price')
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],string='Status',copy=False)
    partner_id = fields.Many2one('res.partner',string="Partner",required=True)
    property_id=fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string='Validity',default=7)
    deadline = fields.Date(string='Deadline')

    @api.onchange('validity')
    def _compute_deadline(self):
        self.deadline = datetime.date.today()+ datetime.timedelta(days=self.validity)
