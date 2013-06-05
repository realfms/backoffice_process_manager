__author__ = 'mac'

import uuid

# TODO: Guarantee uid is unique among different nodes if this code is distributed
def compute_uuid():
    uid = uuid.uuid4()

    # Order = ten first characters of uuid
    return uid.hex[:10]