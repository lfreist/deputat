import os
import sys
sys.path.append('../')
try:
    from deputat import settings
except ImportError:
    import settings


# dictionary for subjects
SUBJECT_LONG_DICT = {
    'Mathe': 'M',
    'Deutsch': 'D',
    'Englisch': 'E',
    'Sport': 'S',
    'Französisch': 'F',
    'Technik': 'T'
}

# reversed dictionary for subjects
SUBJECT_SHORT_DICT = {short: long for long, short in SUBJECT_LONG_DICT.items()}

save = settings.save_dir()


class Class:
    def __init__(self, level: int, name: str, subjects: dict):
        self.level = int(level)
        self.name = name
        self.subjects = subjects


    def __str__(self):
        return f'Klasse:\t {self.level}{self.name}\n' \
               f'Fächer:\t {self._get_subjects()}'

    def __gt__(self, other):
        if self.level == other.level:
            return self.name > other.name
        return self.level > other.level

    def __lt__(self, other):
        if self.level == other.level:
            return self.name < other.name
        return self.level < other.level

    def __eq__(self, other):
        return self.level == other.level and self.name == self.name

    def __repr__(self):
        return f'Class({self.level}, {self.name}, {self.subjects})'


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
        subs = {}
        for s in self.subjects:
            s = SUBJECT_SHORT_DICT[s]
            subs[s] = 0
        for c in AllClasses.classes:
            for s in c.subjects:
                if SUBJECT_SHORT_DICT[s] in subs:
                    if c.subjects[s][1] == self.short:
                        subs[SUBJECT_SHORT_DICT[s]] += int(c.subjects[s][0])
        text = f'Name:\t {self.name} ({self.short})\n' \
               f'Fächer:\t {_build_string_from_dict(subs)}\n' \
               f'Stunden: {self.hours} ({self._get_hours_left()}h übrig)'
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
    filename = 'lehrer.td'

    def read_data(self, path, name=None, additional=False):
        if not additional:
            self.teachers = []
        if name:
            path, name = os.path.split(path)
            read_data(name, path)
        else:
            read_data(path, 'td')


    def save_data(self, location=save):
        save_data(self.filename, location)


    def _list_teacher_hours(self):
        list = []
        for t in self.teachers:
            subs = {}
            for s in t.subjects:
                subs[s] = 0
            for c in AllClasses.classes:
                for s in c.subjects:
                    if s in subs:
                        if c.subjects[s][1] == t.short:
                            subs[s] += int(c.subjects[s][0])
            list.append(f'{t.name}\t({t.short})\t-\t[{_build_string_from_dict(subs)}]')
        return list


    def add_teacher(self, name, short, hours, subjects):
        new = Teacher(name, short, hours, subjects)
        for i in self.teachers:
            if i.short == new.short:
                return False
        self.teachers.append(new)
        return True


class AllClasses:
    classes = []
    backup = []
    filename = 'klassen.cd'

    def read_data(self, path, name=None, additional=False):
        if not additional:
            self.classes = []
        if name:
            path, name = os.path.split(path)
            liste = read_data(path, 'cd', name)
        else:
            liste = read_data(path, 'cd')
        print(liste)
        for i in liste:
            for c in self.classes:
                if not c.get_fullname == i.get_fullname:
                    self.classes.append(i)


    def save_data(self, location=save):
        save_data(self.filename, location)


    def list_levels(self):
        liste = []
        for c in self.classes:
            if str(c.level) not in liste:
                liste.append(str(c.level))
        return liste

    def add_class(self, level, name, subjects):
        new = Class(level, name, subjects)
        self.classes.append(new)
        return True


def _build_string_from_dict(subs: dict):
    text = ""
    for i in subs:
        text += f'{i}: {subs[i]}h, '
    return text[0:-2]


def read_data(path, typ, filename=None):
    if filename:
        print(filename)
        return
    liste = []
    for f in os.listdir(path):
        if typ == 'cd':
            if f.endswith('.cd'):
                with open(os.path.join(path, f), 'r') as file:
                    lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip().split(',')
                    line[-1] = line[-1].split(';')  # 'S-2-null'
                    new = {}
                    for fach in line[-1]:
                        fach = fach.split('-')  # ['S', '2', 'null']
                        fach[1] = int(fach[1])
                        new[fach[0]] = fach[1:]
                    line[-1] = new
                    liste.append(build_object(line, typ))
        elif typ == 'td':
            if f.endswith('.td'):
                with open(os.path.join(path, f), 'r') as file:
                    lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip().split(',')
                    line[-1] = line[-1].split(';')
                    liste.append(build_object(line, typ))
    return liste


def build_object(line: list, typ: str) -> bool:
    if typ == 'td':
        name, short, hours, subjects = line[0], line[1], int(line[2]), line[3]
        return Teacher(name, short, hours, subjects)
    elif typ == 'cd':
        level, name, subjects = line[0], line[1], line[2]
        return Class(level, name, subjects)


def save_data(filename, path=save):
    path = os.path.join(path, filename)
    try:
        file = open(path, 'w')
        if filename.endswith('.td'):
            print('name,kürzel,stunden,fächer', file=file)
            for obj in AllTeachers.teachers:
                print(",".join(obj.list_it()), file=file)
        elif filename.endswith('.cd'):
            print('klassenstufe,name,fächer(fach-stundenzahl-lehrer)', file=file)
            for obj in AllClasses.classes:
                print(",".join(obj.list_it()), file=file)
        file.close()
    except TypeError as error:
        print(error)


if __name__ == '__main__':
    AllTeachers().read_data('/home/lfreist/Documents/projects/deputat/deputat/data')
    AllClasses().read_data('/home/lfreist/Documents/projects/deputat/deputat/data')