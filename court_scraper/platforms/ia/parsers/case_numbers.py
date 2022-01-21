from . import case_types


def parse(case_number):
    """
    Parses Iowa case numbers to separate the case type from the case identifier.
    """
    id_ = case_number[2:]
    type_ = case_number[:2]
    return {
        "type_id": type_,
        "type_name": case_types.LOOKUP_BY_ID.get(type_),
        "id": id_,
    }
