import sys

from a3d_cli import __version__, config, dictparser, interface
from a3d_cli.exceptions import A3DValidationError


def cli(  # pylint: disable=too-many-arguments,too-many-locals
    action,
    username,
    password,
    order_types=None,
    catalogue_item_id=None,
    required_date=None,
    gender=None,
    birth_year=None,
    surgery=None,
    notes=None,
    base_url=None,
    order_id=None,
    dicom_location=None,
    verify=True,
):

    if action == "create":

        check_variables(
            dicom_location=dicom_location,
            order_types=order_types,
            catalogue_item_id=catalogue_item_id,
            required_date=required_date,
            gender=gender,
            birth_year=birth_year,
            surgery=surgery,
            notes=notes,
        )

        api = initialize_app(base_url, verify)

        try:
            api.check_dicom_location(dicom_location)
        except A3DValidationError as validation_error:
            print(validation_error)
            sys.exit()

        try:
            valid_required_date = api.check_required_date(required_date)
        except A3DValidationError as validation_error:
            print(validation_error)
            sys.exit()

        login(api, username, password)

        try:
            valid_order_type_ids = api.check_order_types(order_types)
            valid_catalogue_item_id = api.check_catalogue_item_id(catalogue_item_id)
        except A3DValidationError as validation_error:
            print(validation_error)
            sys.exit()

        order = create_and_set_order(
            api,
            valid_order_type_ids,
            valid_catalogue_item_id,
            valid_required_date,
            gender,
            birth_year,
            surgery,
            notes,
        )
        order_id = order["id"]
        upload_files(api, dicom_location)
        complete_upload(api)
        return order_id

    if action == "upload":
        if order_id is None:
            print("Must specify Order ID")
            sys.exit()
        api = initialize_app(base_url, verify)
        login(api, username, password)
        get_order(api, order_id)
        upload_files(api, dicom_location)
        complete_upload(api)
        return order_id

    return None


def initialize_app(base_url, verify):
    print("Connecting to: %s" % base_url)
    return interface.A3dCliInterface(base_url, verify=(verify == "True"))


def login(api, username, password):
    print("\nLogin as user: " + username)
    return check_error_response(api.login(username, password))


def check_error_response(response):
    if "error" in response:
        print("\nAn error has occurred: " + response["error"])
        sys.exit()
    return response


def create_and_set_order(api, *args):
    print("\nCreating new order")
    create_order_response = api.create_order(*args)
    order = check_error_response(create_order_response)
    order = api.get_order(order["id"])
    print("Order " + str(order["displayOrderNo"]) + " created")
    check_error_response(api.update_order(order))
    return order


def upload_files(api, dicom_location):
    print("\nUploading files from folder: " + dicom_location)
    return api.upload_files(dicom_location)


def complete_upload(api):
    print("\nStart DICOM parse")
    return check_error_response(api.complete_upload())


def get_order(api, order_id):
    print("\nRetrieving order " + order_id)
    return check_error_response(api.get_order(order_id))


def check_variables(**kwa):
    error = False
    for key, value in kwa.items():
        if value is None:
            print("Missing variable '" + key + "'")
            error = True
    if error:
        print("Use: a3dcli --help")
        sys.exit()


def build_args():
    """Build arguments parser"""
    arg_parser = dictparser.DictParser(
        prog="a3dcli",
        description="Axial3D CLI (%s)" % __version__,
    )

    # Mandatory args
    arg_parser.add_argument("action", choices=["create", "upload"], help="Create Order, Upload by order id")

    arg_parser.add_argument("--config_file", required=True, help="a3dcli config file")

    # Optional args
    arg_parser.add_argument("--order-type", help="Order Types", nargs="*", dest="order_types")

    arg_parser.add_argument("--catalogue-item-id", help="Catalogue Item", nargs="?", type=int, dest="catalogue_item_id")

    arg_parser.add_argument("--surgery", help="Surgery", nargs="?")

    arg_parser.add_argument("--required-date", help="Required Date", nargs="?")

    arg_parser.add_argument("--patient-gender", help="Gender", nargs="?", choices=["M", "F", "U"], dest="gender")

    arg_parser.add_argument("--patient-birth-year", help="Gender", nargs="?", type=int, dest="birth_year")

    arg_parser.add_argument("--notes", help="Notes", nargs="?")

    arg_parser.add_argument("--base_url", help="Base url of axial3D API")

    arg_parser.add_argument("--verify", action="store_true")

    arg_parser.add_argument("--username", help="axial3D account username")

    arg_parser.add_argument("--password", help="axial3D account password")

    arg_parser.add_argument("--order_id", help="ID of the order")

    arg_parser.add_argument("--dicom_location", help="Path to DICOM files")

    return arg_parser


def main():
    parser = build_args()
    cli_args = parser.parse_args_dict()

    config_file = cli_args.pop("config_file")
    config_data = config.parse_config(config_file)
    if "config_connection" in config_data:
        args = config_data["config_connection"]
    if "config_default_order" in config_data:
        args.update(config_data["config_default_order"])
    args.update(cli_args)

    cli(**args)


if __name__ == "__main__":
    main()
