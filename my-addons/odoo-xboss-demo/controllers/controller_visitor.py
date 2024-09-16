from odoo import http
from odoo.http import request
import re

class VisitorController(http.Controller):
    @http.route('/visitor/create', methods=['POST'], type='json', auth='public')
    def create_visitor(self, **kwargs):
        visitor_data = {
            'name': kwargs.get('name', 'Unknown'),
            'company': kwargs.get('company', 'Unknown'),
            'phone': kwargs.get('phone'),
            'email': kwargs.get('email'),
            'host': kwargs.get('host'),
            'statusCheckin': 'planned',
            'isServeDrink': kwargs.get('isServeDrink', False),
            'station_id': kwargs.get('station_id'),
            'drinks_id': [(6, 0, kwargs.get('drinks_id', []))],
        }

        # Check Valid
        validation_response = self._valid_data(visitor_data)
        if validation_response:
            return validation_response

        visitor = request.env['booking.visitor'].sudo().create(visitor_data)
        # print(visitor_data)

        return {
            'status': 'Success',
            'message': 'Visitor created',
            'data': visitor,
        }

    # Validation Data
    def _valid_data(self, visitor_data):
        # Validate phone
        phone = visitor_data.get('phone')
        if phone and not re.match(r'(84|0[3|5|7|8|9])+([0-9]{8})\b', phone):
            return self._error_response('Invalid phone number')

        # Validate email
        email = visitor_data.get('email')
        if email and not re.match(r'^\S+@\S+\.\S+$', email):
            return self._error_response('Invalid email address')

        # Check Exist Host
        host_id = visitor_data.get('host')
        host = request.env['res.users'].sudo().browse(host_id)
        if not host.exists():
            return self._error_response('Host not found')

        # Check Exist Station
        station_id = visitor_data.get('station_id')
        station = request.env['booking.station'].sudo().browse(station_id)
        if not station.exists():
            return self._error_response('Station not found')

        # Check Exist Drinks
        drinks_id = visitor_data.get('drinks_id', [])[0][2]
        if drinks_id:
            for drink in drinks_id:
                foundDrink = request.env['booking.drink'].sudo().browse(drink)
                if not foundDrink.exists():
                    return self._error_response('Some drinks not found')

        return None

    def _error_response(self, message):
        return {
            'status': 'Failed',
            'message': message,
        }
