from odoo import fields, models


class TutorReassignWizardLines(models.TransientModel):
    """
    Helper model to represent a single lesson in the reassignment wizard.
    Includes a boolean field for user selection.
    """

    _name = 'tutor.reassign.wizard.line'
    _description = 'Reassign Tutor Wizard Line'

    wizard_id = fields.Many2one(
        comodel_name='tutor.reassign.wizard',
        string='Wizard',
    )
    lesson_id = fields.Many2one(
        comodel_name='tutor.lesson',
        string='Lesson',
    )
    reassign = fields.Boolean(
        string='Reassign',
        default=True,
    )

    name = fields.Char(related='lesson_id.name', string='Number', readonly=True)
    appointment_date = fields.Datetime(related='lesson_id.appointment_date', string='Date', readonly=True)
    student_id = fields.Many2one(related='lesson_id.student_id', string='Student', readonly=True)
    state = fields.Selection(related='lesson_id.state', string='Status', readonly=True)
