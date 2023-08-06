# Copyright 2021 Coopdevs Treball SCCL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from datetime import date, timedelta


class TestNotifyExtraEmployees(TransactionCase):
    def setUp(self):
        super(TestNotifyExtraEmployees, self).setUp()
        self.hol_model = self.env['hr.leave'].with_context(import_file=True)
        self.user_model = self.env['res.users']
        self.emp_model = self.env['hr.employee']
        self.type_model = self.env['hr.leave.type']
        self.dep_model = self.env['hr.department']

        self.user = self.user_model.create({
            'name': 'Test User',
            'login': 'user',
            'email': 'test.user@example.com'})
        self.extra_employee = self.user_model.create({
            'name': 'Test Extra Employee',
            'login': 'employee',
            'email': 'test.employee@example.com'})
        self.emp_extra_employee = self.emp_model.create({
            'name': 'Test Extra Employee',
            'user_id': self.extra_employee.id})
        self.extra_manager = self.user_model.create({
            'name': 'Test Extra Manager',
            'login': 'manager',
            'email': 'test.manager@example.com'
        })
        self.emp_extra_manager = self.emp_model.create({
            'name': 'Test Extra Manager',
            'user_id': self.extra_manager.id
        })
        self.extra_department = self.dep_model.create({
            'name': 'Extra department',
            'manager_id': self.emp_extra_manager.id
        })
        self.employee = self.emp_model.create({
            'name': 'Test employee',
            'user_id': self.user.id,
            'department_ids': [(6, 0, [self.extra_department.id])]
        })
        self.holiday_type = self.type_model.create({
            'name': 'Leave',
            'allocation_type': 'fixed',
            'extra_notify_employees': [(6, 0, [self.emp_extra_employee.id])]
        })
        self.env['hr.leave.allocation'].create({
            'holiday_type': 'employee',
            'employee_id': self.employee.id,
            'holiday_status_id': self.holiday_type.id,
            'state': 'validate',
            'number_of_days': 1.0,
        })

    def test_add_follower_1(self):
        """Tests if the extra employee is added as follower to the leave
        request. With is_sudden = False.
        """
        extra_employee = self.extra_employee.partner_id
        # With the configuration disabled:
        self.holiday_type.is_sudden = False
        leave = self.hol_model.sudo(self.user).create({
            'name': 'I am ill',
            'employee_id': self.employee.id,
            'holiday_status_id': self.holiday_type.id,
            'date_from': date.today(),
        })
        follower_set = extra_employee in leave.message_follower_ids.mapped(
            'partner_id') if extra_employee else False
        self.assertFalse(follower_set, "Follower added unexpectedly.")

    def test_add_follower_2(self):
        """Tests if the extra employee is added as follower to the leave
        request. With is_sudden = True.
        """
        extra_employee = self.extra_employee.partner_id
        # With the configuration disabled:
        self.holiday_type.is_sudden = True
        leave = self.hol_model.sudo(self.user).create({
            'name': 'I am still ill',
            'employee_id': self.employee.id,
            'holiday_status_id': self.holiday_type.id,
            'date_from': date.today(),
        })
        follower_set = extra_employee in leave.message_follower_ids.mapped(
            'partner_id') if extra_employee else False
        self.assertTrue(follower_set, "Extra employee hasn't been added "
                                      "as follower.")

    def test_add_follower_multidepartment(self):
        """Tests if the extra employee is added as follower to the leave
        request. With is_sudden = True.
        """
        extra_manager = self.extra_manager.partner_id
        # With the configuration disabled:
        self.holiday_type.is_sudden = True
        leave = self.hol_model.sudo(self.user).create({
            'name': 'I am still ill',
            'employee_id': self.employee.id,
            'holiday_status_id': self.holiday_type.id,
            'date_from': date.today(),
        })
        follower_set = extra_manager in leave.message_follower_ids.mapped(
            'partner_id') if extra_manager else False
        self.assertTrue(follower_set, "Extra manager hasn't been added "
                                      "as follower.")

    def test_add_follower_next_week(self):
        """Tests if the extra employee is not added as follower
        because the leave is next week.
        """
        extra_employee = self.extra_employee.partner_id
        # With the configuration disabled:
        self.holiday_type.is_sudden = True
        leave = self.hol_model.sudo(self.user).create({
            'name': 'I will be ill',
            'employee_id': self.employee.id,
            'holiday_status_id': self.holiday_type.id,
            'date_from': date.today() + timedelta(days=7),
            'date_to': date.today() + timedelta(days=7),
        })
        follower_set = extra_employee in leave.message_follower_ids.mapped(
            'partner_id') if extra_employee else False
        self.assertFalse(follower_set, "Follower added unexpectedly.")
