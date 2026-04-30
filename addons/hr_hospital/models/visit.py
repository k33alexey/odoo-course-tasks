import logging

from odoo import models, fields, api, _
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
        default='New')
    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    completion_date = fields.Datetime(string='Completion Date')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='Status', default='planned')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    disease_ids = fields.Many2many(
        'hr_hospital.disease',
        'visit_disease_rel',
        'visit_id',
        'disease_id',
        string='Diagnoses')
    notes = fields.Html(string='Summary')

    @api.depends('name', 'visit_date')
    def _compute_display_name(self):
        for rec in self:
            date_part = fields.Date.to_string(rec.visit_date.date()) if rec.visit_date else ''
            rec.display_name = f"Visit #{rec.name} from {date_part}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hr_hospital.visit') or 'New'
        return super().create(vals_list)

    @api.constrains('active', 'doctor_id', 'visit_date', 'completion_date')
    def _check_visit(self):
        if self.env.context.get('install_mode'):
            return
        for visit in self:
            if visit.state == 'done':
                raise ValidationError(_('Cannot change the values. Visit already done'))

    def unlink(self):
        for visit in self:
            if visit.state == 'done':
                raise ValidationError(_('Not allowed to delete the record. Visit already done'))