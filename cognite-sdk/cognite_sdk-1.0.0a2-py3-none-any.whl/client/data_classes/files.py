from typing import *
from typing import Dict, List

from cognite.client._base import *


# GenClass: FilesMetadata
class FileMetadata(CogniteResource):
    """No description.

    Args:
        external_id (str): External Id provided by client. Should be unique within the project.
        name (str): No description.
        source (str): The source of the file.
        mime_type (str): File type. E.g. pdf, css, spreadsheet, ..
        metadata (Dict[str, Any]): Customizable extra data about the file. String key -> String value.
        asset_ids (List[int]): No description.
        id (int): Javascript friendly internal ID given to the object.
        uploaded (bool): Whether or not the actual file is uploaded. This field is returned only by the API, it has no effect in a post body.
        uploaded_time (int): It is the number of seconds that have elapsed since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        created_time (int): It is the number of seconds that have elapsed since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): It is the number of seconds that have elapsed since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        external_id: str = None,
        name: str = None,
        source: str = None,
        mime_type: str = None,
        metadata: Dict[str, Any] = None,
        asset_ids: List[int] = None,
        id: int = None,
        uploaded: bool = None,
        uploaded_time: int = None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.name = name
        self.source = source
        self.mime_type = mime_type
        self.metadata = metadata
        self.asset_ids = asset_ids
        self.id = id
        self.uploaded = uploaded
        self.uploaded_time = uploaded_time
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cognite_client

    # GenStop


# GenClass: FilesSearchFilter.filter
class FileMetadataFilter(CogniteFilter):
    """No description.

    Args:
        metadata (Dict[str, Any]): Customizable extra data about the event. String key -> String value.
        asset_ids (List[int]): Asset IDs of related equipment that this event relates to.
        source (str): The source of this event.
        created_time (Dict[str, Any]): Range between two timestamps
        last_updated_time (Dict[str, Any]): Range between two timestamps
        external_id_prefix (str): External Id provided by client. Should be unique within the project.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        metadata: Dict[str, Any] = None,
        asset_ids: List[int] = None,
        source: str = None,
        created_time: Dict[str, Any] = None,
        last_updated_time: Dict[str, Any] = None,
        external_id_prefix: str = None,
        cognite_client=None,
    ):
        self.metadata = metadata
        self.asset_ids = asset_ids
        self.source = source
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.external_id_prefix = external_id_prefix
        self._cognite_client = cognite_client

    # GenStop


# GenUpdateClass: FileChange
class FileMetadataUpdate(CogniteUpdate):
    """Changes will be applied to file.

    Args:
        id (int): ID given by the API to the file.
        external_id (str): No description.
    """

    @property
    def source(self):
        return _PrimitiveFileMetadataUpdate(self, "source")

    @property
    def metadata(self):
        return _ObjectFileMetadataUpdate(self, "metadata")

    @property
    def asset_ids(self):
        return _ListFileMetadataUpdate(self, "assetIds")

    @property
    def external_id(self):
        return _PrimitiveFileMetadataUpdate(self, "externalId")


class _PrimitiveFileMetadataUpdate(CognitePrimitiveUpdate):
    def set(self, value: Any) -> FileMetadataUpdate:
        return self._set(value)


class _ObjectFileMetadataUpdate(CogniteObjectUpdate):
    def set(self, value: Dict) -> FileMetadataUpdate:
        return self._set(value)

    def add(self, value: Dict) -> FileMetadataUpdate:
        return self._add(value)

    def remove(self, value: List) -> FileMetadataUpdate:
        return self._remove(value)


class _ListFileMetadataUpdate(CogniteListUpdate):
    def set(self, value: List) -> FileMetadataUpdate:
        return self._set(value)

    def add(self, value: List) -> FileMetadataUpdate:
        return self._add(value)

    def remove(self, value: List) -> FileMetadataUpdate:
        return self._remove(value)

    # GenStop


class FileMetadataList(CogniteResourceList):
    _RESOURCE = FileMetadata
    _UPDATE = FileMetadataUpdate
