# -*- coding: utf-8 -*-
{
    'name': "Xboss - demo",

    'description': """ """,

    'author': "Zanh",

    'category': 'Tutorials/Demo',
    
    'version': '0.1',

    'depends': ['base', 'mail', 'bus'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/booking_station_views.xml',
        'views/booking_menus.xml',
        'views/booking_visitor_views.xml',
        'views/booking_drink_views.xml',
        'views/booking_desk_views.xml',
        'views/booking_desk_form_views.xml',
        'views/booking_desk_ask_views.xml',
        'views/booking_desk_success_views.xml',
        'views/booking_drink_graph.xml',
        'data/email_template_data.xml',
        # 'views/js_loader.xml',
        # 'views/css_loader.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo-xboss-demo/static/src/css/booking_station_views.css',
        ],
        'web.assets_frontend': [
            'odoo-xboss-demo/static/src/js/*',
        ],
    }
}
