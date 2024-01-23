from sqlite3 import Row
from api.db import get_db
from typing import Optional
from wtforms import Form, TextAreaField, StringField, validators


class EquipmentForm(Form):
    name = StringField('Name', validators=[validators.Length(min=4, max=50)])
    description = TextAreaField('Description', validators=[
                                validators.Length(min=4, max=200)])


class Equipment():
    table_name = 'equipment'

    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        """Convert the Equipment object to a dictionary."""
        return {'id': self.id, 'name': self.name, 'description': self.description}

    def save(self):
        """Save or update the Equipment object in the database."""
        db = get_db()
        if self.id:
            # Update existing equipment
            db.execute('UPDATE equipment SET name = ?, description = ? WHERE id = ?', 
                       (self.name, self.description, self.id))
        else:
            # Insert new equipment
            cursor = db.execute('INSERT INTO equipment (name, description) VALUES (?, ?)', 
                                (self.name, self.description))
            self.id = cursor.lastrowid
        db.commit()

    @staticmethod
    def from_row(row: Row) -> 'Equipment':
        id, name, description = row
        return Equipment(id, name, description)

    @staticmethod
    def get(id: int) -> Optional['Equipment']:
        db = get_db()
        equipment = db.execute(
            'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
        if equipment:
            return Equipment(id=equipment['id'], name=equipment['name'], description=equipment['description'])
        return None

    @staticmethod
    def get_all() -> list['Equipment']:
        db = get_db()
        equipment_rows = db.execute('SELECT * FROM equipment').fetchall()
        return [Equipment.from_row(row) for row in equipment_rows]

    @classmethod
    def all(cls) -> 'EquipmentCollection':
        """Return a collection of all Equipment objects."""
        db = get_db()
        equipment_rows = db.execute('SELECT * FROM equipment').fetchall()
        equipment_objects = [cls(id=row['id'], name=row['name'],
                                 description=row['description']) for row in equipment_rows]
        return EquipmentCollection(equipment_objects)

    @staticmethod
    def from_dict(data):
        return Equipment(id=data.get('id'), name=data.get('name'), description=data.get('description'))


class EquipmentCollection(Equipment):
    def __init__(self, equipment_list):
        self.equipment_list = equipment_list

    def serialize(self) -> list[dict[str, str]]:
        """Convert the EquipmentCollection object to a list of dictionaries."""
        return [equipment.to_dict() for equipment in self.equipment_list]
