# Copyright 2021 Coopdevs Treball SCCL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    is_sudden = fields.Boolean('Sudden Leave?')
    extra_notify_employees = fields.Many2many('hr.employee', string="Notify to these employees")