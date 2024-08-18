from .controllers.location_controller import insert_locations
from .services.location_service import LocationService
from .tables.location_table import LocationTable, table_registry

__all__ = [
    'LocationTable',
    'table_registry',
    'LocationService',
    'insert_locations',
]
