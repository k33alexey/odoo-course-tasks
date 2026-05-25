from odoo import api, fields, models


class Tutor(models.Model):
    """
    Represents a tutor in the system.
    Tutors have specializations and a history of lessons.
    Inherits from abstract person to share basic personal data fields.
    """
    _name = 'tutor.tutor'
    _description = 'Tutor'
    _inherit = ['tutor.abstract.person']

    active = fields.Boolean(string='Active', default=True)
    spec_ids = fields.Many2many(comodel_name='tutor.specialization', string='Tutor Specialization', required=True)
    specialization_color = fields.Integer(related='spec_ids.color', string='Specialization Color', readonly=False)
    color = fields.Integer(string='Color Index', default=0)
    lesson_ids = fields.One2many(
        comodel_name='tutor.lesson',
        inverse_name='tutor_id',
        string='Lesson History',
        readonly=True,
    )

    @api.depends('full_name', 'spec_ids', 'spec_ids.name')
    def _compute_display_name(self):
        """
        Constructs a readable name for the record.
        Example: 'Ivanov Ivan Ivanovich (Mathematics, Physics)'
        """
        for tutor in self:
            full_name = tutor.full_name or ''

            if tutor.spec_ids:
                spec_list = ', '.join(tutor.spec_ids.mapped('name'))
            else:
                spec_list = self.env._('No Specialization')

            tutor.display_name = f'{full_name} ({spec_list})'

    def action_quick_create_lesson(self):
        """
        Helper method to open a new lesson wizard or form pre-filled
        with the current tutor's information.
        :return: ir.actions.act_window to open the lesson form.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='New Lesson for Tutor %(name)s', name=self.full_name),
            'type': 'ir.actions.act_window',
            'res_model': 'tutor.lesson',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_tutor_id': self.id,
            },
        }
