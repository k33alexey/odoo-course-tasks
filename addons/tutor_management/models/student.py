from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = 'tutor.student'
    _description = 'Patient'
    _inherit = ['tutor.abstract.person', 'mail.thread', 'mail.activity.mixin']

    lesson_ids = fields.One2many(
        comodel_name='tutor.lesson',
        inverse_name='student_id',
        string='Lesson history',
        readonly=True,
    )
    lesson_count = fields.Integer(compute='_compute_lesson_count')

    def _compute_lesson_count(self):
        for student in self:
            student.lesson_count = len(student.lesson_ids)

    @api.model
    def action_empty(self, *args, **kwargs):
        return False
