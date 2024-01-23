from api.db import get_db

class BaseModel:
    table_name = ''  # Should be overridden in child classes

    @classmethod
    def all(cls) -> list['BaseModel']:
        db = get_db()
        rows = db.execute(f'SELECT * FROM {cls.table_name}').fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def get(cls, id):
        db = get_db()
        row = db.execute(f'SELECT * FROM {cls.table_name} WHERE id = ?', (id,)).fetchone()
        if row:
            return cls.from_row(row)
        return None

    def save(self):
        # Implement the save logic, which inserts or updates the record in the database.
        pass

    def delete(self):
        # Implement the delete logic, which removes the record from the database.
        pass

    @staticmethod
    def from_row(row):
        # This method should be implemented in each child class
        raise NotImplementedError

    def to_dict(self):
        # Convert the object to a dictionary. This should be implemented in each child class.
        raise NotImplementedError

class BaseModelCollection:
    def __init__(self, items: list[BaseModel]):
        self.items = items

    def to_list(self):
        return [item.to_dict() for item in self.items]

    def to_dict(self):
        return {'items': self.to_list()}

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]