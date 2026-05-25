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
    lesson_ids = fields.Many2many(
        comodel_name='tutor.lesson',
        string='Lessons to Reassign',
        compute='_compute_lesson_ids',
    )

    @api.depends('from_tutor_id')
    def _compute_lesson_ids(self):
        """
        Automatically identifies all lessons in 'planned' state for the
        selected 'from' tutor. These records will be the target of the
        reassignment operation.
        """
        for record in self:
            if record.from_tutor_id:
                lessons = self.env['tutor.lesson'].search(
                    [('tutor_id', '=', record.from_tutor_id.id), ('state', '=', 'planned')]
                )
                record.lesson_ids = [Command.set(lessons.ids)]
            else:
                record.lesson_ids = [Command.clear()]

    def action_reassign(self):
        """
        Executes the reassignment of all identified lessons to the new tutor.
        Validates that the source and destination tutors are different and
        that there are lessons to process.
        :return: Client notification action with success message and page reload.
        :raises UserError: If tutors are identical or no lessons are found.
        """
        self.ensure_one()

        if self.from_tutor_id == self.to_tutor_id:
            raise UserError(self.env._('Source and destination tutors must be different!'))

        lessons = self.lesson_ids

        if not lessons:
            raise UserError(self.env._('No planned lessons found for this tutor.'))

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
