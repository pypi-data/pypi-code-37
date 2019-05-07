from ..codenames import (
    account_manager,
    administration,
    auditor,
    clinic,
    data_manager,
    everyone,
    export,
    lab,
    lab_view,
    pharmacy,
    pii,
    pii_view,
)
from .group_names import (
    ACCOUNT_MANAGER,
    ADMINISTRATION,
    PII_VIEW,
    EVERYONE,
    AUDITOR,
    CLINIC,
    LAB,
    LAB_VIEW,
    PHARMACY,
    PII,
    EXPORT,
    DATA_MANAGER,
)

DEFAULT_CODENAMES = {
    ACCOUNT_MANAGER: account_manager,
    ADMINISTRATION: administration,
    AUDITOR: auditor,
    CLINIC: clinic,
    DATA_MANAGER: data_manager,
    EVERYONE: everyone,
    EXPORT: export,
    LAB: lab,
    LAB_VIEW: lab_view,
    PHARMACY: pharmacy,
    PII: pii,
    PII_VIEW: pii_view,
}
