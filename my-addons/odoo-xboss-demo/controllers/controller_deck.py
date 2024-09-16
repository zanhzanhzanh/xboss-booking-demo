from odoo import http
from odoo.http import request
from qrcode.main import QRCode
import base64
from io import BytesIO

class DeskController(http.Controller):
    @http.route('/desk', methods=['GET'], auth='public', website=True)
    def odoo_deck(self, **kwargs):
        station_id = kwargs.get('station_id')
        station = request.env['booking.station'].sudo().browse(int(station_id[1]))

        if not station.exists():
            return request.redirect('/page/404')

        #Generate QR
        qr_image= self._generate_qr()

        return request.render('odoo-xboss-demo.booking_desk_views', {
            'station': station,
            'qr_image': qr_image,
        })

    @http.route('/desk-form', methods=['GET'], auth='public', website=True)
    def odoo_deck_form(self, **kwargs):
        station_id = kwargs.get('station_id')
        station = request.env['booking.station'].sudo().browse(int(station_id[1]))

        if not station.exists():
            return request.redirect('/page/404')

        return request.render('odoo-xboss-demo.booking_desk_form_views', {
            'allowHost':  station.isHostSeletion,
            'allowEmail': station.emailAuth if station.isAuthGuest else None,
            'allowPhone': station.phoneAuth if station.isAuthGuest else None,
            'allowOrganization': station.organizationAuth if station.isAuthGuest else None,
            'users': station.reponsibles_id,
        })

    @http.route('/desk-ask', methods=['GET'], auth='public', website=True)
    def odoo_deck_ask(self, **kwargs):
        drinks = request.env['booking.drink'].sudo().search([])

        if not drinks.exists():
            return request.redirect('/page/404')

        return request.render('odoo-xboss-demo.booking_desk_ask_views', {
            'drinks': drinks,
        })

    @http.route('/desk-success', methods=['GET'], auth='public', website=True)
    def odoo_deck_success(self, **kwargs):
        return request.render('odoo-xboss-demo.booking_desk_success_views')

    def _generate_qr(self):
        # Take URL
        path = http.request.httprequest.path
        query_string = http.request.httprequest.query_string.decode('utf-8')
        url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + path + '?' + query_string

        # Config QR code
        qr = QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)

        # Generate QR code
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return qr_image