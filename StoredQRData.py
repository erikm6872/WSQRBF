

import sys
import uuid


class StoredQRData:
    def __init__(self, url="", guid=None):
        self.url = url
        if not guid:
            self.guid = uuid.uuid4().hex
        else:
            self.guid = guid

    def __eq__(self, other):
        if self.url == other.url and self.guid == other.guid:
            return True
        return False
