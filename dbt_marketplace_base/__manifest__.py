{
    'name': 'Dreambits Marketplace Base',
    'version': '1.0',
    'depends': ['base','stock','sale','dbt_shipment_base'],
    'summary': 'Module to have Shipment and Shipment Transporter Models',
    'description': """
        This module includes base for integrating various marketplaces into the
        existing odoo ecosystem of SO and shipments.

        This module is a must-dependancy for all MarketPlace Integration Module
        By Dreambits.
   """,
    'author': 'Karan Shah/Dreambits Technologies Pvt. Ltd.',
    'category': '',
    'website': 'https://www.dreambits.in',
    'demo': [],
    'data': [
        'views/shipment_view.xml',
        'views/stock_picking_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}

