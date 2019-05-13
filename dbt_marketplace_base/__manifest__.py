{
    'name': 'Dreambits Marketplace Base',
    'version': '11.0.1.0.0',
    'depends': ['dbt_shipment_base'],
    'summary': 'Module to have Shipment and Shipment Transporter Models',
    'description': """
        This module includes base for integrating various marketplaces into the
        existing odoo ecosystem of Sales Orders and Shipments.

        This module is also dependant on another module:
        Dreambits Shipments Base (dbt_shipment_base)

        This module is a must-dependancy for all MarketPlace Integration Modules
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

