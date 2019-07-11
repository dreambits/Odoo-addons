#  /usr/bin/env python
#  -*- coding: utf-8 -*-

from odoo import models,  fields,  api
import logging

_logger = logging.getLogger(__name__)
class Company(models.Model):
    _inherit = "res.company"

    shipment_picking_type_id = fields.Many2one('stock.picking.type', required=1, oldname="shippment_picking_type_id")
