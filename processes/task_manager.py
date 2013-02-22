#!/usr/bin/python
# coding=utf-8

"""
Copyright 2012 Telefonica Investigación y Desarrollo, S.A.U

This file is part of Billing_PoC.

Billing_PoC is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.
Billing_PoC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with Billing_PoC.
If not, see http://www.gnu.org/licenses/.

For those usages not covered by the GNU Affero General Public License please contact with::mac@tid.es
"""

from django.utils import simplejson
from models import Task, SubProcess

class TaskManager:

    def generate_task(self, sp_id, name):
        subprocess = SubProcess.objects.get(id=sp_id)

        task = Task(subprocess=subprocess, name=name)
        task.save()

        return task

    def get_subprocess_data(self, sp_id):
        subprocess = SubProcess.objects.get(id=sp_id)

        return simplejson.loads(subprocess.result)

    def process_task(self, sp_id, name, success, fn):

        if not success:
            return (False, False)

        try:
            task = self.generate_task(sp_id, name)

            (result, remarkable_data) = fn()

            task.set_now_as_end()
            task.set_remarkable_data(remarkable_data)
            task.set_result(simplejson.dumps(result))
            task.set_status('OK')

            task.save()

            return (True, task)
        except Exception as e:

            trace = {
                'type': type(e),
                'args': e.args,
                'text': unicode(e)
            }

            if (task):
                try:
                    task.set_remarkable_data(trace)
                    task.set_status('ERROR')

                    task.save()
                except:
                    pass

            # Writing log
            print "### LOG ### {0} cloud't be processed! {1} {2} {3}".format(name, type(e), e.args, unicode(e))

            return (False, None)
