from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class ClassroomManagment(models.Model):
    _name = 'classroom.managment'
    _description = 'Classroom Description'

    name = fields.Char(string='Class Name', requried=1)
    summary = fields.Char(string='summary')
    num_of_students = fields.Integer(string='Num Of Students', compute='_calc_num_of_students', store=1)
    student_ids = fields.One2many('students.managment', 'class_id', string="Class students")

    @api.depends('student_ids')
    def _calc_num_of_students(self):
        for rec in self:
            rec.num_of_students = len(rec.student_ids)

    @api.constrains('num_of_students')
    def _max_num_of_students(self):
        for rec in self:
            if rec.num_of_students > 20:
                raise ValidationError(_("The Class is Compeleted, Please add this in another class"))
