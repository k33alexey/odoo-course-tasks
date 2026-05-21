from odoo import fields, models


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
