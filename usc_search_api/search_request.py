import re

ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')
FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')

def conv_to_snake_case(camel_case):
    s = FIRST_CAP_RE.sub(r'\1_\2', camel_case)
    return ALL_CAP_RE.sub(r'\1_\2', s).lower()

class SearchRequest(dict):


    SEARCH_TERMS = [
            'principalName',
            'principalId',
            'entityId',
            'firstName',
            'middleName',
            'lastName',
            'emailAddress',
            'phoneNumber',
            'employeeId',
            'campusCode',
            'primaryDepartmentCode',
            'employeeStatusCode',
            'employeeTypeCode',
            'active'
        ]

    def __setattr__(self, name, value):
        if name in SearchRequest.SEARCH_TERMS:
            super(dict, self).__setattr_(name, value)
            return True
        else:
            return False


def set_search_request_attr(term):
    def fn(self, value):
        self[term] = value
    return fn

for term in SearchRequest.SEARCH_TERMS:
    setattr(
        SearchRequest,
        'set_%s' % (conv_to_snake_case(term),),
        set_search_request_attr(term)
    )
