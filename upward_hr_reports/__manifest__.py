# -*- coding: utf-8 -*-
{
    'name': "upward hr report",
    'author': "Upward co.",
    'category': 'hr_reports',
    'version': '17.0',
    'depends': ['base', 'mail', 'hr','hr_contract'],

    'data': [
        'reports/reports.xml',
        'reports/employee_template.xml',
        'reports/contract_template.xml',
    ],
    'installable': True,
}
