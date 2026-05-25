from odoo import Command, api, fields, models
from odoo.exceptions import UserError


class TutorReassignWizard(models.TransientModel):
    """
    Wizard to reassign planned lessons from one tutor to another.
    Allows for bulk updates of lesson assignments when a tutor
    is unavailable or there's a need to balance workload.
    """

    _name = 'tutor.reassign.wizard'
    _description = 'Reassign Tutor for Planned Lessons'

    from_tutor_id = fields.Many2one(
        comodel_name='tutor.tutor',
        string='From Tutor',
        required=True,
    )
    to_tutor_id = fields.Many2one(
        comodel_name='tutor.tutor',
        string='To Tutor',
        required=True,
    )
    line_ids = fields.One2many(
        comodel_name='tutor.reassign.wizard.line',
        inverse_name='wizard_id',
        string='Lessons to Reassign',
    )

    @api.onchange('from_tutor_id')
    def _onchange_from_tutor_id(self):
        """
        Populates the lines with planned lessons for the selected tutor.
        Allows users to selectively mark lessons for reassignment.
        """
        self.line_ids = [Command.clear()]
        if self.from_tutor_id:
            lessons = self.env['tutor.lesson'].search(
                [('tutor_id', '=', self.from_tutor_id.id), ('state', '=', 'planned')]
            )
            lines = [
                Command.create(
                    {
                        'lesson_id': lesson.id,
                        'reassign': True,
                    }
                )
                for lesson in lessons
            ]

            self.line_ids = lines

    def action_reassign(self):
        """
        Executes the reassignment of marked lessons to the new tutor.
        Validates that the source and destination tutors are different and
        that at least one lesson is selected.
        :return: Client notification action with success message or warning.
        :raises UserError: If tutors are identical.
        """
        self.ensure_one()

        if self.from_tutor_id == self.to_tutor_id:
            raise UserError(self.env._('Source and destination tutors must be different!'))

        selected_lines = self.line_ids.filtered('reassign')
        lessons = selected_lines.mapped('lesson_id')

        if not lessons:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': self.env._('Warning'),
                    'message': self.env._('Please select at least one lesson row to reassign.'),
                    'type': 'danger',
                    'sticky': False,
                },
            }

        lessons.write({'tutor_id': self.to_tutor_id.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': self.env._('Success'),
                'message': self.env._(
                    source='%(count)s lessons reassigned to %(name)s',
                    count=len(lessons),
                    name=self.to_tutor_id.full_name,
                ),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            },
        }
