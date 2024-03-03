# -*- coding: utf-8 -*-
{
    'name': "upward hr report",
    'author': "Upward co.",
    'category': 'hr_reports',
    'version': '17.0',
    'depends': ['base', 'mail', 'hr', 'hr_contract'],

    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'data/report_paperformat_landscape.xml',
        'wizard/wizard_view.xml',
        'reports/reports.xml',
        'reports/employee_template.xml',
        'reports/contract_template.xml',
        'reports/employee_template_landscape.xml'

    ],

    'assets': {
        'web.assets_backend': [
            'upward_hr_reports/static/src/css/table_style.scss',
        ]
    }
    ,

    'installable': True,
}
