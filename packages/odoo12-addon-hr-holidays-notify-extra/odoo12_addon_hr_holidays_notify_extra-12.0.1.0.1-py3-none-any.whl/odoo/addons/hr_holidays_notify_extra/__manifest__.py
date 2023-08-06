# Copyright 2021 Coopdevs Treball SCCL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "HR Holidays Notify Extra Employees",
    "summary": "Notify other employees by mail on Leave Requests "
               "creation depending on the type",
    "version": "12.0.1.0.1",
    "category": "Human Resources",
    "website": "https://gitlab.com/coopdevs/odoo-addons",
    "author": "César López Ramírez (Coopdevs Treball SCCL)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        'hr_employee_multidepartment',
        'hr_holidays',
        'mail',
    ],
    "data": [
        'views/hr_leave_type.xml'
    ]
}
