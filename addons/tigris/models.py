# -*- coding: utf-8 -*-

# from openerp import models, fields, api

from openerp.osv import fields, osv
from openerp import tools


class pos_report_model(osv.osv):
    _name = "pos.report.model"
    _description = "POS Report"
    _auto = False
    _columns = {
        'id': fields.integer('id', readonly=True),
        'create_date': fields.date('Date', readonly=True),
        'login': fields.char('login', readonly=True),
        'pos_reference': fields.char('POS Ref', readonly=True),
        'sale_price_unit': fields.float('SP/Unit', readonly=True),
        'cost_price_unit': fields.float('CP/Unit', readonly=True),
        'price_subtotal': fields.float('Subtotal', readonly=True),
        'qty': fields.float('Qty', readonly=True),
        'name_template': fields.char('Product', readonly=True),
        'complete_name': fields.char('Destination', readonly=True),
        'profit': fields.float('Profit/Loss', readonly=True)
    }
    _order = 'create_date asc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'pos_report_model')
        cr.execute("""
            CREATE OR REPLACE VIEW pos_report_model AS (
            SELECT
			row_number() OVER () as id,
			a.create_date,
			d.login,
			a.name as pos_reference,
			a.price_unit as sale_price_unit,
			b.price_unit as cost_price_unit,
			a.price_subtotal,
			a.qty,
			e.name_template,
			f.complete_name,
			(a.price_unit-b.price_unit)*a.qty AS profit
			FROM pos_order_line a
			JOIN stock_move b ON a.name=b.name
			JOIN res_users d ON a.create_uid=d.id
			JOIN product_product e on a.product_id=e.id
			JOIN stock_location f on b.location_dest_id=f.id
            )
        """)

pos_report_model()

class stock_move_model(osv.osv):
    _name = "stock.move.model"
    _description = "Stock Move Report"
    _auto = False
    _columns = {
        'id': fields.integer('id', readonly=True),
        'create_date': fields.date('Create Date', readonly=True),
        'date': fields.date('Date', readonly=True),
        'product': fields.char('Product', readonly=True),
        'origin': fields.char('Origin', readonly=True),
        'location1': fields.char('Location1', readonly=True),
        'location2': fields.char('Location2', readonly=True),
        'name': fields.char('Reference', readonly=True),
        'price_unit': fields.float('Price per unit', readonly=True),
        'product_qty': fields.float('Quantity', readonly=True),
        'inventory_value': fields.float('Inventory Value', readonly=True)
    }
    _order = 'create_date asc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'stock_move_model')
        cr.execute("""
            CREATE OR REPLACE VIEW stock_move_model AS (
            SELECT
			row_number() OVER () as id,
			a1.id as aid,
			a1.origin,
			a1.product_uos_qty,
			a1.create_date,
			a1.move_dest_id,
			a1.product_uom,
			a1.price_unit,
			a1.product_uom_qty,
			a1.company_id,
			a1.date,
			a1.product_qty,
			a1.product_uos,
			a3.complete_name as location1, --location_id
			a1.priority,
			a1.picking_type_id,
			a1.partner_id,
			a1.note,
			a1.state,
			a1.origin_returned_move_id,
			a1.product_packaging,
			a1.date_expected,
			a1.procurement_id,
			a1.name,
			a1.create_uid,
			a1.warehouse_id,
			a1.inventory_id,
			a1.partially_available,
			a1.propagate,
			a1.restrict_partner_id,
			a1.procure_method,
			a1.write_uid,
			a1.restrict_lot_id,
			a1.group_id,
			a2.name_template as product, --product_id,
			a1.split_from,
			a1.picking_id,
			a4.complete_name as location2, --location_dest_id,
			a1.write_date,
			a1.push_rule_id,
			a1.rule_id,
			a1.invoice_state,
			a1.purchase_line_id,
			a1.price_unit*a1.product_qty as inventory_value
			FROM stock_move a1
			JOIN product_product a2 on a1.product_id=a2.id
			JOIN stock_location a3 on a1.location_id=a3.id
			JOIN stock_location a4 on a1.location_dest_id=a4.id
            )
        """)

stock_move_model()

class stock_quant_model(osv.osv):
    _name = "stock.quant.model"
    _description = "Stock Quant Report"
    _auto = False
    _columns = {
        'id': fields.integer('id', readonly=True),
        'create_date': fields.date('Create Date', readonly=True),
        'write_date': fields.date('Write Date', readonly=True),
        'in_date': fields.date('In Date', readonly=True),
        'qty': fields.float('Qty', readonly=True),
        'cost': fields.float('Cost', readonly=True),
        'name_template': fields.char('Product', readonly=True),
        'current_location': fields.char('Current', readonly=True),
        'inventory_value': fields.float('Inventory Value', readonly=True)
    }
    _order = 'create_date asc, in_date asc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'stock_quant_model')
        cr.execute("""
            CREATE OR REPLACE VIEW stock_quant_model AS (
            SELECT
			row_number() OVER () as id,
			a1.create_date,
			a1.write_date,
			a1.in_date,
			a1.qty,
			a1.cost,
			a4.name_template,
			a5.complete_name as current_location,
			(a1.cost*a1.qty) as inventory_value
			FROM stock_quant a1
			JOIN product_product a4 on a1.product_id=a4.id
			JOIN stock_location a5 on a1.location_id=a5.id
            )
        """)

stock_quant_model()
