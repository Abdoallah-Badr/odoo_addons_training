from odoo import fields, models, api


class Property(models.Model):
    _name = 'estate.property'
    _description = 'property model for estate module'

    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description', required=True)
    post_code = fields.Integer(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms', default=2, required=True)
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean(string='Garden')

    garden_orien = fields.Selection([('west', "West"), ('east', 'East'), ('north', 'North'), ('south', "South")],compute='_compute_graden_defaults', readonly=False)
    status = fields.Selection([('new', 'New'), ('received', 'Received'), ('accepted', 'Accepted'), ('sold', 'Sold'),('canceled', 'Canceled')], required=True)

    active = fields.Boolean(string='Active')
    available_form = fields.Date(string='Available from', copy=False, default=fields.Datetime.now)

    #price fields
    expected_price = fields.Float(string='Expected price')
    best_offer = fields.Float(string='Best offer',compute='_compute_best_offer')
    sell_price = fields.Float('Selling price', copy=False)

    garage = fields.Boolean(string='Garage')

    # area fields
    living_area = fields.Integer(string='Living area (sqm)')
    garden_area = fields.Integer(string='Garden area (sqm)', compute='_compute_graden_defaults', readonly=False)
    total_area = fields.Integer(compute='_compute_total_area', string='Total area (sqm)', readonly=True)


    # related fields
    property_type_id = fields.Many2one('estate.property.type')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string=' ')
    salesman = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                               default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)

    @api.onchange('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.onchange('garden')
    def _compute_graden_defaults(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orien = 'north'
        else:
            self.garden_area = 0
            self.garden_orien = ''

    @api.onchange('offer_ids')
    def _compute_best_offer(self):
        price_list = []
        for rec in self.offer_ids:
            price_list.append(rec.price)

        if len(price_list) != 0:
            self.best_offer = max(price_list)
