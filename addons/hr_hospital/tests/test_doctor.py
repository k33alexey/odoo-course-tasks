from odoo.exceptions import ValidationError
from odoo.tests.common import tagged

from .common import TestHospitalCommon


@tagged('post_install', '-at_install')
class TestHospitalDoctor(TestHospitalCommon):
    """Test suite for the 'hr_hospital.doctor' model.

    This class contains test cases to validate doctor profile creation,
    display name generation, automatic intern flagging, and business logic
    constraints related to mentoring relationships.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare master data required for all test cases.

        This method runs once before any test methods are executed.
        It sets up medical categories (Cardiologist, Surgeon, Intern)
        to serve as a baseline database state for isolated transactions.
        """
        super().setUpClass()

        cls.category_surgeon = cls.env['hr_hospital.doctor.category'].create(
            {
                'name': 'Surgeon',
                'color': 5,
            }
        )

    def test_01_doctor_basic_creation_and_display_name(self):
        """Verify standard doctor profile creation and display name computation.

        Ensures that default fields, related fields (category color), and
        the '_compute_display_name' method generate the correct string format.
        """
        doctor = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Alexey',
                'last_name': 'Kalinin',
                'category_id': self.category_cardio.id,
            }
        )

        self.assertTrue(doctor.active)
        self.assertEqual(doctor.category_color, 3)
        self.assertFalse(doctor.is_intern)
        self.assertEqual(doctor.display_name, 'Kalinin Alexey (Cardiologist)')

    def test_02_compute_is_intern(self):
        """Verify automatic validation of the 'Is Intern' flag.

        Ensures that assigning the predefined intern category automatically
        sets the 'is_intern' Boolean field to True via the compute method.
        """
        intern = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Dmitry',
                'last_name': 'Petrov',
                'category_id': self.category_intern.id,
            }
        )
        self.assertTrue(intern.is_intern)

    def test_03_constraint_self_mentor(self):
        """Ensure a doctor cannot be assigned as their own mentor.

        Validates that the '@api.constrains' logic triggers a ValidationError
        when a record attempts to reference itself in the 'mentor_id' field.
        """
        doctor = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'category_id': self.category_surgeon.id,
            }
        )

        with self.assertRaises(ValidationError, msg='A doctor cannot be their own mentor.'):
            doctor.write({'mentor_id': doctor.id})

    def test_04_constraint_intern_cannot_be_mentor(self):
        """Ensure an intern doctor cannot be assigned as a mentor to anyone else.

        Validates that the system blocks mentoring relationships where the
        selected mentor belongs to the intern category.
        """
        intern = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Dmitry',
                'last_name': 'Petrov',
                'category_id': self.category_intern.id,
            }
        )
        doctor = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Sergey',
                'last_name': 'Sidorov',
                'category_id': self.category_cardio.id,
            }
        )

        with self.assertRaises(ValidationError, msg='Intern is not allowed to be a mentor'):
            doctor.write({'mentor_id': intern.id})

    def test_05_action_quick_create_visit(self):
        """Verify the dictionary action returned for quick visit creation.

        Validates that the 'action_quick_create_visit' method returns a proper
        window action structure with pre-filled context for the current doctor.
        """
        doctor = self.env['hr_hospital.doctor'].create(
            {
                'first_name': 'Alexey',
                'last_name': 'Kalinin',
                'category_id': self.category_cardio.id,
            }
        )

        action = doctor.action_quick_create_visit()

        self.assertEqual(action.get('type'), 'ir.actions.act_window')
        self.assertEqual(action.get('res_model'), 'hr_hospital.visit')
        self.assertEqual(action.get('view_mode'), 'form')
        self.assertEqual(action.get('target'), 'new')

        context = action.get('context', {})
        self.assertEqual(context.get('default_doctor_id'), doctor.id)
