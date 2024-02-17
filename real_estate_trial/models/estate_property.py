from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Property(models.Model):
    _name = 'estate.property'
    _description = 'property model for estate module'
    _rec_name = "title"
    _order = 'id desc'

    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description', required=True)
    post_code = fields.Integer(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms', default=2, required=True)
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean(string='Garden')
    garage = fields.Boolean(string='Garage')

    garden_orien = fields.Selection([('west', "West"), ('east', 'East'), ('north', 'North'), ('south', "South")],
                                    readonly=False)
    status = fields.Selection(
        [('new', 'New'), ('received', 'Received'), ('accepted', 'Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default='new', required=True, copy=False)

    active = fields.Boolean(string='Active')
    available_form = fields.Date(string='Available from', copy=False, default=fields.Datetime.now)

    # price fields
    expected_price = fields.Float(string='Expected price')
    best_offer = fields.Float(string='Best offer', default=0, compute='_compute_best_offer')
    sell_price = fields.Float('Selling price', copy=False, readonly=True, )
    # fields.Monetary

    sell_price_inwords = fields.Char('price in words', compute='_compute_amount_to_words')
    # area fields
    living_area = fields.Integer(string='Living area (sqm)')
    garden_area = fields.Integer(string='Garden area (sqm)', readonly=False)
    total_area = fields.Integer(compute='_compute_total_area', string='Total area (sqm)', readonly=True, store=True)

    # related fields
    property_type_id = fields.Many2one('estate.property.type')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', store=True)
    salesman_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                               default=lambda self: self.env.user)

    buyer = fields.Many2one('res.partner', string="Buyer", readonly=False, copy=False)

    state = fields.Selection([('sold', 'Sold'), ('cancel', 'Cancel')])
    _sql_constraints = [
        ('no_of_expected_price_positive', 'CHECK(expected_price > 0)',
         'The property expected price of must be positive.'),
        ('no_of_sell_price_positive', 'CHECK(sell_price > 0)', 'The property sell price of must be positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.onchange('garden')
    def _onchange_garden_defaults(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orien = 'north'
        else:
            self.garden_area = 0
            self.garden_orien = ''

    @api.onchange('offer_ids')
    def _onchange_selling_price(self):
        for rec in self:
            if not rec.offer_ids:
                rec.sell_price = 0
                rec.buyer = ""

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        price_list = []
        for rec in self.offer_ids:
            price_list.append(rec.price)

        if len(price_list) != 0:
            self.best_offer = max(price_list)
        else:
            self.best_offer = 0

    @api.onchange('sell_price')
    def _compute_amount_to_words(self):
        res_currency = self.env.user.company_id.currency_id
        for rec in self:
            rec.sell_price_inwords = res_currency.amount_to_text(rec.sell_price)

    def action_property_sold(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError("Canceled properties can't be sold")
            else:
                rec.state = 'sold'
                rec.status = 'sold'
                return

    def action_property_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError("sold properties can't be canceled")
            else:
                rec.state = 'cancel'
                rec.status = 'canceled'
                return

    @api.ondelete(at_uninstall=False)
    def _unlink_when_state(self):
        for rec in self:
            if rec.status in ('new','canceled'):
                raise UserError("Can't delete while status New or Canceled")
