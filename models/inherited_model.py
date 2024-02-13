from odoo import models, fields


class InheritModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesman")
