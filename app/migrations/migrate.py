from app.admin.models.migrations import Migrations
from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
import importlib
import json
import os

 
class MigrateDatas:
    def __init__(self, data_base_url=settings.database_sync) -> None:
        self.data_base_url = data_base_url
        pass

    def get_data_json(self, migrations_dir=settings.migrations_dir):
        existing_files = os.listdir(migrations_dir)
        existing_files.sort()
        data_files = []

        for files in existing_files:
            with open(f"{migrations_dir}/{files}", "r") as f:
                data_files.append(json.load(f))

        return data_files

    def add_data(self, migrations_dir=settings.migrations_dir):
        data_files = self.get_data_json(migrations_dir)
        data = []

        engine = create_engine(self.data_base_url)
        db = Session(bind=engine)

        for i in data_files:

            try:
                migrations_name = i['migrations']
                model_name = i['model']
                module = i['module']
                model_class = getattr(importlib.import_module(
                    f'app.{module}.models'), model_name)
                model_data = i['data']
                update = i['update']

            except Exception as e:
                print(f"Error on processing migrations: {e}")
                return None

            if not self.check_migrations(db, migrations_name):

                instance_migrations = Migrations(name=migrations_name)
                db.add(instance_migrations)
                try:

                    for data in model_data:
                        id = data['data']['id']
                        if update:
                            existing_record = db.query(model_class).filter_by(
                                id=id).first()
                            if existing_record:
                                for key, value in data['data'].items():
                                    setattr(existing_record, key, value)
                        else:
                            instance = model_class(**data['data'])
                            db.add(instance)

                        if 'model_relationship' in data:
                            self.model_relationships(
                                db,
                                model_class,
                                data,
                                existing_record if update else instance)

                    db.commit()
                    print(f"Migrations completed - {migrations_name}")
                    db.close()
                except Exception as e:
                    print(e)
                    db.rollback()
            else:
                print(f"Migration unchanged - {migrations_name}")
            db.close()

    def check_migrations(self, db, migrations_name):
        exist = db.query(Migrations).filter(
            Migrations.name == migrations_name).first()
        return True if exist else False

    def model_relationships(self, db, model_parent, data, instance):
        model_mapper = inspect(model_parent)
        model_relationship = data['model_relationship']['model']
        child_model = model_mapper.relationships[model_relationship].mapper.class_

        children_data = data['model_relationship']['data']
        data_child_ids = [child['id'] for child in children_data]

        children = db.query(child_model).filter(
            child_model.id.in_(data_child_ids)).all()

        getattr(instance, model_relationship).extend(children)
