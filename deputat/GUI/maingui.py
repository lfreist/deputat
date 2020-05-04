import os

try:
    from deputat import settings
    from deputat.script.deputat import AllTeachers, AllClasses, SUBJECT_SHORT_DICT, add_class
    from deputat.GUI.popups import AddTeacherPopUp, AddClassPopUp, QuitPopUp
except ImportError:
    import settings
    from script.deputat import AllTeachers, AllClasses, SUBJECT_SHORT_DICT
    from GUI.popups import AddTeacherPopUp, AddClassPopUp, QuitPopUp

from PyQt5.QtWidgets import (QMainWindow, QApplication, QGroupBox, QHBoxLayout,
                             QLabel, QPushButton, QVBoxLayout, QWidget, QTabWidget,
                             QComboBox, QCheckBox, QListWidget, QAction, QFileDialog,
                             QFileSystemModel, QTreeView)

from PyQt5.QtGui import QIcon


CHANGED = False


class MainWindow(QMainWindow):
    icon_path = settings.icon_dir()
    location = ''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.allclasses = AllClasses()
        self.allteachers = AllTeachers()

        title = 'Deputat - Übersicht'
        icon = os.path.join(self.icon_path, 'deputat.svg')
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon))
        self.setGeometry(200, 200, 1250, 500)

        self._build_menu()
        self.statusBar().showMessage('test')

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)


    def _build_menu(self):
        menu_bar = self.menuBar()
        file = menu_bar.addMenu("Datei")

        save = QAction(QIcon(os.path.join(self.icon_path, 'save.svg')), "Speichern", self)
        file.addAction(save)
        save.triggered.connect(self._save)

        load = file.addMenu(QIcon(os.path.join(self.icon_path, 'add.svg')), "Lade Daten")
        import_full = QAction(QIcon(os.path.join(self.icon_path, 'import.svg')), 'Vollständiges Set', self)
        import_teacher = QAction(QIcon(os.path.join(self.icon_path, 'add_teacher.svg')), 'Lehrer', self)
        import_class = QAction(QIcon(os.path.join(self.icon_path, 'add_class.svg')), 'Klassen', self)

        import_full.triggered.connect(self._import_full)
        import_teacher.triggered.connect(self._import_teacher)
        import_class.triggered.connect(self._import_class)

        load.addAction(import_full)
        load.addAction(import_teacher)
        load.addAction(import_class)

        export = file.addMenu(QIcon(os.path.join(self.icon_path, 'export.svg')), 'Exportieren')
        export.addAction(QAction(QIcon(os.path.join(self.icon_path, 'csv.svg')), 'als .csv', self))
        file.addSeparator()

        file.addAction(QAction(QIcon(os.path.join(self.icon_path, 'exit.svg')), "Quit", self))

        info = menu_bar.addMenu("Info")
        info.addAction(QAction(QIcon(os.path.join(self.icon_path, 'about.svg')), "Über", self))
        info.addAction(QAction(QIcon(os.path.join(self.icon_path, 'github.svg')), "GitHub", self))
        info.addAction(QAction(QIcon(os.path.join(self.icon_path, 'pypi.svg')), "PyPi", self))

        help = menu_bar.addMenu("Hilfe")
        help.addAction(QAction(QIcon(os.path.join(self.icon_path, 'mail.svg')), "Mail", self))
        help.addAction(QAction(QIcon(os.path.join(self.icon_path, 'github.svg')), "GitHub", self))
        help.addAction(QAction(QIcon(os.path.join(self.icon_path, 'readme.svg')), "Readme", self))


    def closeEvent(self, event):
        if CHANGED:
            close = QuitPopUp('exit').get()
            if close:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


    def _import_full(self):
        path = QFileDialog.getExistingDirectory(self, 'Odner wählen')
        if not self.location:
            self.location = path
        self.allclasses.read_data(path)
        self.allteachers.read_data(path)
        self.main_widget._refresh(self.main_widget)
        print(self.allclasses.classes)
        print(self.allteachers.teachers)


    def _import_teacher(self):
        path = QFileDialog.getOpenFileName(self, 'Odner wählen')[0]
        if not self.location:
            self.location = path
        self.allteachers.read_data(path, True, additional=True)
        self.main_widget._refresh(self.main_widget)
        self.statusBar().showMessage(f'{os.path.split(path)[1]} importiert')


    def _import_class(self):
        path = QFileDialog.getOpenFileName(self, 'Odner wählen')[0]
        if not self.location:
            self.location = path
        self.allclasses.read_data(path, True, additional=True)
        self.main_widget._refresh(self.main_widget)
        self.statusBar().showMessage(f'{os.path.split(path)[1]} importiert')


    def _save(self):
        a = self.allclasses.save_data()
        b = self.allteachers.save_data()
        global CHANGED
        CHANGED = False
        if a and b:
            self.statusBar().showMessage('erfolgreich gespeichert')
        else:
            self.statusBar().showMessage('speichern nicht erfolgreich!')


class MainWidget(QWidget):
    icon_path = settings.icon_dir()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainwindow = parent

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
        self.fill_combo_level()

        self.hours_missing = QCheckBox('Nur Klassen mit fehlenden Stunden')
        self.done_classes = QCheckBox('Nur volltändige Klassen')
        self.spec_teacher = QCheckBox('Nur spezifische Lehrkraft')

        self.select_teacher = QComboBox()
        self.fill_combo_teacher()
        self.select_teacher.setDisabled(True)

        self.spec_teacher.toggled.connect(self.select_teacher.setEnabled)

        reset_button = QPushButton('Zurücksetzen')

        self.select_level.currentTextChanged.connect(self._search_classes)
        self.hours_missing.stateChanged.connect(self._search_classes)
        self.done_classes.stateChanged.connect(self._search_classes)
        self.spec_teacher.stateChanged.connect(self._search_classes)
        self.select_teacher.currentTextChanged.connect(self._search_classes)
        reset_button.clicked.connect(self._reset)

        sublayout_top.addWidget(level_label)
        sublayout_top.addWidget(self.select_level)
        sublayout_bot.addWidget(reset_button)
        #sublayout_bot.addWidget(search_button)

        layout.addLayout(sublayout_top)
        layout.addWidget(self.hours_missing)
        layout.addWidget(self.done_classes)
        layout.addWidget(self.spec_teacher)
        layout.addWidget(self.select_teacher)
        layout.addLayout(sublayout_bot)

        self.TLGB.setLayout(layout)

    def fill_combo_teacher(self):
        self.select_teacher.clear()
        self.select_teacher.addItems(['Lehrkraft auswählen'] + [t.name for t in self.mainwindow.allteachers.teachers])


    def fill_combo_level(self):
        self.select_level.clear()
        self.select_level.addItems(['Alle'] + self.mainwindow.allclasses.list_levels())


    def createBLGB(self):
        """
        places GroupBox to bottom-left
        """

        self.BLGB = QGroupBox('Reststunden Lehrer')
        self.blgb_layout = QHBoxLayout()
        self.list_area = QListWidget()
        self._build_teacher_list()
        self.blgb_layout.addWidget(self.list_area)
        self.BLGB.setLayout(self.blgb_layout)


    def createTRGB(self):
        """
        places GroupBox to top-left
        """

        self.TRGB = QGroupBox('Deputat')
        gb_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self._list_tabs(self.mainwindow.allclasses.classes)
        layout_tab_bot = QHBoxLayout()

        add_teacher_button = QPushButton('Lehrer Hinzufügen')
        add_teacher_button.setIcon(QIcon(os.path.join(self.icon_path, 'add.svg')))
        add_class_button = QPushButton('Klasse Hinzufügen')
        add_class_button.setIcon(QIcon(os.path.join(self.icon_path, 'add.svg')))

        add_teacher_button.clicked.connect(self._add_teacher)
        add_class_button.clicked.connect(self._add_class)

        layout_tab_bot.addWidget(add_teacher_button)
        layout_tab_bot.addWidget(add_class_button)
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
        self.fill_combo_teacher()
        top.addWidget(self.searchbar)

        self.selected = self._selected_teacher()

        layout.addLayout(top)
        layout.addLayout(self.selected)
        self.searchbar.currentTextChanged.connect(self._changed_search)
        self.BRGB.setLayout(layout)
        # ----------------end Layout----------------


    def fill_combo_teacher_search(self):
        self.searchbar.clear()
        self.searchbar.addItems(['Lehrkraft auswählen'] + [t.name for t in self.mainwindow.allteachers.teachers])


    def _build_teacher_list(self):
        self.list_area.clear()
        self.list_area.addItems(self.mainwindow.allteachers._list_teacher_hours())


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


    def _changed_search(self, t_name=None):
        name = self.searchbar.currentText()
        text = ''
        for t in self.mainwindow.allteachers.teachers:
            if t.name == name:
                text = str(t)
        if name == 'Lehrkraft auswählen':
            self.info.setText('Keine Lehrkraft ausgewählt')
        else:
            self.info.setText(text)
        if t_name:
            for t in self.mainwindow.allteachers.teachers:
                if t.name == t_name:
                    self.searchbar.setCurrentText(t_name)
                    break


    def _list_available_teachers(self, subject):
        return ['Lehrkraft wählen'] + [f'{t.name} ({t.short}) - {t._get_hours_left()} Stunden übrig'
                                       for t in self.mainwindow.allteachers.teachers
                                       if subject in t.subjects]


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
            for t in self.mainwindow.allteachers.teachers:
                if t.name == current_text:
                    teacher = t
                    break
        for c in self.mainwindow.allclasses.classes:
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


    def _list_tabs(self, classes):
        last_tab = self.tabs.currentIndex()
        for i in list(range(self.tabs.count()))[::-1]:
            self.tabs.removeTab(i)
        liste = sorted([obj for obj in classes])
        for obj in liste:
            self.tabs.addTab(self._add_tab(obj), obj.get_fullname())
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
        name = None
        for t in self.mainwindow.allteachers.teachers:
            if t.short in text:
                teacher = t
                break
        if not self.mainwindow.allclasses.backup:
            self.mainwindow.allclasses.backup = self.mainwindow.allclasses.classes.copy()
        for c in self.mainwindow.allclasses.classes:
            if c == klasse:
                for s in c.subjects:
                    if s != short:
                        continue
                    try:
                        c.subjects[s][1] = teacher.short
                        name = teacher.name
                    except AttributeError:
                        c.subjects[s][1] = 'null'
        self._refresh(name)
        global CHANGED
        CHANGED = True

    def _add_class(self):
        add_c = AddClassPopUp('Klasse Hinzufügen', self)
        add_c.setGeometry(100, 200, 500, 300)
        add_c.show()


    def _add_teacher(self):
        add_t = AddTeacherPopUp('Lehrer Hinzufügen', self)
        add_t.setGeometry(100, 200, 500, 300)
        add_t.show()


    def _refresh(self, name=None):
        self._changed_search(name)
        self._search_classes()
        self._build_teacher_list()
        self.fill_combo_teacher()
        self.fill_combo_level()
        self.fill_combo_teacher_search()


def run():
    import sys
    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
    sys.exit(app.exec_())
