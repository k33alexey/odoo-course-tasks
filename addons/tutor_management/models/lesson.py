import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Lesson(models.Model):
    """
    Main model representing a tutoring session between a tutor and a student.
    Manages lesson states, pricing based on specialization, and ensures
    data integrity by restricting changes to completed lessons.
    """

    _name = 'tutor.lesson'
    _description = 'Lesson'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Active', default=True, tracking=True)
    name = fields.Char(string='Number', required=True, copy=False, readonly=True, default='New')
    appointment_date = fields.Datetime(string='Appointment Date', required=True, tracking=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ],
        string='Status',
        default='planned',
        tracking=True,
        group_expand='_expand_states',
    )
    tutor_id = fields.Many2one(comodel_name='tutor.tutor', string='Tutor', required=True, tracking=True)
    student_id = fields.Many2one(comodel_name='tutor.student', string='Student', required=True, tracking=True)
    notes = fields.Html(string='Notes')
    count_by_spec = fields.Integer(string='Count by Specialization', compute='_compute_count_by_spec')
    spec_id = fields.Many2one(comodel_name='tutor.specialization', string='Specialization', tracking=True)
    price = fields.Monetary(string='Price', required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency', default=lambda self: self.env.company.currency_id
    )
    allowed_spec_ids = fields.Many2many(comodel_name='tutor.specialization', compute='_compute_allowed_spec_ids')

    @api.depends('tutor_id')
    def _compute_allowed_spec_ids(self):
        """
        Filters the available specializations based on the selected tutor's
        expertise. Ensures that a tutor can only be assigned to lessons
        within their known subjects.
        """
        for lesson in self:
            lesson.allowed_spec_ids = lesson.tutor_id.spec_ids if lesson.tutor_id else self.env['tutor.specialization']

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

        specs = self.mapped('spec_id')
        grouped = self.env['tutor.lesson']._read_group(
            domain=[('spec_id', 'in', specs.ids)],
            groupby=['spec_id'],
            aggregates=['__count'],
        )
        counts = {spec.id: count for spec, count in grouped}

        for lesson in self:
            lesson.count_by_spec = counts.get(lesson.spec_id.id, 0)

    @api.onchange('tutor_id')
    def _onchange_tutor_id(self):
        """
        Resets the specialization if the newly selected tutor does not
        support the previously chosen one.
        """
        if not self.tutor_id or (self.spec_id and self.spec_id not in self.tutor_id.spec_ids):
            self.spec_id = False

    @api.onchange('spec_id')
    def _onchange_spec_id(self):
        """
        Automatically updates the lesson price based on the default price
        of the selected specialization.
        """
        if self.spec_id:
            self.price = self.spec_id.price

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

    def write(self, vals):
        """
        Ensures that lessons in 'Done' state cannot be modified,
        except for changing the state itself (if allowed by logic).
        :raises ValidationError: If trying to edit fields of a completed lesson.
        """
        for lesson in self:
            if lesson.state == 'done':
                if 'state' not in vals:
                    raise ValidationError(self.env._('Cannot change fields in a completed lesson.'))

        return super().write(vals)

    def unlink(self):
        """
        Restricts the deletion of lessons that have reached the 'Done' state.
        :raises ValidationError: If 'done' records are present in the set.
        """

        if any(lesson.state == 'done' for lesson in self):
            raise ValidationError(self.env._('Not allowed to delete the record. Lesson already done'))

        return super().unlink()

    @api.model
    def _expand_states(self, states, domain):
        """
        Used for Kanban view grouping to ensure all possible states are
        visible as columns, even if they contain no records.
        """
        return [key for key, _ in self._fields['state'].selection]

    def get_state_color(self):
        """
        Returns a bootstrap-style color class based on the current state.
        Useful for dynamic styling in Kanban or custom web views.
        :return: string representing a CSS color class.
        """

        self.ensure_one()

        colors = {
            'done': 'success',
            'planned': 'secondary',
            'in_progress': 'warning',
            'cancel': 'danger',
        }
        return colors.get(self.state, 'info')

    def action_archive(self):
        """
        Prevents archiving of completed lessons to preserve history.
        :raises ValidationError: If lesson is done.
        """

        if any(lesson.state == 'done' for lesson in self):
            raise ValidationError(self.env._('Not allowed to archive the record. Lesson already done'))

        return super().action_archive()

    def action_done(self):
        """Sets the lesson state to 'Done'."""
        self.ensure_one()
        self.write({'state': 'done'})

    def action_cancel(self):
        """Sets the lesson state to 'Cancel'."""
        self.ensure_one()
        self.write({'state': 'cancel'})

    def action_in_progress(self):
        """Sets the lesson state to 'In Progress'."""
        self.ensure_one()
        self.write({'state': 'in_progress'})

    def action_draft(self):
        """Resets the lesson state to 'Planned'."""
        self.ensure_one()
        self.write({'state': 'planned'})

    def action_view_lessons_by_spec(self):
        """
        Opens a list view showing all lessons associated with
        the same specialization as the current record.
        :return: dict representing the ir.actions.act_window.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='Lessons by %(spec)s', spec=self.spec_id.name),
            'type': 'ir.actions.act_window',
            'res_model': 'tutor.lesson',
            'view_mode': 'list',
            'domain': [('spec_id', '=', self.spec_id.id)],
            'target': 'current',
        }
