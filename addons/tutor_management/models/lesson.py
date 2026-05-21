import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Lesson(models.Model):
    _name = 'tutor.lesson'
    _description = 'Lesson'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Number', required=True, copy=False, readonly=True, default='New')

    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('cancel', 'Cancel'),
            ('done', 'Done'),
        ],
        string='Status',
        default='planned',
    )
    tutor_id = fields.Many2one(comodel_name='tutor.tutor', string='Tutor', required=True)
    student_id = fields.Many2one(comodel_name='tutor.student', string='Student', required=True)
    notes = fields.Html(string='Notes')
    count_by_spec = fields.Integer(string='Count by specialization', compute='_compute_count_by_spec')
    spec_id = fields.Many2one(comodel_name='tutor.specialization', string='Specialization')

    @api.depends('name', 'create_date')
    def _compute_display_name(self):
        """
        Formats the lesson name for display, combining the unique
        sequence number and the date of the lesson.
        Data: sequence_data.xml
        Example: 'LSN/2026/00001 from 21.05.2026'
        """

        for lesson in self:
            date_part = fields.Date.to_string(lesson.create_date.date()) if lesson.create_date else ''
            lesson.display_name = f'{lesson.name} from {date_part}'

    @api.depends('spec_id')
    def _compute_count_by_spec(self):
        """
        Calculates how many times the selected specialization has been recorded
        across all lessons. Used for quick statistical reference.
        """

        for lesson in self:
            if lesson.spec_id:
                lesson.count_by_spec = self.env['tutor.lesson'].search_count(
                    [('spec_id', '=', lesson.spec_id)],
                )
            else:
                lesson.count_by_spec = 0

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides creation to assign a unique sequence number to each lesson
        from the 'tutor.lesson' sequence defined in data.
        :param vals_list: List of dictionaries for record creation.
        :return: Created lesson records.
        """

        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tutor.lesson') or 'New'
        return super().create(vals_list)

    @api.model
    def get_state_color(self):
        """
        Returns a bootstrap-style color class based on the current state.
        Useful for dynamic styling in Kanban or custom web views.
        :return: string representing a CSS color class.
        """

        self.ensure_one()

        colors = {'done': 'success', 'planned': 'secondary', 'cancel': 'danger'}
        return colors.get(self.state, 'info')

    @api.constrains('active', 'tutor_id', 'student_id', 'appointment_date')
    def _check_lesson(self):
        """
        Prevents modifications to key fields if the lesson status is 'Done'.
        Ensures historical lesson data integrity.
        :raises ValidationError: If an attempt is made to edit a completed lesson.
        """

        if self.env.context.get('install_mode'):
            return
        for lesson in self:
            if lesson.state == 'done':
                raise ValidationError(self.env._('Cannot change the values. Lesson already done'))

    def unlink(self):
        """
        Restricts the deletion of lessons that have reached the 'Done' state.
        :raises ValidationError: If 'done' records are present in the set.
        """

        if any(lesson.state == 'done' for lesson in self):
            raise ValidationError(self.env._('Not allowed to delete the record. Lesson already done'))

        return super().unlink()

    def action_archive(self):
        """
        Prevents archiving of completed lessons
        """

        if any(lesson.state == 'done' for lesson in self):
            raise ValidationError(self.env._('Not allowed to archive the record. Lesson already done'))

        return super().action_archive()

    def action_view_lessons_by_spec(self):
        """
        Opens a list view showing all lessons associated with
        the same specialization as the current record.
        :return: dict representing the ir.actions.act_window.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='Lessons by %(disease)s', disease=self.spec_id.name),
            'type': 'ir.actions.act_window',
            'res_model': 'tutor.lesson',
            'view_mode': 'list',
            'domain': [('spec_id', '=', self.spec_id.id)],
            'target': 'current',
        }
