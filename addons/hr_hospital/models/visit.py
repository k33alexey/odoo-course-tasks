import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Hospital Visit'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(
        string='Number',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    completion_date = fields.Datetime(string='Completion Date')
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('cancel', 'Cancel'),
            ('done', 'Done'),
        ],
        string='Status',
        default='planned'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Doctor',
        required=True
    )
    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Patient',
        required=True
    )
    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Diagnose'
    )
    notes = fields.Html(string='Summary')
    count_by_disease = fields.Integer(string='Count by disease', compute='_compute_count_by_disease')

    @api.depends('name', 'visit_date')
    def _compute_display_name(self):
        for visit in self:
            date_part = fields.Date.to_string(visit.visit_date.date()) if visit.visit_date else ''
            visit.display_name = f"Visit #{visit.name} from {date_part}"

    @api.depends('disease_id')
    def _compute_count_by_disease(self):
        for visit in self:
            if visit.disease_id:
                visit.count_by_disease = self.env['hr_hospital.visit'].search_count(
                    [
                        ('disease_id', '=', visit.disease_id)
                    ],
                )
            else:
                visit.count_by_disease = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hr_hospital.visit') or 'New'
        return super().create(vals_list)

    @api.model
    def get_state_color(self):
        self.ensure_one()

        colors = {'done': 'success', 'planned': 'secondary', 'cancel': 'danger'}
        return colors.get(self.state, 'info')

    @api.constrains('active', 'doctor_id', 'visit_date', 'completion_date')
    def _check_visit(self):
        if self.env.context.get('install_mode'):
            return
        for visit in self:
            if visit.state == 'done':
                raise ValidationError(self.env._('Cannot change the values. Visit already done'))

    def unlink(self):
        if any(visit.state == 'done' for visit in self):
            raise ValidationError(self.env._('Not allowed to delete the record. Visit already done'))

        return super().unlink()

    def action_archive(self):
        if any(visit.state == 'done' for visit in self):
            raise ValidationError(self.env._('Not allowed to archive the record. Visit already done'))

        return super().action_archive()

    def action_view_visits_by_disease(self):
        self.ensure_one()

        return {
            'name': self.env._('Visits by %s', self.disease_id.id),
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list',
            'domain': [('disease_id', '=', self.disease_id.id)],
            'target': 'current',
        }
