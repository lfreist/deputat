#  -*- coding: utf-8 -*-
"""
GUI
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
                             QTabWidget, QComboBox,
                             QCheckBox)

from deputat import AllTeachers, AllClasses, SUBJECT_SHORT_DICT


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = 'Übersicht'
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 1250, 500)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        view_menu = menu_bar.addMenu('View')

        self.setCentralWidget(MainWidget(self))


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ----------------create GroupBoxes-------------
        self.createTLGB()
        self.createBLGB()
        self.createTRGB()
        self.createBRGB()
        # ----------------end GroupBoxes----------------

        # ----------------main Layout-------------------
        main_layout = QHBoxLayout()

        left_area = QVBoxLayout()
        right_area = QVBoxLayout()
        left_area.addWidget(self.TLGB)
        left_area.addWidget(self.BLGB)
        right_area.addWidget(self.TRGB)
        right_area.addWidget(self.BRGB)

        main_layout.addLayout(left_area)
        main_layout.addLayout(right_area)

        self.setLayout(main_layout)
        # ----------------end main Layout----------------


    def createTLGB(self):
        """
        places GroupBox to top-left
        """

        self.TLGB = QGroupBox('Suchoptionen für Klassen')
        layout = QVBoxLayout()
        sublayout_top = QHBoxLayout()
        sublayout_bot = QHBoxLayout()

        level_label = QLabel('Klassenstufe: ')
        self.select_level = QComboBox()
        self.select_level.addItems(['Alle'] + self._get_class_levels())

        self.hours_missing = QCheckBox('Nur Klassen mit fehlenden Stunden')
        self.done_classes = QCheckBox('Nur volltändige Klassen')
        self.spec_teacher = QCheckBox('Nur spezifische Lehrkraft')

        self.select_teacher = QComboBox()
        self.select_teacher.addItems(['Lehrkraft auswählen'] + [t.name for t in AllTeachers.teachers])
        self.select_teacher.setDisabled(True)

        self.spec_teacher.toggled.connect(self.select_teacher.setEnabled)

        search_button = QPushButton('OK')
        reset_button = QPushButton('Zurücksetzen')

        search_button.clicked.connect(self._search_classes)
        reset_button.clicked.connect(self._reset)

        sublayout_top.addWidget(level_label)
        sublayout_top.addWidget(self.select_level)
        sublayout_bot.addWidget(reset_button)
        sublayout_bot.addWidget(search_button)

        layout.addLayout(sublayout_top)
        layout.addWidget(self.hours_missing)
        layout.addWidget(self.done_classes)
        layout.addWidget(self.spec_teacher)
        layout.addWidget(self.select_teacher)
        layout.addLayout(sublayout_bot)

        self.TLGB.setLayout(layout)



    def createBLGB(self):
        """
        places GroupBox to bottom-left
        """

        self.BLGB = QGroupBox('Reststunden Lehrer')


    def createTRGB(self):
        """
        places GroupBox to top-left
        """

        self.TRGB = QGroupBox('Klassen')
        gb_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self._list_tabs()
        layout_tab_bot = QHBoxLayout()
        cancel_button = QPushButton('Änderungen verwerfen')
        ok_button = QPushButton('Änderungen übernehmen')
        cancel_button.setStyleSheet("background-color: red")
        ok_button.setStyleSheet("background-color: green")
        layout_tab_bot.addWidget(cancel_button)
        layout_tab_bot.addWidget(ok_button)
        gb_layout.addWidget(self.tabs)
        gb_layout.addLayout(layout_tab_bot)
        self.TRGB.setLayout(gb_layout)


    def createBRGB(self):
        """
        places GroupBox to bottom-right
        """

        self.BRGB = QGroupBox('Lehrer')

        layout = QVBoxLayout()
        top = QHBoxLayout()
        self.searchbar = QComboBox()
        self.searchbar.addItems(['Lehrkraft auswählen'] + [t.name for t in AllTeachers.teachers])
        top.addWidget(self.searchbar)

        self.selected = self._selected_teacher()

        layout.addLayout(top)
        layout.addLayout(self.selected)
        self.searchbar.activated.connect(self._changed_search)
        self.BRGB.setLayout(layout)
        # ----------------end Layout----------------


    def _add_tab(self, obj):
        tab = QWidget()
        layout_tab = QVBoxLayout()
        for i in obj.subjects:
            item = self._class_info_item(i, obj.subjects[i], obj)
            layout_tab.addLayout(item)
        tab.setLayout(layout_tab)
        return tab


    def _selected_teacher(self):
        selected = QHBoxLayout()
        self.info = QLabel('')
        selected.addWidget(self.info) #TODO: add proper widgets
        return selected


    def _changed_search(self):
        name = self.searchbar.currentText()
        text = ''
        for t in AllTeachers.teachers:
            if t.name == name:
                text = str(t)
        if name == 'Lehrkraft auswählen':
            self.info.setText('Keine Lehrkraft ausgewählt')
        else:
            self.info.setText(text)


    def _list_available_teachers(self, subject):
        return ['Lehrkraft wählen'] + [f'{t.name} ({t.short}) - {t._get_hours_left()} Stunden übrig'
                                       for t in AllTeachers.teachers
                                       if subject in t.subjects]


    def _get_class_levels(self):
        liste = []
        for c in AllClasses.classes:
            if c.level not in liste:
                liste.append(c.level)
        return liste


    def _reset(self):
        self.hours_missing.setChecked(False)
        self.done_classes.setChecked(False)
        self.spec_teacher.setChecked(False)
        self.select_level.setCurrentText('Alle')
        self.select_teacher.setCurrentText('Lehrkraft auswählen')
        self._search_classes()


    def _search_classes(self):
        levels = self.select_level.currentText()
        hours_missing = self.hours_missing.checkState()
        done_classes = self.done_classes.checkState()
        teacher = None
        classes = []
        current_text = self.select_teacher.currentText()
        if self.spec_teacher.checkState() and current_text != 'Lehrkraft auswählen':
            for t in AllTeachers.teachers:
                if t.name == current_text:
                    teacher = t
                    break
        for c in AllClasses.classes:
            if str(c.level) == levels or levels == 'Alle':
                classes.append(c)
        if hours_missing:
            for c in classes.copy():
                if not c.hours_missing(): #wenn keine stunden fehlen -> entferne Klasse
                    classes.remove(c)
        if done_classes:
            for c in classes.copy():
                if c.hours_missing(): #wenn Stunden fehlen -> entferne Klasse
                    classes.remove(c)
        if teacher:
            for c in classes.copy():
                if teacher.short not in c.list_teachers():
                    classes.remove(c)
        self._list_tabs(classes)


    def _list_tabs(self, classes=AllClasses.classes):
        last_tab = self.tabs.currentIndex()
        for i in list(range(self.tabs.count()))[::-1]:
            self.tabs.removeTab(i)
        for obj in classes:
            name = obj.get_fullname()
            self.tabs.addTab(self._add_tab(obj), name)
        self.tabs.setCurrentIndex(last_tab)


    def _class_info_item(self, short: str, info: list, obj):
        layout = QHBoxLayout()
        name = SUBJECT_SHORT_DICT[short]
        hours = str(info[0])
        teacher = info[1]
        name_label = QLabel(name)
        hours_label = QLabel(hours)
        teacher_selection = QComboBox()
        available_teachers = self._list_available_teachers(short)
        teacher_selection.addItems(available_teachers)
        if obj.subjects[short][1] == teacher:
            for i in available_teachers:
                if teacher in i:
                    teacher_selection.setCurrentText(i)
        teacher_selection.activated.connect(lambda: self.teacher_added(obj, teacher_selection.currentText(), short))
        layout.addWidget(name_label)
        layout.addWidget(hours_label)
        layout.addWidget(teacher_selection)
        return layout


    def teacher_added(self, klasse, text, short):
        teacher = None
        for t in AllTeachers.teachers:
            if t.short in text:
                teacher = t
                break
        AllClasses.backup = AllClasses.classes.copy()
        for c in AllClasses.classes:
            if c == klasse:
                for s in c.subjects:
                    if s != short:
                        continue
                    if text == 'Lehrkraft auswählen':
                        c.subjects[s][1] = 'null'
                    else:
                        c.subjects[s][1] = teacher.short
        self._changed_search()
        self._search_classes()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
    sys.exit(app.exec_())