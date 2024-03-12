from entities.Vehicle import Vehicle


def serialize_complex_obj(o):
    if isinstance(o, Vehicle):
        return {
            'x1': o.x1,
            'y1': o.y1,
            'x2': o.x2,
            'y2': o.y2,
            'track_id': o.track_id}
    # You can add more isinstance checks for other custom objects
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
