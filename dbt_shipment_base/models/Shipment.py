#  /usr/bin/env python
#  -*- coding: utf-8 -*-

from odoo import models,  fields,  api
import logging

_logger = logging.getLogger(__name__)


class Shipment(models.Model):
    _name = 'dbt.shipment'

    _inherits = {
        'sale.order': 'associated_sale'
    }

    name = fields.Char('Name')
    created_by = fields.Char('Created By')
    shipment_id = fields.Char('Shipment ID')

    transporter = fields.Many2one('dbt.shipment.transporter',
                                  string='Transporter')

    label_file = fields.Binary('Label')
    label_filename = fields.Char('Label File Name')

    input_file_name = fields.Char('Input File Name')
    input_file_content = fields.Text('Input File Contents')
    output_file_name = fields.Char('Output File Name')
    output_file_content = fields.Text('Output File Contents')
    log_file_name = fields.Char('Log File Name')
    log_file_content = fields.Text('Log File Contents')
    error_file_name = fields.Char('Error File Name')
    error_file_content = fields.Text('Error File Contents')

    awb_number = fields.Char("Airway Bill Number")
    state = fields.Selection([
        ('ready', 'Ready for packing'),
        ('packing', 'Packing'),
        ('wait_label', 'Waiting for Label'),
        ('ready_shipment', 'Ready for shipment'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('error', 'Error'),
    ])
    label_state = fields.Selection([
        ('waiting', 'Waiting'),
        ('generated', 'Generated'),
        ('sent', 'Sent'),
        ('printed', 'Printed'),
        ('error', 'Error'),
    ])

    associated_sale = fields.Many2one('sale.order',
                                      string='Associated Sales Order',
                                      required=True,  ondelete='cascade')
    associated_pickings = fields.One2many('stock.picking',
                                          'associated_shipment',
                                          string='Associated Stock Pickings')

    ready_for_sync = fields.Boolean('Ready for Sync')
    synced = fields.Boolean('Synced')

    @api.model
    def create(self,  vals):
        _logger.info("inside set name")
        name = self.env['ir.sequence'].next_by_code('dbt.shipment')

        vals["name"] = name
        vals["state"] = "ready"
        vals["label_state"] = "waiting"
        return super(Shipment,  self).create(vals)

    @api.model
    @api.multi
    def name_get(self):
        _logger.info("Inside name_get fn")
        result = []
        for record in self:
            name = "{} | {} | {}".format(
                record.name,
                record.transporter.name if record.transporter.name else "None",
                record.associated_sale.name)
            result.append((record.id,  name))
        return result

    @api.depends('associated_sale')
    def get_pickings(self):
        #  we get the SO and find the relevant pickings and associated them
        so = self.associated_sale
        if so and so.picking_ids:
            self.associated_pickings = (6, False, so.picking_ids)

    def update_state(self):
        #  get all the shipments who are in state of wait_label and whose
        #  label_state is set to generated or sent.

        _logger.info("Inside scheduler to get output of shipments")
        pending_shipments = self.env["dbt.shipment"].search([
            ('state', 'in', ('wait_label', 'ready_shipment', 'done')),
            ('label_state', 'in', ['generated', 'sent'])
        ])

        #  we invoke the output_method
        for shipments in pending_shipments:
            _logger.info("Shipment: " + str(shipments.name)
                         + ": calling output method from scheduler")
            transporter = shipments.transporter
            output_method = getattr(transporter,  transporter.get_output_method)
            output_method(self.associated_shipment)

    def action_sync(self):
        self.ready_for_sync = True


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    associated_shipment = fields.Many2one('dbt.shipment', 'Shipment')
    transporter = fields.Selection(string='Transporter',
                                   selection='get_transporters')

    @api.model
    def get_transporters(self):
        transporters = self.env['dbt.shipment.transporter'].search([])

        name_list = []

        for t in transporters:
            name_list.append((t.transporter_code, t.name))

        return name_list

    @api.multi
    def action_confirm(self):
        res = super(CustomSaleOrder, self).action_confirm()
        self.create_shipment()
        return res

    @api.multi
    def write(self, vals):
        res = super(CustomSaleOrder, self).write(vals)

        dependant_fields = [
            "transporter",
            "picking_ids",
            "state",
            "procurement_group_id",
            "order_line"
        ]
        _logger.info("Writing vals for SO")
        _logger.info(vals)

        if any(v in dependant_fields for v in list(vals.keys())):
            self.create_shipment()
        return res

    def create_shipment(self):
        # lets get the tranporter and make the relevant

        # lets get the state. If it is confirmed SO then also proceed
        state = self.state
        if state == "sale":
            # lets check if shipment is already available or not
            shipment = self.associated_shipment
            _logger.info(shipment)

            if not shipment:
                # lets try to find any shipment having this SO associated to it
                search_shipment = self.env['dbt.shipment'].search([
                    ('associated_sale', '=', self.id)
                ])
                if search_shipment:
                    shipment = search_shipment[0]

                else:
                    values = {
                        'associated_sale': self.id,
                    }
                    shipment = self.env['dbt.shipment'].create(values)

                transporter_id = self.env['dbt.shipment.transporter'].search([
                    ('transporter_code', '=', self.transporter)
                ])
                if transporter_id:
                    shipment.transporter = transporter_id.id

                _logger.info("Setting shipment in SO")
                _logger.info(self)
                _logger.info(shipment)
                self.associated_shipment = shipment

            # lets see if picking_ids is added
            _logger.info("Setting pickingS")
            _logger.info(self.picking_ids)

            pickings = [x if isinstance(x, int) else x.id
                        for x in self.picking_ids]
            _logger.info(pickings)
            if pickings:
                shipment.associated_pickings = [(6, False, pickings)]


class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'
    associated_shipment = fields.Many2one('dbt.shipment', 'Shipment')

    @api.multi
    def action_done(self):
        prev = super(CustomStockPicking, self).action_done()
        _logger.info("We are now inside stock picking")

        company = self.env['res.company']._company_default_get('stock.picking')
        picking_type = company.shippment_picking_type_id.id
        _logger.info("picking_type-> {0}".format(picking_type))

        if self.picking_type_id.id == picking_type:
            transporter = self.associated_shipment.transporter
            _logger.info("this is delivery and this is its courier decided")
            _logger.info(transporter)
            _logger.info("Lets see if this transporter has any methods or not")
            generate_method = transporter.generate_file_method
            output_method = transporter.get_output_method

            _logger.info(generate_method)
            _logger.info(output_method)

            if transporter.transporter_type == "manual":
                _logger.info("Manual transportation so no label is generated")
                self.associated_shipment.state = "ready_shipment"
            else:
                #  The transporter's method need to update label state and
                # state of shipment
                _logger.info("now lets call this methods")
                #  we are sending the stock picking object while calling the
                #  method so it should get the relevant shipment and keep it
                #  updated
                if generate_method and not generate_method == "":
                    input_function = getattr(transporter,  generate_method)
                    input_function(self)

                if output_method and not output_method == "":
                    output_function = getattr(transporter,  output_method)
                    output_function(self.associated_shipment)
        return prev

    @api.multi
    def write(self, vals):
        _logger.info("inside stock picking write")
        _logger.info(self)
        _logger.info(vals)

        result = super(CustomStockPicking,  self).write(vals)
        for rec in self:

            _logger.info(rec)
            shipment = rec.associated_shipment
            if shipment:

                # lets check the state and type now
                _logger.info(rec.picking_type_id)
                _logger.info(rec.state)

                company = self.env['res.company']._company_default_get('stock.picking')
                picking_type = company.shippment_picking_type_id.id
                _logger.info("picking_type-> {0}".format(picking_type))
                # when the packing stock.picking is available then state should
                # be changed to 'ready'
                if rec.picking_type_id.id == picking_type:
                    if rec.state == "assigned":
                        shipment.state = "ready"

                        #  when the any of pack_operation_ids.qty_done
                        # is updated then we should
                        #  change the state to 'packing'
                        if any([x.qty_done > 0
                                for x in rec.move_line_ids]):
                            shipment.state = "packing"

                    # when the packing stock.picking is 'done' then the state
                    # should be changed to 'wait_label'.
                    # At this stage,  we start wait for label's methods to
                    # complete the work and change the state to 'ready_shipment'
                    elif rec.state == "done":
                        shipment.state = "wait_label"
                        shipment.label_state = "waiting"
        return result


class ShipmentTransporter(models.Model):
    _name = "dbt.shipment.transporter"

    name = fields.Char('Name')
    transporter_type = fields.Selection(string='Transporter Type', selection=[
        ('internal', 'Internal'),
        ('external', 'External'),
        ('manual', 'Manual'),
    ])
    transporter_code = fields.Char('Transporter Code')

    returns_file = fields.Boolean('Return label file ?')

    generate_file_method = fields.Char('Generate & Send Label Method')
    get_output_method = fields.Char('Fetch output Method')

    active = fields.Boolean('Active')
