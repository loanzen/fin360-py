import requests
from attrdict import AttrDict


class Fin360ApiException(Exception):

    def __init__(self, status, description):
        description_map = {
            400: "Bad Request",
            401: "Invalid Access Token",
            403: "Access Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }
        self.status = status
        self.description = description_map[status]
        super(Fin360ApiException, self).__init__(description)

    def to_dict(self):
        return {
            'status': self.status,
            'description': self.description
        }

    def __str__(self):
        return super(Fin360ApiException, self).__str__()


class Fin360Client(object):
    def __init__(self, **kwargs):
        self.access_token = kwargs.get('access_token', None)

    def authenticate(self, email, password):

        url = "https://www.fin360.in/bank-auth/api/v1/login"

        data = {"emailAddress": email, "password": password}
        response = requests.request("POST", url, data=data)

        if response.status_code is not 200:
            raise Fin360ApiException(response.status_code, response.text)

        self.access_token = response.json()['access_token']

        return AttrDict(response.json())
