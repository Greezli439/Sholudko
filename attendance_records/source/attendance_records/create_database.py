"""
Read data from file and write data in to DB
"""


from peewee import *
from main import read_files


PATH = '/home/mykhailo/Hillel/Final_Project/Sholudko/data'
db = SqliteDatabase('people.db')


class BaceModel(Model):
    class Meta:
        database = db


class PersonModel(BaceModel):
    crew_id = CharField()
    name = CharField()


class EnterModel(BaceModel):
    person = ForeignKeyField(PersonModel)
    date = DateField()
    time = TimeField()


class ExitModel(BaceModel):
    person = ForeignKeyField(PersonModel)
    date = DateField()
    time = TimeField()


def fill_table(path):
    """
    read data from file and write data in to DB
    :param path: Path
    :return: None
    """
    crew, enter, exit_f = read_files(path)
    for line in crew:
        person = {
            'crew_id': (crew_id := line.split(' |')[0]),
            'name': line.split(' |')[1].replace('\n', '')
        }
        person_obj = PersonModel.create(**person)

        for line in enter:
            id_p, datetime = line.split(' |')
            date, time = datetime.split()
            if crew_id != id_p:
                continue
            EnterModel.create(person=person_obj, date=date, time=time)

        for line in exit_f:
            id_p, datetime = line.split(' |')
            date, time = datetime.split()
            if crew_id != id_p:
                continue
            ExitModel.create(person=person_obj, date=date, time=time)


if __name__ == '__main__':
    db.connect()
    db.create_tables([PersonModel, EnterModel, ExitModel])
    fill_table(PATH)

