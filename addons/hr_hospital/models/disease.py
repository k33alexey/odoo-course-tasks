import logging
import random

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    code = fields.Char(string='ICD Code')
    color = fields.Integer(
        string='Color Index',
        default=lambda self: random.randint(1, 11)
    )