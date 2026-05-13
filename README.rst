===================
Hospital Management
===================

.. ![](/hr_hospital/static/description/icon.png)

This module provides a comprehensive system for managing hospital operations,
focusing on doctor-patient relationships, visit history, and medical classifications.

Features
========

* **Doctor Management**: Organize medical staff by categories and manage mentoring hierarchy (Mentors and Interns).
* **Patient Records**: Maintain detailed patient information including blood types and contact details.
* **Visit Tracking**: Manage the full lifecycle of hospital visits with status automation.
* **Medical History**: Automatic tracking of personal doctor assignments.
* **Disease Directory**: Hierarchical classification of diseases (ICD-compliant).

Usage
=====

1. Go to **Hospital** menu.
2. Configure **Doctor Categories** and **Diseases**.
3. Create **Doctor** profiles and assign **Mentors** to **Interns**.
4. Register **Patients** and schedule **Visits**.

Technical Notes
===============

* Inherits from ``mail.thread`` and ``mail.activity.mixin`` for communication.
* Uses ``image.mixin`` for person avatars.
* Includes strict validation for mentoring rules and visit status changes.

Credits
=======

* **Author**: Kalinin Alexey <k33alexey@gmail.com>