# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': "an application to manage apartment ",

    'description': """
L       ong description of module's purpose
    """,

    'author': "mohsen",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offers_view.xml',
        'views/inherited_model_view.xml',
        'views/reports.xml',
        'views/penalties_and_rewards_template_view.xml',
        'views/vacation_request_template_veiw.xml',
        'views/long_vacation_request_template_view.xml',
        'views/money_refound_template_view.xml',
        'views/my_groups.xml',



    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
    'sequence': -330,
}
