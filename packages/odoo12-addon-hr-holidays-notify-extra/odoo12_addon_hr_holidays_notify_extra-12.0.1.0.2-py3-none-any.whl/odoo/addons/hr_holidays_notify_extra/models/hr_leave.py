# Copyright 2021 Coopdevs Treball SCCL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from datetime import date

class HRLeave(models.Model):
    _inherit = 'hr.leave'

    @api.multi
    def _get_extra_employees_to_notify(self):
        """Defines who to notify."""
        self.ensure_one()
        leave_type = self.holiday_status_id
        extra_employees = []
        if leave_type.is_sudden:
            for department in self.employee_id.department_ids:
                extra_employees.append(department.manager_id)
            extra_employees += leave_type.extra_notify_employees
        return extra_employees

    @api.model
    def create(self, vals):
        res = super(HRLeave, self).create(vals)
        res._notify_extra_employees()
        return res

    @api.multi
    def _notify_extra_employees(self):
        """Input: res.user"""
        self.ensure_one()
        extra_employees = self._get_extra_employees_to_notify()
        if not len(extra_employees):
            return True
        leave_date = self.date_from.date()
        today = date.today()
        if not (
            today.weekday() <= leave_date.weekday() and
            (leave_date - today).days < 7
        ):
            return True
        for extra_employee in extra_employees:
            self.add_follower(extra_employee.id)
            if extra_employee.user_id:
                self._message_auto_subscribe_notify(
                    [extra_employee.user_id.partner_id.id],
                    template='mail.message_user_assigned')
        return True
