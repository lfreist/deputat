"""
Author: Leon Freist <freist.leon@gmx.de>
"""

import os

# dictionary for subjects
SUBJECT_LONG_DICT = {
    'Mathe': 'M',
    'Deutsch': 'D',
    'Englisch': 'E',
    'Sport': 'S'
}

# reversed dictionary for subjects
SUBJECT_SHORT_DICT = {short: long for long, short in SUBJECT_LONG_DICT.items()}


class Subject:
    def __init__(self, name: str=None, hours: int=None, teacher: str=None):
        pass


class Class:
    def __init__(self, level: int, name: str, subjects: dict):
        self.level = level
        self.name = name
        self.subjects = subjects


    def __str__(self):
        return f'Klasse:\t {self.level}{self.name}\n' \
               f'Fächer:\t {self._get_subjects()}'


    def list_it(self):
        return [self.level, self.name, ';'.join(self.subjects_to_list())]


    def subjects_to_list(self):
        liste = []
        for i in self.subjects:
            liste.append(str(i + f'-{self.subjects[i][0]}-{self.subjects[i][1]}'))
        return liste


    def _get_subjects(self):
        text = ''
        for i in self.subjects:
            text += i + f' ({self.subjects[i][0]} Stunden) bei {self.subjects[i][1]}\n\t\t '
        return text


    def get_fullname(self):
        return f'{self.level}{self.name}'


    def hours_missing(self):
        for i in self.subjects:
            if self.subjects[i][1] == 'null':
                return True
        return False


    def list_teachers(self):
        teachers = []
        for i in self.subjects:
            if self.subjects[i][1] not in teachers and self.subjects[i][1] != 'null':
                teachers.append(self.subjects[i][1])
        return teachers


class Teacher:
    def __init__(self, name: str, short: str, hours: int, subjects: list):
        assert hours >= 0, f'{name} hat weniger als 0 Stunden ({hours}).'
        self.name = name
        self.short = short
        self.hours = hours
        self.subjects = subjects
        self.hours_left = hours


    def __str__(self):
        subs = [SUBJECT_SHORT_DICT[s] for s in self.subjects]
        text = f'Name:\t {self.name} ({self.short})\n' \
               f'Fächer:\t {", ".join(subs)}\n' \
               f'Stunden: {self.hours} ({self._get_hours_left()} h übrig)'
        return text


    def __repr__(self):
        return f'Teacher({self.name}, {self.short}, {self.hours}, {self.subjects})'


    def list_it(self):
        return [self.name, self.short, str(self.hours), ';'.join(self.subjects)]


    def _get_hours_left(self):
        teached_hours = []
        for c in AllClasses.classes:
            for s in c.subjects:
                if c.subjects[s][1] == self.short:
                    teached_hours.append(int(c.subjects[s][0]))
        return self.hours - sum(teached_hours)



class AllTeachers:
    teachers = []
    backup = []
    filename = 'lehrer.csv'

    def read_data(self, additional=False):
        if not additional:
            self.teachers = []
        build_data(self.filename)

    def save_data(self):
        save_data(self.filename)

class AllClasses:
    classes = []
    backup = []
    filename = 'klassen.csv'

    def read_data(self, additional=False):
        if not additional:
            self.classes = []
        build_data(self.filename)

    def save_data(self):
        save_data(self.filename)



def build_object(line: list, typ: str) -> bool:
    if typ == 'lehrer.csv':
        name, short, hours, subjects = line[0], line[1], int(line[2]), line[3]
        AllTeachers.teachers.append(Teacher(name, short, hours, subjects))
        return True
    elif typ == 'klassen.csv':
        level, name, subjects = line[0], line[1], line[2]
        AllClasses.classes.append(Class(level, name, subjects))
        return True
    elif typ == 'fach':
        return True
    return False


def build_data(filename: str):
    with open(os.path.join(os.path.split(os.getcwd())[0], 'data', filename), 'r') as file:
        lines = file.readlines()[1:]
    for line in lines:
        line = line.strip().split(',')
        if filename == 'lehrer.csv':
            line[-1] = line[-1].split(';')
        elif filename == 'klassen.csv':
            line[-1] = line[-1].split(';') # 'S-2-null'
            new = {}
            for fach in line[-1]:
                fach = fach.split('-') # ['S', '2', 'null']
                fach[1] = int(fach[1])
                new[fach[0]] = fach[1:]
            line[-1] = new
        build_object(line, filename)


def save_data(filename: str):
    path = os.path.join(os.path.split(os.getcwd())[0], 'data', filename)
    try:
        file = open(path, 'w')
        if filename == 'lehrer.csv':
            print('name,kürzel,stunden,fächer', file=file)
            for obj in AllTeachers.teachers:
                print(",".join(obj.list_it()), file=file)
        elif filename == 'klassen.csv':
            print('klassenstufe,name,fächer(fach-stundenzahl-lehrer)', file=file)
            for obj in AllClasses.classes:
                print(",".join(obj.list_it()), file=file)
        file.close()
    except TypeError as error:
        print(error)


AllClasses().read_data()
AllTeachers().read_data()