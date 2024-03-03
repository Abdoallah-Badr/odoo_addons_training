from odoo import api, models, fields


class Report_wizard(models.TransientModel):
    _name = 'report.options.wizard'
    _description = 'report options wizard'

    mod_orientation = fields.Selection([('portrait', 'Portrait'), ('landscape', 'Landscape')])

    @api.onchange('mod_orientation')
    def process(self):
        action_record_ref = 'upward_hr_reports.action_upward_employee_report';
        report_paper_id = self.env.ref(action_record_ref).read()[0].get('paperformat_id')[0]
        action_record_ref = 'upward_hr_reports.action_upward_employee_report_landscape';
        active_id = self.env.context.get('active_id')
        employee_record = self.env['hr.employee'].browse(active_id)
        if self.mod_orientation == 'landscape':
            self.env['report.paperformat'].browse(report_paper_id).write({'orientation': 'Landscape','dpi':80})
        else:
            self.env['report.paperformat'].browse(report_paper_id).write({'orientation': 'Portrait'})

        return self.env.ref(action_record_ref).report_action(employee_record)
