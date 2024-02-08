from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _sql_constraints = [('name_uniq', "unique(name)",
                         f"this property name is already exists")]
