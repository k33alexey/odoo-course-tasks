from odoo import Command
from odoo.tests.common import TransactionCase


class TutorManagementCommon(TransactionCase):
    """Base test class for tutor management module providing shared master data."""

    @classmethod
    def setUpClass(cls):
        """Set up core database records required across multiple test suites."""
        super().setUpClass()

        # Create Specialization
        cls.spec_math = cls.env.ref(xml_id='tutor_management.math', raise_if_not_found=False)

        if not cls.spec_math:
            cls.spec_math = cls.env['tutor.specialization'].create(
                {
                    'name': 'Mathematics',
                    'price': 500,
                }
            )

        # Create Tutor
        cls.tutor = cls.env['tutor.tutor'].create(
            {
                'first_name': 'Test',
                'last_name': 'Tutor',
                'spec_ids': [Command.set([cls.spec_math.id])],
            }
        )

        # Create Student
        cls.student = cls.env['tutor.student'].create(
            {
                'first_name': 'Test',
                'last_name': 'Student',
            }
        )
