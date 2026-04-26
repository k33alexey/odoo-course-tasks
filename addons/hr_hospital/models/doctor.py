import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.abstract.person']

    active = fields.Boolean('Active', default=True)