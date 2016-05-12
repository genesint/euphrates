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

class stock_report_model(osv.osv):
    _name = "stock.report.model"
    _description = "Stock Report"
    _auto = False
    _columns = {
        'id': fields.integer('id', readonly=True),
        'create_date': fields.date('Create Date', readonly=True),
        'write_date': fields.date('Write Date', readonly=True),
        'in_date': fields.date('In Date', readonly=True),
        'qty': fields.float('Qty', readonly=True),
        'cost': fields.float('Cost', readonly=True),
        'name_template': fields.char('Product', readonly=True),
        'complete_name': fields.char('Destination', readonly=True),
        'inventory_value': fields.float('Inventory Value', readonly=True)
    }
    _order = 'create_date asc, in_date asc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'stock_report_model')
        cr.execute("""
            CREATE OR REPLACE VIEW stock_report_model AS (
            SELECT
			row_number() OVER () as id,
			a.create_date,
			a.write_date,
			a.in_date,
			a.qty,
			a.cost,
			b.name_template,
			d.complete_name,
			(a.cost*a.qty) as inventory_value
			FROM stock_quant a
			JOIN product_product b on a.product_id=b.id
			JOIN stock_location d on a.location_id=d.id
            )
        """)

stock_report_model()
