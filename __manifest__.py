{
    'name': "Real Estate",
    'description': "task of odoo17 documentation",
    'author': "Upward - H",
    'website': "",
    'version': "17.0.1.0",
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        # "security/security.xml",
        "views/real_state_view.xml",
        "views/estate_propert_type_view.xml",
        "views/estate_propert_tag_view.xml",
        "views/base_menu.xml",
    ],
    'application': True,
    'category': 'Uncategorized',
}
