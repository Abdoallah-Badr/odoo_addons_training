from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class EstateProperty(models.Model):
    _name='estate.property'
    _description='EstatePropertyDescription'

    name=fields.Char(string='title',requried=1,default='new house',size=20)
    postcode=fields.Char(string='Postcode',size=20)
    description=fields.Text(string='Description' )
    date_availability=fields.Date(string='Date Aavailability' )
    expected_price=fields.Float(string='Expected Price',required=True )
    selling_price=fields.Float(string='Selling Price' )
    bedrooms=fields.Integer(string='bedrooms' )
    living_area=fields.Integer(string='Living Area' )
    facades=fields.Integer(string='Facades' )
    garden_area=fields.Integer(string='Garden Area' )
    garage=fields.Boolean(string='arage' )
    garden=fields.Boolean(string='garden' )
    age=fields.Integer(string='Age',default=6)
    gender=fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ])

    # @api.constrains('age')
    # def _check_age(self):
    #     for rec in self:
    #         if rec.age<6:
    #             raise ValidationError(_("students must be older than 6 "))
    #
    # @api.onchange('grade')
    # def check_grade(self):
    #     for rec in self:
    #         if rec.grade in ['fourth', 'fifth', 'sixth']:
    #             rec.is_old=1
    #             print('=================>',rec.is_old)
    #         else:
    #             rec.is_old=0
    #             # print("=========================>",rec.is_old)
    #
    # @api.constrains('num_of_courses')
    # def check_num_of_courses(self):
    #      for rec in self:
    #          if rec.num_of_courses < 6 and rec.is_old:
    #              # print("'==========================>",rec.num_of_courses)
    #              raise ValidationError(_("Students in the fourth grade or above are supposed to take more than 6 subjects "))
    #
    #
    # @api.model
    # def create(self, vals_list):
    #     vals_list['student_seq']=self.env['ir.sequence'].next_by_code('student.sequence')
    #     return super(StudentsManagment,self).create(vals_list)
