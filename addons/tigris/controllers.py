# -*- coding: utf-8 -*-
from openerp import http

# class Tigris(http.Controller):
#     @http.route('/tigris/tigris/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tigris/tigris/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tigris.listing', {
#             'root': '/tigris/tigris',
#             'objects': http.request.env['tigris.tigris'].search([]),
#         })

#     @http.route('/tigris/tigris/objects/<model("tigris.tigris"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tigris.object', {
#             'object': obj
#         })