import base64
import datetime
import hashlib
import json
from urllib.parse import urljoin

import requests

bucket_name = 'upload.dev.vankrupt.io'
md5_hash = hashlib.md5()


def auth_check(f):
    def wrapper(*args, **kwargs):
        assert args[0].authenticated
        access_token = args[0]._access_token
        payload = access_token.split('.')[1] + '='
        payload = base64.decodebytes(bytes(payload, 'utf-8'))
        payload = json.loads(payload)
        exp = int(payload['exp'])
        exp = datetime.datetime.fromtimestamp(exp)
        if exp <= datetime.datetime.now():
            args[0].refresh_token()

        return f(*args, **kwargs)

    return wrapper


def notify_dedup_service(url, upload_id, upload_size, file_md5):
    notification = {
        "message": {
            "attributes": {
                "eventType": "OBJECT_FINALIZE",
                "payloadFormat": "JSON_API_V1",
            },
            "data": base64.encodebytes(json.dumps({
                "bucket": bucket_name,
                "id": "random id",
                "selfLink": "str",
                "name": upload_id,
                "size": upload_size,
                "md5Hash": file_md5,
                "timeCreated": "str",
            }).encode()).decode()
        }
    }
    requests.post(
        url,
        json=notification,
    )


class CreatorClient:
    def __init__(
            self,
            local_testing: bool = False,
            api_url: str = 'https://api.dev.vankrupt.io',
    ):
        # make sure that, if testing, all needed values are provided
        # assert not local_testing or map_processing_url
        assert not local_testing or api_url != 'https://api.dev.vankrupt.io'

        self._local_testing = local_testing
        self._api_url = api_url
        self._local_mapprocessing_url = 'http://localhost:9000/uploaded'
        self._auth_header = None
        self._access_token = None
        self._refresh_token = None

        self.authenticated = False

    @staticmethod
    def xml_upload(map_file, policy_document, file_name):
        files = {
            "file": (file_name, map_file)
        }

        return requests.post(
            policy_document['url'],
            data=policy_document['fields'],
            files=files,
        )

    @staticmethod
    def local_upload(map_file, object_name):
        """
        curl -X POST --data-binary @OBJECT_LOCATION \
            -H "Authorization: Bearer OAUTH2_TOKEN" \
            -H "Content-Type: OBJECT_CONTENT_TYPE" \
            ""
        """
        return requests.post(
            f'http://localhost:8081/upload/storage/v1/b/{bucket_name}/o?uploadType=media&name={object_name}',
            data=map_file,
        )

    def register(self, user: dict):
        response = requests.post(
            urljoin(self._api_url, '/users/'),
            json=user
        )
        return response

    def authenticate(self, username: str, password: str) -> dict:
        response = requests.post(
            urljoin(self._api_url, '/token'),
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
            }
        )
        self._auth_header = {
            'Authorization': 'Bearer ' + response.json()['access_token']
        }
        self._access_token = response.json()['access_token']
        self._refresh_token = response.json()['refresh_token']
        self.authenticated = True
        return self._auth_header

    def refresh_token(self):
        if not self._refresh_token:
            raise EnvironmentError

        response = requests.post(
            urljoin(self._api_url, '/token/'),
            json={
                "refresh_token": self._refresh_token,
            }
        )
        self._auth_header = {
            'Authorization': 'Bearer ' + response.json()['access_token']
        }
        self._access_token = response.json()['access_token']
        self._refresh_token = response.json()['refresh_token']
        return self._auth_header

    @auth_check
    def get_me(self):
        response = requests.post(
            urljoin(self._api_url, '/users/me'),
            json=map,
            headers=self._auth_header,
        )
        return response

    @auth_check
    def create_map(self, map: dict):
        response = requests.post(
            urljoin(self._api_url, '/maps/'),
            json=map,
            headers=self._auth_header,
        )
        return response

    @auth_check
    def initiate_upload(self, map_id: int, map_version: dict):
        response = requests.post(
            urljoin(self._api_url, f"/maps/{map_id}/initiate_upload/"),
            json=map_version,
            headers=self._auth_header,
        )
        return response

    @auth_check
    def my_maps(self):
        response = requests.get(
            urljoin(self._api_url, "/maps/my/"),
            # self._api_url + f"/maps/my/",
            headers=self._auth_header,
        )
        return response

    def upload_map(self, map_size: int, map_file: bytes, policy_document: dict):
        object_id = policy_document['fields']['key']
        if self._local_testing:
            response = self.local_upload(map_file,
                                         object_name=object_id)

            md5_hash.update(map_file)
            map_md5_hash = base64.encodebytes(md5_hash.digest()).decode()
            notify_dedup_service(
                url=self._local_mapprocessing_url,
                upload_id=object_id,
                upload_size=map_size,
                file_md5=map_md5_hash
            )
        else:
            response = self.xml_upload(map_file, policy_document, file_name=object_id)
        return response
