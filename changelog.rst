19.0.1.3.0
----------

* **Added REST API Controllers:** Implemented native HTTP endpoints for external integrations.
* Added ``GET /hr_hospital/doctor`` endpoint to retrieve the list of all doctors in clean JSON format.
* Added ``POST /hr_hospital/doctor`` endpoint for creating new doctor records with built-in basic validation and CSRF bypass for external tools like Postman.
* Optimized database resource processing by replacing heavy search loops with high-performance list comprehensions.

19.0.1.2.2
----------

* Initial release of the Hospital Management module.
* Implemented core models: Doctor, Patient, Disease, and Visit.
* Added mentoring logic (Mentor/Intern hierarchy) and automated validation.
* Added history tracking for personal doctor assignments.
* Implemented contact validation (phone and email) for medical staff and patients.
* Configured record rules for access rights (view own and interns' documents).