from odoo import fields, models


class Student(models.Model):
    """
    Represents a student in the tutoring system.
    Extends the abstract person model to include lesson history and
    statistical counters for management purposes.
    """
    _name = 'tutor.student'
    _description = 'Patient'
    _inherit = ['tutor.abstract.person', 'mail.thread', 'mail.activity.mixin']

    lesson_ids = fields.One2many(
        comodel_name='tutor.lesson',
        inverse_name='student_id',
        string='Lesson History',
        readonly=True,
    )
    lesson_count = fields.Integer(compute='_compute_lesson_count')

    def _compute_lesson_count(self):
        """
        Calculates the total number of lessons associated with the student.
        Used for displaying the lesson count in smart buttons or kanban views.
        """
        for student in self:
            student.lesson_count = len(student.lesson_ids)
