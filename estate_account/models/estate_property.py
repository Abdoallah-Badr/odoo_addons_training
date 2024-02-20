from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_sold_action(self):
        for rec in self:
            rec.env['account.move'].create({
                "partner_id": rec.buyer.id,
                "move_type": 'out_invoice',
                "invoice_line_ids": [
                    Command.create({
                        "name": rec.name,
                        "quantity": 1.0,
                        "price_unit": rec.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        "name": 'administrative fees',
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    })
                ]
            })
            res = super().set_sold_action()
            return res
