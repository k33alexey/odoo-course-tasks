import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Hospital Visit'

    name = fields.Char(
        string='Number',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    disease_ids = fields.Many2many(
        'hr_hospital.disease',
        'visit_disease_rel',
        'visit_id',
        'disease_id',
        string='Diagnoses'
    )
    notes = fields.Text(string='Doctor Notes')

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
