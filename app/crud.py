from sqlalchemy import select
from app.models import Activity
from math import radians, sin, cos, sqrt, atan2


async def get_activity_tree_ids(db, root_id: int) -> list[int]:
    result = await db.execute(select(Activity))
    activities = result.scalars().all()

    tree = {}
    for act in activities:
        tree.setdefault(act.parent_id, []).append(act)

    ids = []

    def collect(parent_id):
        for act in tree.get(parent_id, []):
            ids.append(act.id)
            collect(act.id)

    ids.append(root_id)
    collect(root_id)

    return ids


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2)**2

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
