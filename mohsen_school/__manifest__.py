# -*- coding: utf-8 -*-
{
    'name': "Mohsen School",

    'summary': "an application to manage schools teachers,students,class,courses",

    'description': """
L       ong description of module's purpose
    """,

    'author': "mohsen",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/courses_view.xml',
        'views/teachers_view.xml',
        'views/estate_property_view.xml',
        'views/classroom_view.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
}

