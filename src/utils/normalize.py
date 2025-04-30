def normalize_empty_to_none(obj):
    """
    Convierte cadenas vacías ("") en None en todos los atributos de tipo str de un modelo SQLAlchemy.
    """
    if not hasattr(obj, "__table__"):
        return

    for attr in dir(obj):
        if not attr.startswith("_") and isinstance(getattr(obj, attr, None), str):
            if getattr(obj, attr) == "":
                setattr(obj, attr, None)
