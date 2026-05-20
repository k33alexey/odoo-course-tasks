======================================
Hospital Management System (hr_hospital)
======================================

This module adds a hospital management system functionality for Odoo.
It allows tracking doctors, patients, diseases, and managing visits.
Created as part of the Odoo School UA course, section 'Module formalization'.

Installation
============

To install this module, you need to:

#. Clone the repository with the module into your local ``addons`` directory.
#. Make sure the directory is mounted in your ``docker-compose.yml`` file.
#. Update the Odoo applications list inside the Docker container.
#. Install the module via the Odoo web interface.

Usage
=====

User manual
-----------

To manage hospital records:

* Go to **Hospital** main menu.
* Navigate to **Doctors** or **Patients** to manage records.

REST API Testing (Postman)
--------------------------

The module provides a clean REST API (HTTP type) to interact with doctor records without JSON-RPC wrappers:

* **GET** ``http://example.com/api/hospital/doctor`` — Retrieve the list of all doctors.
* **POST** ``http://example.com/api/hospital/doctor`` — Create a new doctor. Send raw JSON body (e.g., ``{"name": "Dr. House"}``).

Notes:
------

- When modifying Python controllers or models, don't forget to update the module from the terminal using Docker CLI:

  .. code-block:: bash

     docker compose exec web odoo -u hr_hospital -d postgres --stop-after-init
     docker compose restart web

- Make sure your Postman Desktop Agent is running when testing API locally on macOS to avoid localhost blockages.

Credits
=======

Authors
-------

* Kalinin Alexey

Contributors
------------

* Kalinin Alexey <k33alexey@gmail.com>