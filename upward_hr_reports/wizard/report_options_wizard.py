from odoo import api, models, fields


class Report_wizard(models.TransientModel):
    _name = 'report.options.wizard'
    _description = 'report options wizard'

    mod_orientation = fields.Selection([('portrait', 'Portrait'), ('landscape', 'Landscape')])

    @api.onchange('mod_orientation')
    def process(self):
        action_record_ref = 'upward_hr_reports.action_upward_employee_report';
        action_record_landscape_ref = 'upward_hr_reports.action_upward_employee_report_landscape';
        active_id = self.env.context.get('active_id')
        employee_record = self.env['hr.employee'].browse(active_id)
        if self.mod_orientation == 'landscape':
            return self.env.ref(action_record_landscape_ref).report_action(employee_record)
        else:
            return self.env.ref(action_record_ref).report_action(employee_record)

