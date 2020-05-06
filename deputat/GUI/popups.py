from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel,
                             QLineEdit, QVBoxLayout, QMessageBox, QCheckBox, QSlider,
                             QSpinBox)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

from deputat import settings
from deputat.script.deputat import AllTeachers, AllClasses, Class, SUBJECT_LONG_DICT


class AddTeacherPopUp(QDialog):
    icon_path = settings.icon_dir()
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.mainwidget = parent
        self.create_form_GB()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle(name)

    def create_form_GB(self):
        self.formGroupBox = QGroupBox("Informationen")
        self.layout = QFormLayout()
        self.name, self.short = QLineEdit(), QLineEdit()
        self.subjects = [QCheckBox(s) for s in SUBJECT_LONG_DICT]
        self.layout.addRow(QLabel("Name:"), self.name)
        self.layout.addRow(QLabel("Kürzel:"), self.short)
        self.layout.addRow(QLabel("Fächer:"), self.subjects[0])
        for s in self.subjects[1:]:
            self.layout.addRow(QLabel(''), s)
        self.hours = QSlider(Qt.Horizontal)
        self.hours.setMinimum(1)
        self.hours.setMaximum(28)
        self.hours.setValue(22)
        self.hours.setTickPosition(QSlider.TicksAbove)
        self.hours.setTickInterval(1)
        self.hours.valueChanged.connect(self.update_label)
        self.hours_edit = QLineEdit('22')
        self.hours_edit.textChanged.connect(self.update_hours)
        self.layout.addRow(QLabel('Anzahl Stunden:'), QLabel(''))
        self.layout.addRow(self.hours_edit, self.hours)
        self.formGroupBox.setLayout(self.layout)


    def update_label(self):
        self.hours_edit.setText(str(self.hours.value()))


    def update_hours(self):
        try:
            self.hours.setValue(int(self.hours_edit.text()))
        except (TypeError, ValueError):
            pass

    def add(self):
        subs = []
        index = []
        for i, o in enumerate(self.subjects):
            if o.isChecked():
                index.append(i)
        for i, o in enumerate(SUBJECT_LONG_DICT):
            if i in index:
                subs.append(SUBJECT_LONG_DICT[o])
        if not subs or not self.name.text() or not self.short.text() or not self.hours.value():
            return
        self.mainwidget.mainwindow.allteachers.add_teacher(None, self.name.text(), self.short.text(), int(self.hours.value()), subs)
        self.mainwidget._refresh()
        self.mainwidget.mainwindow.statusBar().showMessage(f'Lehrer {self.name.text()} hinzugefügt')
        self.mainwidget.mainwindow.changed = True
        self.accept()


class AddClassPopUp(QDialog):
    icon_path = settings.icon_dir()
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.mainwidget = parent
        
        self.valid = False
        
        self.create_form_GB()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle(name)

    def create_form_GB(self):
        self.formGroupBox = QGroupBox("Informationen")
        self.layout = QFormLayout()
        self.level, self.name = QLineEdit(), QLineEdit()
        self.level.setValidator(QIntValidator(1, 10))
        self.level.textChanged.connect(self.is_valid)
        self.name.textChanged.connect(self.is_valid)
        self.layout.addRow(QLabel("Jahrgangsstufe:"), self.level)
        self.layout.addRow(QLabel("Klassenname (a, b, etc.)"), self.name)
        self.layout.addRow(QLabel("Fächer"), QLabel("Stunden"))
        self.subjects = self.get_subjects()
        for l, s in self.subjects:
            self.layout.addRow(l, s)
        self.formGroupBox.setLayout(self.layout)


    def get_subjects(self):
        liste = []
        for s in SUBJECT_LONG_DICT:
            label = QLabel(f'    {s}')
            spin = QSpinBox()
            spin.setValue(0)
            spin.setMaximum(6)
            spin.setMinimum(0)
            liste.append((label, spin))
        return liste


    def is_valid(self):
        if not self.level.text() or not self.name.text():
            pass
        for c in self.mainwidget.mainwindow.allclasses.classes:
            if f'{c.level}{c.name}' == f'{self.level.text()}{self.name.text()}':
                self.level.setStyleSheet('Background: red')
                self.valid = False
                return
        self.level.setStyleSheet('Background: white')
        self.valid = True


    def add(self):
        subs = {}
        for i, o in enumerate(self.subjects):
            hours = int(o[1].text())
            name = o[0].text().strip()
            if hours:
                subs[SUBJECT_LONG_DICT[name]] = [hours, 'null']
        if not subs or not self.name.text() or not self.level.text() or not self.valid:
            return
        self.mainwidget.mainwindow.allclasses.add_class(None, int(self.level.text()), self.name.text(), subs)
        self.mainwidget._refresh()
        self.mainwidget.mainwindow.statusBar().showMessage(f'Klasse {self.level.text()}{self.name.text()} hinzugefügt')
        self.mainwidget.mainwindow.changed = True
        self.accept()



class QuitPopUp(QMessageBox):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText("Ohne speichern verlassen?")
        self.setWindowTitle("Exit")
        self.setDetailedText("Diese Warnung kann fälschlicherweise angezeigt werden,"\
                             "wenn Änderungen manuell rückgängig gemacht wurden...")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)

        self._close = None

        returnValue = self.exec()
        if returnValue == QMessageBox.Yes:
            self._close = True
        if returnValue == QMessageBox.No:
            self._close = False


    def get(self):
        return self._close