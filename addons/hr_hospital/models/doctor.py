import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    """
    Model representing medical staff (doctors and interns) in the hospital system.
    This model manages doctor profiles, their categories, and the mentoring
    link between experienced doctors and interns.
    """

    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.medic.info']

    active = fields.Boolean(string='Active', default=True)
    category_id = fields.Many2one(comodel_name='hr_hospital.doctor.category', string='Doctor Category', required=True)
    category_color = fields.Integer(related='category_id.color', string='Category Color', readonly=False)
    color = fields.Integer(string='Color Index', default=0)
    is_intern = fields.Boolean(string='Is Intern', compute='_compute_is_intern', default=False, store=True)
    system_user_id = fields.Many2one(comodel_name='res.users', string='System User')
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Mentor')
    intern_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
        readonly=True,
    )

    @api.depends('full_name', 'category_id')
    def _compute_display_name(self):
        """
        Constructs a readable name for the record.
        Example: 'Ivanov Ivan Ivanovich'
        """

        for doctor in self:
            full_name = doctor.full_name or ''
            category = doctor.category_id.name or self.env._('No Category')
            doctor.display_name = f'{full_name} ({category})'

    @api.depends('category_id')
    def _compute_is_intern(self):
        """
        Automatically flags a doctor as an intern if their category matches the predefined 'intern' XML record.
        """

        intern_category = self.env.ref(xml_id='hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            doctor.is_intern = doctor.category_id == intern_category

    @api.constrains('category_id', 'mentor_id')
    def _check_mentor(self):
        """
        Business logic validation for mentoring:
        1. An intern cannot be a mentor for someone else.
        2. A doctor cannot be their own mentor.
        3. A doctor currently assigned as an intern cannot have trainees.
        :raises ValidationError: If any mentoring rule is violated.
        """

        intern_category = self.env.ref(xml_id='hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.category_id == intern_category:
                raise ValidationError(self.env._('Intern is not allowed to be a mentor'))
            if doctor.mentor_id == doctor:
                raise ValidationError(self.env._('A doctor cannot be their own mentor.'))
            if doctor.category_id == intern_category:
                trainee = self.search([('mentor_id', '=', doctor.id)])
                if trainee:
                    raise ValidationError(self.env._('This doctor is currently reserved for mentors.'))

    def action_quick_create_visit(self):
        """
        Helper method to open a new visit wizard or form pre-filled
        with the current doctor's information.
        :return: ir.actions.act_window to open the visit form.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='New Visit for Doctor %(name)s', name=self.full_name),
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            },
        }
