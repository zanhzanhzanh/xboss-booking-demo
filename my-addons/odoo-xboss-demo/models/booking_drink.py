from odoo import models, fields

class Drink(models.Model):
    _name = 'booking.drink'
    _description = 'Drink'

    #Property
    name = fields.Char(string='Drink Name', required=True)
    color = fields.Integer(string='Color', required=True)
    image = fields.Binary(string='Image')

    _sql_constraints = [
        ('unique_drink_name', 'UNIQUE(name)', 'The drink name must be unique.')
    ]