def normalize_empty_to_none(obj):
    for attr in obj.__mapper__.column_attrs:
        val = getattr(obj, attr.key)
        if isinstance(val, str) and val.strip() == "":
            setattr(obj, attr.key, None)
