"""
Module a3dcli
================
This is the command line interface (cli) to the axial3D (a3d) API
"""

import itertools
import json
import os
import sys

import requests
from dateutil.parser import ParserError, parse

from . import __version__, exceptions


class A3dCliInterface:
    def __init__(self, base_url="https://localhost:8443", verify=True):
        """Init the class with the IP of the backend API"""
        self.jwt = None
        self.current_order = None
        self.base_url = base_url
        self.verify = verify

        self._order_types = {}
        self._catalogue = {}

        if not verify:
            requests.packages.urllib3.disable_warnings(  # pylint: disable=no-member
                requests.packages.urllib3.exceptions.InsecureRequestWarning  # pylint: disable=no-member
            )

    def base_headers(self):
        return {
            "User-Agent": "a3dcli %s" % __version__,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "Bearer {}".format(self.jwt),
            "Content-Type": "application/json;",
        }

    def send_request(self, method, endpoint, files=None, **data):
        request = getattr(requests, method)
        url = self.build_url(endpoint)
        request_data = self.build_data(**data)
        headers = self.base_headers()

        if request_data:
            response = request(url, json.dumps(request_data), files=files, verify=self.verify, headers=headers)
        else:
            response = request(url, files=files, verify=self.verify, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                print(response.json())
            except json.JSONDecodeError:
                print(response.content.decode("utf-8"))
            raise

        try:
            return response.json()
        except json.JSONDecodeError:
            return response.content.decode("utf-8")

    def build_url(self, end_point):
        return self.base_url + end_point

    def build_data(self, **data):
        params = {"jwt": self.jwt, "order": json.dumps(self.current_order)}
        params.update(data)
        return params

    def login(self, username, password):
        """Login to the webapp, the returned JWT is saved as a class variable which is used in all the other requests"""

        url = self.build_url("/api/v2/login")
        response = requests.post(
            url,
            json={"username": username, "password": password},
            verify=self.verify,
        )
        response.raise_for_status()
        data = response.json()
        self.jwt = data["jwt"]

        self._order_types = self.fetch_order_types()
        self._catalogue = self.fetch_catalogue()

        return response

    def fetch_catalogue(self):
        url = self.build_url("/api/catalogue/items")

        response = requests.get(url, verify=self.verify, headers=self.base_headers())

        response.raise_for_status()

        return {catalogue_item["id"]: catalogue_item for catalogue_item in response.json()}

    def fetch_order_types(self):
        url = self.build_url("/api/orderTypes")

        response = requests.get(url, verify=self.verify, headers=self.base_headers())

        response.raise_for_status()

        return {order_type["name"]: order_type for order_type in response.json()}

    def check_catalogue_item_id(self, catalogue_item_id):
        if catalogue_item_id not in self._catalogue.keys():
            raise exceptions.A3DCatalogueError(catalogue_item_id, self._catalogue)

        return self._catalogue[catalogue_item_id]["id"]

    def check_order_types(self, order_types):
        if not all(ot in self._order_types.keys() for ot in order_types):
            raise exceptions.A3DOrderTypeError(order_types, list(self._order_types.keys()))

        return [self._order_types[order_type]["id"] for order_type in order_types]

    @staticmethod
    def check_required_date(date_string):
        try:
            valid_datetime = parse(date_string)
        except ParserError as parse_exception:
            raise exceptions.A3DRequiredDateError(date_string) from parse_exception

        return valid_datetime

    @staticmethod
    def check_dicom_location(dicom_location):
        if not os.path.isdir(dicom_location):
            raise exceptions.A3DValidationError("Directory '%s' is not a valid directory" % dicom_location)

    def create_order(  # pylint: disable=too-many-arguments
        self,
        order_type_ids,
        catalogue_item_id,
        required_date,
        gender,
        birth_year,
        surgery,
        notes,
    ):
        """Creates a new order, the order is returned and saved as a class variable for future calls"""

        post_data = {
            "catalogueItemId": catalogue_item_id,
            "orderTypeIds": order_type_ids,
            "patientBirthYear": birth_year,
            "patientGender": gender,
            "userId": 1,
            "requiredDate": required_date.isoformat(),
            "surgery": surgery,
            "notes": notes,
        }

        response_data = self.send_request("post", "/api/v3/orders", **post_data)
        self.current_order = response_data
        return response_data

    def get_order(self, order_id):
        """Retrieves an order with its OrderID"""
        data = self.send_request(
            "get",
            "/api/v3/orders/%s" % order_id,
        )
        self.current_order = data
        return data

    def update_order(self, order=None, **new_params):
        """
        Updates an order. Multiple calls possible
         * Sending a whole order, without params
         * Sending a whole order, with a params dict. This dict will update the sent order
         * Nothing , which will send the class 'current_order'
         * Just the params dict, which will update the values of the class 'current_order'
        """
        if order is None:
            if self.current_order is None:
                raise ValueError("Order is not set")
            order = self.current_order

        for param, value in new_params.items():
            if param in order:
                order[param] = value

        self.current_order = order

        return self.send_request(
            "patch",
            "/api/v3/orders/%s" % order["id"],
        )

    def upload_files(self, path, order=None, chunk_size=10):
        """Upload all the DICOM files from a path to an order"""
        if order is None:
            if self.current_order is None:
                return
            order = self.current_order

        dicom_files = list(self.list_dicom_from_dir(path))
        files = []
        for i, dicom in enumerate(dicom_files):
            sys.stdout.flush()
            with open(dicom, "rb") as fid:
                fid.seek(0)
                data = fid.read()
                files.append((str(i), data))
            if (i + 1) % chunk_size == 0 or (i + 1) == len(dicom_files):
                if len(files) > 0:
                    endpoint = "/api/v3/orders/%s/uploads/9999" % order["id"]
                    url = self.build_url(endpoint)
                    headers = {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Authorization": "Bearer {}".format(self.jwt),
                        "Content-Type": "application/octet-stream;",
                    }

                    requests.put(url, files=files, verify=self.verify, headers=headers)
                    files = []
        return

    def complete_upload(self, order=None):
        """Complete upload and trigger parse"""
        if order is None:
            if self.current_order is None:
                raise ValueError("Order is not set")
            order = self.current_order

        order_id = order["id"]
        return self.send_request("post", "/api/v3/orders/%s/uploadComplete" % order_id)

    def list_files_recursive(self, path):
        """list all files under a directoy tree"""
        flist = list_files(path)
        recursive = itertools.chain.from_iterable(self.list_files_recursive(hpath) for hpath in list_dirs(path))
        return itertools.chain.from_iterable([flist, recursive])

    def list_dicom_from_dir(self, path):
        """
        Retrieves all the DICOM files from path (including subfolders)
        Only non extension files, 'dcm', 'dicom' or 'ima'
        """
        return self.list_files_recursive(path)


def list_files(path):
    """list only files from a path"""
    names = os.listdir(path)
    gen = filter(lambda name: os.path.isfile(os.path.join(path, name)), names)
    gen = (os.path.join(path, name) for name in gen)
    return gen


def list_dirs(path):
    """list only files from a path"""
    names = os.listdir(path)
    gen = filter(lambda name: os.path.isdir(os.path.join(path, name)), names)
    gen = (os.path.join(path, name) for name in gen)
    return gen
