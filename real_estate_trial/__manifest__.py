# -*- coding: utf-8 -*-
{
    'name': "Real Estate",
    'summary': " Manage your properties ",
    'description': """
        School module for managing your properties:
            - produces your properties
            - negotiate with clients
            - analyze clients
    """,

    'author': "Upward co.",
    'category': 'estate',
    'version': '17.0',
    'depends': ['base'],

    'data': [
         'security/ir.model.access.csv',
         'views/module_main_views.xml',
    ],
    # 'assets': {'web.assets_backend':['static/src/css/styles.css']},
    'installable':True,
}