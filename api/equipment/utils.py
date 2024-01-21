from db import get_db

#################################
## EQUIPMENT UTILITY FUNCTIONS ##
#################################


def check_if_equipment_exists(id):
    db = get_db()
    equipment = db.execute(
        'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
    if equipment is None:
        return False
    return True
