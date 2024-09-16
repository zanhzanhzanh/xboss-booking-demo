from odoo import models, fields, api

class Station(models.Model):
    _name = 'booking.station'
    _description = 'Station'
    
    #Property
    name = fields.Char(string='Frontdesk Name', required=True, default='Unknown')
    reponsibles_id = fields.Many2one('res.users', string='Reponsibles')
    company_id = fields.Many2one('res.company', string='Company')
    kloskUrl = fields.Char(string='Klosk URL')
    
    isHostSeletion = fields.Boolean(string='Host Selection', default=True)
    isAuthGuest = fields.Boolean(string='Authenticate Guest', default=True)
    emailAuth = fields.Selection(
        string='Email',
        selection=[
            ('required', 'Required'),
            ('optional', 'Optional'),
            ('none', 'None'),
        ],
        default='optional'
    )
    phoneAuth = fields.Selection(
        string='Phone',
        selection=[
            ('required', 'Required'),
            ('optional', 'Optional'),
            ('none', 'None'),
        ],
        default='optional'
    )
    organizationAuth = fields.Selection(
        string='Organization',
        selection=[
            ('required', 'Required'),
            ('optional', 'Optional'),
            ('none', 'None'),
        ],
        default='optional'
    )
    isEmailNotify = fields.Boolean(string='Notify by email', default=True)
    isSmsNotify = fields.Boolean(string='Notify by SMS', default=True)
    isSelfCheckin = fields.Boolean(string='Self Check-In', default=True)
    isOfferDrinks = fields.Boolean(string='Offer Drinks', default=True)
    isDicussNotify = fields.Boolean(string='Notify by dicuss', default=True)
    theme = fields.Selection(
        string='Theme',
        selection=[
            ('light', 'Light'),
            ('dark', 'Dark'),
        ],
        default='light'
    )
    
    drinks_id = fields.Many2many('booking.drink', string='Drinks')
    visitor_ids = fields.One2many('booking.visitor', 'station_id', string='Visitors')

    # Compute Field
    visitor_count = fields.Integer(string='Total Visitors', compute='_compute_visitor_count')
    planned_count = fields.Integer(string='Planned Visitors', compute='_compute_planned_count')
    drinks_to_serve_count = fields.Integer(string='Drinks to Serve', compute='_compute_drinks_to_serve_count')
    last_checkin = fields.Datetime(string='Last Check-In', compute='_compute_last_checkin')

    # Open Desk
    def action_open_desk(self):
        self.ensure_one()
        station_id = self.ids

        return {
            'type': 'ir.actions.act_url',
            'url': f'desk?station_id={station_id}',
            'target': 'new',
        }

    @api.depends('visitor_ids')
    def _compute_visitor_count(self):
        for record in self:
            record.visitor_count = self.env['booking.visitor'].search_count([('station_id', '=', record.id)])

    @api.depends('visitor_ids')
    def _compute_planned_count(self):
        for record in self:
            record.planned_count = self.env['booking.visitor'].search_count([
                ('station_id', '=', record.id),
                ('statusCheckin', '=', 'planned')
            ])

    @api.depends('visitor_ids')
    def _compute_drinks_to_serve_count(self):
        for record in self:
            record.drinks_to_serve_count = self.env['booking.visitor'].search_count([
                ('station_id', '=', record.id),
                ('isServeDrink', '=', False)
            ])

    @api.depends('visitor_ids.checkin')
    def _compute_last_checkin(self):
        for record in self:
            last_checkin_visitor = self.env['booking.visitor'].search([
                ('station_id', '=', record.id),
                ('checkin', '!=', False)
            ], order='checkin desc', limit=1)
            record.last_checkin = last_checkin_visitor.checkin if last_checkin_visitor else False