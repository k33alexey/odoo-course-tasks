from odoo.tests.common import TransactionCase


class TestHospitalCommon(TransactionCase):
    """Base test class for hr_hospital module providing shared master data."""

    @classmethod
    def setUpClass(cls):
        """Set up core database records required across multiple test suites."""
        super().setUpClass()

        cls.category_cardio = cls.env['hr_hospital.doctor.category'].create(
            {
                'name': 'Cardiologist',
                'color': 3,
                'sequence': 10,
            }
        )
        cls.category_intern = cls.env.ref(xml_id='hr_hospital.doctor_category_intern', raise_if_not_found=False)

        if not cls.category_intern:
            cls.category_intern = cls.env['hr_hospital.doctor.category'].create(
                {
                    'name': 'Intern',
                    'color': 1,
                    'sequence': 30,
                }
            )
            cls.env['ir.model.data'].create(
                {
                    'module': 'hr_hospital',
                    'name': 'doctor_category_intern',
                    'model': 'hr_hospital.doctor.category',
                    'res_id': cls.category_intern.id,
                }
            )
