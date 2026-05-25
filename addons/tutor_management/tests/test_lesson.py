from odoo.exceptions import ValidationError
from odoo.tests.common import tagged

from .common import TutorManagementCommon


@tagged('post_install', '-at_install')
class TestLesson(TutorManagementCommon):
    """Test suite for the 'tutor.lesson' model.

    This class contains test cases...
    """

    @classmethod
    def setUpClass(cls):
        """Prepare master data required for all test cases."""
        super().setUpClass()
        cls.lesson = cls.env['tutor.lesson'].create(
            {
                'tutor_id': cls.tutor.id,
                'student_id': cls.student.id,
                'spec_id': cls.spec_math.id,
                'appointment_date': '2026-05-25 10:00:00',
                'price': 500,
            }
        )

    def test_01_lesson_creation_sequence(self):
        """Test that lesson name is automatically generated from sequence."""
        self.assertNotEqual(self.lesson.name, second='New', msg="Lesson name should not be 'New'")
        self.assertTrue(self.lesson.name.startswith('LSN/'), msg="Lesson name should start with 'LSN/'")

    def test_02_lesson_done_modification_constraint(self):
        """Test that modifying a lesson in 'done' state raises ValidationError."""
        self.lesson.action_done()
        self.assertEqual(self.lesson.state, second='done')

        with self.assertRaises(ValidationError, msg="Should not be able to modify a 'done' lesson"):
            self.lesson.write({'appointment_date': '2026-05-26 10:00:00'})

    def test_03_lesson_done_deletion_constraint(self):
        """Test that deleting a lesson in 'done' state raises ValidationError."""
        self.lesson.action_done()

        with self.assertRaises(ValidationError, msg="Should not be able to delete a 'done' lesson"):
            self.lesson.unlink()
