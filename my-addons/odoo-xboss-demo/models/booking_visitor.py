from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class Visitor(models.Model):
    _name = 'booking.visitor'
    _description = 'Visitor'

    #Property
    name = fields.Char(string='Name', required=True, default='Unknown')
    company = fields.Char(string='Visitor\'s Company', default='Unknown')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    host = fields.Many2one('res.users', string='Host Name', required=True)
    checkin = fields.Datetime(string='Check In', default=lambda self: datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    # duration = fields.Integer(string='Duration', default=datetime.fromtimestamp(100000).strftime('%H:%M'))
    duration = fields.Integer(string='Duration', default=1)
    statusCheckin = fields.Selection(
        string='Status',
        selection=[
            ('planned', 'Planned'),
            ('checkedin', 'Checked-In'),
            ('checkedout', 'Checked-Out'),
            ('cancelled', 'Cancelled'),
        ],
        default='planned'
    )
    isServeDrink = fields.Boolean(string='Drink Served', default=False)
    station_id = fields.Many2one('booking.station', string='Station')
    drinks_id = fields.Many2many('booking.drink', string='Drinks')

    def action_checkout(self):
        for obj in self:
            if obj.statusCheckin != 'checkedin':
                raise exceptions.UserError('Only can Check Out while Check In')
            obj.statusCheckin = 'checkedout'

    def action_serve_drink(self):
        for obj in self:
            obj.isServeDrink = True

    @api.model
    def create(self, vals):
        # For Sending Email
        record = super(Visitor, self).create(vals)

        if record.station_id and record.station_id.isEmailNotify:
            # Take email from host
            if record.host and record.host.email:
                template = self.env.ref('odoo-xboss-demo.email_template_booking')

                if template:
                    # template.email_to = record.host.email
                    template.send_mail(record.id, force_send=True)
                else:
                    print('No email template found')

        # Send notification
        # self._send_notification(record)

        return record

    # def send_notification(self):
    #     bus = self.env['bus.bus']
    #     message = {
    #         # 'type': 'visitor_notification',
    #         # 'model': 'booking.visitor',
    #         # 'id': record.id,
    #         # 'name': record.name,
    #         'title': 'Warning',
    #         'message': 'Hello',
    #         'sticky': True,
    #         'warning': True,
    #     }
    #
    #     obj = bus._sendone(self.env.user.partner_id, 'hello_notfi', message)
    #     print(obj)

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'message': 'Hello',
        #         'type': 'success',
        #         'sticky': True,
        #     }
        # }