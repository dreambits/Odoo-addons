#/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class ManualShipmentTransporter(models.Model):
    _inherit = "dbt.shipment.transporter"
    _description = "Dbt shipment transporter: Model stores shipment transporter"

    def manual_label_get(self, picking):
        _logger.info("In manual mode, you don't need to generate label")
        _logger.info("We get the picking and that is fine as \
                     we don't have much to do with the SO anyways ")
        _logger.info(picking.name)

    def manual_label_output_get(self, picking):
        _logger.info("But here we test the process to calling the methods")
