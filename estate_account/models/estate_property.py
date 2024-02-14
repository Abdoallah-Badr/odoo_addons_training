from odoo import models, fields, api, _, exceptions, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'


    def confirm_sale(self):
        for rec in self:
            rec.env["account.move"].create(
                {
                    "partner_id": rec.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": rec.name ,
                            "quantity": 1,
                            "price_unit": rec.selling_price * .06,
                        }),
                        Command.create({
                            "name": "administrative fees" ,
                            "quantity": 1,
                            "price_unit": 100,
                        }),
                    ],

                }
            )
            return super().confirm_sale()
