import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.medic.info']

    active = fields.Boolean('Active', default=True)
    category_id = fields.Many2one('hr_hospital.doctor.category', string='Doctor Category', required=True)
    is_intern = fields.Boolean('Is Intern', compute='_compute_is_intern', default=False, store=True)
    system_user_id = fields.Many2one('res.users', string='System User')
    mentor_id = fields.Many2one('hr_hospital.doctor', string='Mentor')
    intern_label = fields.Char(string='Status Label', compute='_compute_is_intern', store=True)

    @api.depends('full_name', 'category_id')
    def _compute_display_name(self):
        for doctor in self:
            full_name = doctor.full_name or ''
            category = doctor.category_id.name or _('No Category')
            doctor.display_name = f"{full_name} ({category})"

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref('hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            doctor.is_intern = doctor.category_id == intern_category
            doctor.intern_label = _('Intern') if doctor.category_id == intern_category else False

    @api.constrains('category_id', 'mentor_id')
    def _check_mentor(self):
        intern_category = self.env.ref('hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.category_id == intern_category:
                raise ValidationError(_('Intern is not allowed in mentor'))
            if doctor.mentor_id == doctor:
                raise ValidationError(_('A doctor cannot be their own mentor.'))
            if doctor.category_id == intern_category:
                trainee = self.search([('mentor_id', '=', doctor.id)])
                if trainee:
                    raise ValidationError(_('This doctor is currently reserved for mentors.'))