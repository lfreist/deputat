import os
import sys
import settings

sys.path.insert(1, settings.base_dir())

from deputat import AllTeachers, SUBJECT_LONG_DICT

from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel,
                             QLineEdit, QVBoxLayout, QMessageBox, QCheckBox, QSlider)

from PyQt5.QtCore import Qt


class AddTeacherPopUp(QDialog):
    icon_path = settings.icon_dir()
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, name, parent=None):
        super().__init__(parent)
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
        self.hours_edit = QLineEdit()
        self.hours_edit.textChanged.connect(self.update_hours)
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
        AllTeachers().add_teacher(self.name.text(), self.short.text(), int(self.hours.value()), subs)
        self.accept()



class QuitPopUp(QMessageBox):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText("Ohne speichern verlassen?")
        self.setWindowTitle("Exit")
        self.setDetailedText("Es scheint, als wäre etwas verändert worden."
                             "Wird nicht gespeichert, gehen alle Änderungen verloren!\n"
                             "Diese Warnung kann jedoch auch fälschlicherweise angezeigt werden,"
                             "wenn Sie Änderungen manuell rückgängig gemacht werden...")
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
