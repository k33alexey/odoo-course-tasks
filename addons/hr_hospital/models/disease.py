from odoo import models, fields

class HospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    code = fields.Char(string='ICD Code')