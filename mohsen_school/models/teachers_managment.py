from   odoo import models,fields,api
from datetime import date,datetime,timedelta
from  dateutil import  relativedelta
class TeachersManagment(models.Model):
    _name='teachers.managment'
    _description='Teachers Description'

    name=fields.Char(string='Teacher Name',requried=1 )
    summary=fields.Char(string='summary',help="some details for this teacher")
    joinig_date=fields.Date(string='Joning Date')
    years_of_experience=fields.Integer(string="Years Of Experience",compute='_compute_experience')


    _sql_constraints=[
        ('check_name_field','unique (name)','name must be unique')

    ]

    @api.depends('joinig_date')
    def _compute_experience(self):
        for rec in self:
            currentYear=date.today()
            if rec.joinig_date:
                rec.years_of_experience=currentYear.year-rec.joinig_date.year
            else:
                rec.years_of_experience=1


