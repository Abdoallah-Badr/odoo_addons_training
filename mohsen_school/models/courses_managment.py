from   odoo import models,fields,api

class CoursesManagment(models.Model):
    _name='courses.managment'
    _description='Course Description'

    name=fields.Char(string='Course Name')
    lectures=fields.Char(string='Num of Licture')
