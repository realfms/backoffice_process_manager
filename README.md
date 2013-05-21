backoffice_process_manager
==============

Backoffice process manager involved in :

* rating, invoicing, invoice sending via email, invoice storing in S3
* consolidate payment information returned by payment gateways
* general control about the results of all stages of the process

A cloud-based RabbitMQ broker is used as Celery broker (CloudAMQP). This queue service is used as base technology for modelling business processes
