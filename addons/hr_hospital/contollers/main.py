from odoo import http
from odoo.http import request


class HospitalController(http.Controller):
    """Controller responsible for handling HTTP API requests related to the hospital module."""

    @http.route(route='/api/hospital/doctor', type='jsonrpc', auth='public', methods=['GET'], csrf=False)
    def get_doctors(self):
        """Retrieve a list of all doctors in the system.

        :return: HTTP response containing a JSON object with a success status and a list of doctor records.
        :rtype: http.Response
        """

        doctors = request.env['hr_hospital.doctor'].sudo().search([])

        result = [
            {
                'id': doctor.id,
                'name': doctor.full_name,
                'category': doctor.category_id.name if doctor.category_id else 'No Category',
                'is_intern': doctor.is_intern,
            }
            for doctor in doctors
        ]

        return {'status': 'success', 'data': result}

    @http.route(
        route='/api/hospital/doctor/<int:doctor_id>', type='jsonrpc', auth='public', methods=['GET'], csrf=False
    )
    def get_doctor(self, doctor_id):
        """Retrieve a doctor by id in the system.

        :return: HTTP response containing a JSON object with a success status and a data of doctor record.
        :rtype: http.Response
        """

        doctor = request.env['hr_hospital.doctor'].sudo().browse(doctor_id)

        if not doctor.exists():
            return {'status': 'error', 'data': [], 'message': f'Doctor with ID {doctor_id} not found'}

        doctor_data = [
            {
                'id': doctor.id,
                'name': doctor.full_name,
                'category': doctor.category_id.name if doctor.category_id else 'No Category',
                'is_intern': doctor.is_intern,
            }
        ]

        return {'status': 'success', 'data': doctor_data}

    @http.route(route='/api/hospital/doctor', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def post_doctor(self):
        return {'status': 'success'}
