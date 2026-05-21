===========================
Tutoring Management System
===========================

This module adds a smart digital tutoring environment functionality.
It allows tracking tutors, active students, educational specializations, and managing lesson documents with automated pricing recalculation.
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

To manage tutoring records:

* Go to **Tutoring** main menu.
* Navigate to **Tutors**, **Students**, or **Lessons** to manage educational workflows.

Notes:
------

- When modifying Python controllers or models, don't forget to update the module from the terminal using Docker CLI (with your module name):

  .. code-block:: bash

     docker compose exec web odoo -u tutoring_management -d postgres --stop-after-init
     docker compose restart web

- Make sure your Postman Desktop Agent is running when testing API locally on macOS to avoid localhost blockages.

Credits
=======

Authors
-------

* Kalinin Oleksii

Contributors
------------

* Kalinin Oleksii <k33alexey@gmail.com>