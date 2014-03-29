# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2001-2014 Zhuhai sunlight software development co.,ltd. All Rights Reserved.
#    Author: Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    _columns = {
        'qc_result': fields.selection([
            ('passed', 'Passed'),
            ('partial', 'Partial Passed'),
            ('rejected', 'Rejected'),
            ], 'QC Result', select=True, help="""
            * Passed: all products passed.\n
            * Partial Passed: Some products have a problem.\n
            * Rejected: all products have a problem.\n
            """
        ),
        'qc_note': fields.text('QC Notes'),
        'qc_date': fields.datetime('QC Date'),
        'state': fields.selection(
            [('draft', 'Draft'),
            ('auto', 'Waiting Another Operation'),
            ('confirmed', 'Waiting Availability'),
            ('qc','Waiting QC Result'),
            ('assigned', 'Ready to Receive'),
            ('done', 'Received'),
            ('cancel', 'Cancelled'),],
            'Status', readonly=True, select=True,
            help="""* Draft: not confirmed yet and will not be scheduled until confirmed\n
                 * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                 * Waiting Availability: still waiting for the availability of products\n
                 * Ready to Receive: products reserved, simply waiting for confirmation.\n
                 * Received: has been processed, can't be modified or cancelled anymore\n
                 * Cancelled: has been cancelled, can't be confirmed anymore"""),
        'qc_date': fields.datetime('QC Date', readonly=True, states={'qc':[('readonly', False)]}),
        'qc_checker': fields.many2one('hr.employee','QC Checker', readonly=True, states={'qc':[('readonly', False)]}),
    }
    def action_assign_wkf(self, cr, uid, ids, context=None):
        """ Changes picking state to assigned.
        @return: True
        """
        self.write(cr, uid, ids, {'state': 'qc'})
        return True



class stock_picking_in(osv.osv):
    _inherit = 'stock.picking.in'

    _columns = {
        'qc_result': fields.selection([
            ('passed', 'Passed'),
            ('partial', 'Partial Passed'),
            ('rejected', 'Rejected'),
            ], 'QC Result', select=True, readonly=True, states={'qc':[('readonly', False)]}, help="""
            * Passed: all products passed.\n
            * Partial Passed: Some products have a problem.\n
            * Rejected: all products have a problem.\n
            """
        ),
        'qc_note': fields.text('QC Notes', readonly=True, states={'qc':[('readonly', False)]}),
        'state': fields.selection(
            [('draft', 'Draft'),
            ('auto', 'Waiting Another Operation'),
            ('confirmed', 'Waiting Availability'),
            ('qc','Waiting QC Result'),
            ('assigned', 'Ready to Receive'),
            ('done', 'Received'),
            ('cancel', 'Cancelled'),],
            'Status', readonly=True, select=True,
            help="""* Draft: not confirmed yet and will not be scheduled until confirmed\n
                 * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                 * Waiting Availability: still waiting for the availability of products\n
                 * Ready to Receive: products reserved, simply waiting for confirmation.\n
                 * Received: has been processed, can't be modified or cancelled anymore\n
                 * Cancelled: has been cancelled, can't be confirmed anymore"""),
        'qc_date': fields.datetime('QC Date', readonly=True, states={'qc':[('readonly', False)]}),
        'qc_checker': fields.many2one('hr.employee','QC Checker', readonly=True, states={'qc':[('readonly', False)]}),
    }

    def action_qc(self, cr, uid, ids, context=None):
        """ QC Done.
        @return: True
        """
        picking = self.browse(cr,uid,ids,context=context)
        if not picking[0].qc_result:
            raise osv.except_osv(_('Error, no qc result!'),
                _('Please put a qc result on the picking list.'))

        self.write(cr, uid, ids, {'state': 'assigned', 'qc_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: