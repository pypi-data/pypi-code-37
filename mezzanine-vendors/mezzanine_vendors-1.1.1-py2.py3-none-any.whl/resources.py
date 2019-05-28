from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget

from .models import Vendor, Subject, Type


class VendorResource(ModelResource):
    """
    Handles importting vendors
    """
    types = Field(
        attribute="types", widget=ManyToManyWidget(model=Type, field="title"))
    subjects = Field(
        attribute="subjects", widget=ManyToManyWidget(model=Subject, field="title"))

    class Meta:
        model = Vendor
        import_id_fields = ("title",)
        skip_unchanged = True
        report_skipped = True
        fields = (
            "title", "phone", "email", "website", "description", "subjects", "types",
            "address", "city", "state")

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Lowercase headers to match field names
        if dataset.headers:
            dataset.headers = [str(header).lower().strip() for header in dataset.headers]

    def before_import_row(self, row, **kwargs):
        # Trim description whitespace
        try:
            row["description"] = row["description"].strip()
        except KeyError:
            pass

        # If city and state are provided separately, append them to the address
        # This will improve geocoder results later
        try:
            address = [row["address"]]
            if row["city"]:
                address.append(row["city"].strip())
            if row["state"]:
                address.append(row["state"].strip())
            row["address"] = ", ".join(address)
        except KeyError:
            pass
