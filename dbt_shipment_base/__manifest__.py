{
    'name': 'Dreambits Shipments Base',
    'version': '1.0',
    'depends': ['base','stock','sale'],
    'summary': 'Module to have Shipment and Shipment Transporter Models',
    'description': """
        This module includes shipment and shipment transporter models which will
        be linked to all SO coming from MarketPlaces.

        This module is a must-dependancy for all MarketPlace Integration Module
        By Dreambits.
   """,
    'author': 'Karan Shah/Dreambits Technologies Pvt. Ltd.',
    'category': '',
    'website': 'https://www.dreambits.in',
    'demo': [],
    'data': [
        'views/shipment_view.xml',
        'views/shipment_transporter_view.xml',
        'data/dbt.shipment.transporter.csv',
        'views/shipment_sequence.xml',
        'views/stock_picking_view.xml',
        'views/shipment_scheduler.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}

