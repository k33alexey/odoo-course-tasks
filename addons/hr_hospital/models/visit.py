from odoo import models, fields

class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Hospital Visit'

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