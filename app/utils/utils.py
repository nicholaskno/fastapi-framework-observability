from app.exceptions.exceptions import UnprocessableEntity
from typing import List, Tuple
from sqlalchemy.orm import Session

"""
Check if an id exist on a table, can check multiples
db: database object
data_list: [(MODEL_OBJ, id, label), ...]
"""
def utils_check_id(db: Session, data_list: List[Tuple], _exception = UnprocessableEntity):
    for data in data_list:
        _exists = db.query(data[0]).get(data[1])

        if _exists is None:
            raise _exception(f"{data[2]} doesn't exists!")
