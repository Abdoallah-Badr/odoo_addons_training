from   odoo import models,fields,api,_
from datetime import date,datetime,timedelta
from odoo.exceptions import ValidationError
class StudentsManagment(models.Model):
    _name='students.managment'
    _description='Stusents Description'

    name=fields.Char(string='Student Name',requried=1,default='new student',size=20)
    student_seq = fields.Char(string='Seq')
    summary=fields.Text(string='Summary' )
    age=fields.Integer(string='Age',default=6)
    gender=fields.Selection([('male','Male'),('female','Female')])
    grade = fields.Selection([
                              ('first', "First Grade"),
                              ('secend', "Secend Grade"),
                              ('third', "Third Grade"),
                              ('fourth', "Fourth Grade"),
                              ('fifth', "Fifth Grade"),
                              ('sixth', "Sixth Grade")],

                                string="Grade",)
    is_old=fields.Boolean(string="Is Old",default=0)

    num_of_courses=fields.Integer(string="Num Of Courses" , default=4)
    state = fields.Selection([('applied','Applied'),('waiting','Waiting'),('accepted','Accepted')],default='applied')
    class_id=fields.Many2one('classroom.managment',string='Class Name')


    _sql_constraints=[
        ('check_name_field','unique (name)','name must be unique')

    ]

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age<6:
                raise ValidationError(_("students must be older than 6 "))

    @api.onchange('grade')
    def check_grade(self):
        for rec in self:
            if rec.grade in ['fourth', 'fifth', 'sixth']:
                rec.is_old=1
                print('=================>',rec.is_old)
            else:
                rec.is_old=0
                # print("=========================>",rec.is_old)

    @api.constrains('num_of_courses')
    def check_num_of_courses(self):
         for rec in self:
             if rec.num_of_courses < 6 and rec.is_old:
                 # print("'==========================>",rec.num_of_courses)
                 raise ValidationError(_("Students in the fourth grade or above are supposed to take more than 6 subjects "))


    @api.model
    def create(self, vals_list):
        vals_list['student_seq']=self.env['ir.sequence'].next_by_code('student.sequence')
        return super(StudentsManagment,self).create(vals_list)
