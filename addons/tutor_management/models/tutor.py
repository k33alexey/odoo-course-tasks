from odoo import api, fields, models


class Tutor(models.Model):
    _name = 'tutor.tutor'
    _description = 'Tutor'
    _inherit = ['tutor.abstract.person']

    active = fields.Boolean(string='Active', default=True)
    spec_id = fields.Many2many(comodel_name='tutor.specialization', string='Tutor specialization', required=True)
    specialization_color = fields.Integer(related='spec_id.color', string='Specialization color', readonly=False)
    color = fields.Integer(string='Color Index', default=0)

    @api.depends('full_name', 'spec_id')
    def _compute_display_name(self):
        """
        Constructs a readable name for the record.
        Example: 'Ivanov Ivan Ivanovich (Mathematics)'
        """

        for tutor in self:
            full_name = tutor.full_name or ''
            spec = tutor.spec_id.name or self.env._('No specialization')
            tutor.display_name = f'{full_name} ({spec})'

    def action_quick_create_visit(self):
        """
        Helper method to open a new lesson wizard or form pre-filled
        with the current tutor's information.
        :return: ir.actions.act_window to open the lesson form.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='New lesson for tutor %(name)s', name=self.full_name),
            'type': 'ir.actions.act_window',
            'res_model': 'tutor.lesson',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_tutor_id': self.id,
            },
        }
