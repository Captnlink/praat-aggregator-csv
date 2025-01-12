

from .normalized_time import deserialize_norm_time_from_csv
from .metadata import deserialize_metadata_from_file

def get_serializer(format:str):
    if format == 'normtimef0' or \
       format == 'normtime_f0acceleration' or \
       format == 'normtime_f0velocity' or \
       format == 'normtime_semitonef0':
        return deserialize_norm_time_from_csv
    elif format == 'metadata':
        return deserialize_metadata_from_file
    else:
        raise ValueError(format)



