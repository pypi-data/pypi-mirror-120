from datetime import datetime, timedelta


class A3DValidationError(Exception):
    pass


class A3DRequiredDateError(A3DValidationError):
    def __init__(self, given_date):
        super().__init__()
        self.given_date = given_date

        five_days = datetime.utcnow() + timedelta(days=5)

        self.valid_examples = [
            five_days.strftime("%Y-%m-%d"),
            five_days.strftime("%d/%m/%y"),
            five_days.strftime("%A %d. %B %Y"),
            five_days.isoformat(),
        ]

    def __str__(self):
        return "The given date '%s' cannot be parsed. Some examples are %s." % (
            self.given_date,
            ", ".join("'%s'" % valid_date for valid_date in self.valid_examples),
        )


class A3DOrderTypeError(A3DValidationError):
    def __init__(self, given_types, valid_types):
        super().__init__()
        self.given_types = given_types
        self.valid_types = valid_types

    def __str__(self):

        invalid_types = [t for t in self.given_types if t not in self.valid_types]

        return "The order types %s are invalid. Valid values are %s." % (
            ", ".join("'%s'" % order_type for order_type in invalid_types),
            ", ".join("'%s'" % order_type for order_type in self.valid_types),
        )


class A3DCatalogueError(A3DValidationError):
    def __init__(self, given_category, valid_categories):
        super().__init__()
        self.given_category = given_category
        self.valid_categories = valid_categories

    def __str__(self):

        valid_values_output = ""
        for category_id, category_data in sorted(self.valid_categories.items()):
            valid_values_output += "%s : %s\n" % (category_id, category_data["name"])

        return "The given category %s is invalid. Valid category ids are:\n%s." % (
            self.given_category,
            valid_values_output,
        )
