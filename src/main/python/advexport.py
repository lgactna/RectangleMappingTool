# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kisun\Desktop\RectangleMappingTool\src\main\resources\base\advexport.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdvExportWindow(object):
    def setupUi(self, AdvExportWindow):
        AdvExportWindow.setObjectName("AdvExportWindow")
        AdvExportWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(AdvExportWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.selected_field_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selected_field_label.sizePolicy().hasHeightForWidth())
        self.selected_field_label.setSizePolicy(sizePolicy)
        self.selected_field_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.selected_field_label.setObjectName("selected_field_label")
        self.verticalLayout_3.addWidget(self.selected_field_label)
        self.selected_info_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_info_label.setMinimumSize(QtCore.QSize(237, 0))
        self.selected_info_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.selected_info_label.setWordWrap(True)
        self.selected_info_label.setObjectName("selected_info_label")
        self.verticalLayout_3.addWidget(self.selected_info_label)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.sample_output_label = QtWidgets.QLabel(self.centralwidget)
        self.sample_output_label.setObjectName("sample_output_label")
        self.gridLayout.addWidget(self.sample_output_label, 2, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.available_fields_list = QtWidgets.QListWidget(self.centralwidget)
        self.available_fields_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.available_fields_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.available_fields_list.setObjectName("available_fields_list")
        self.gridLayout.addWidget(self.available_fields_list, 1, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sample_output_table = QtWidgets.QTableWidget(self.tab)
        self.sample_output_table.setObjectName("sample_output_table")
        self.sample_output_table.setColumnCount(0)
        self.sample_output_table.setRowCount(0)
        self.verticalLayout.addWidget(self.sample_output_table)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sample_output_raw = QtWidgets.QPlainTextEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.sample_output_raw.setFont(font)
        self.sample_output_raw.setPlainText("")
        self.sample_output_raw.setObjectName("sample_output_raw")
        self.verticalLayout_2.addWidget(self.sample_output_raw)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 3, 0, 1, 3)
        self.advanced_export_button = QtWidgets.QPushButton(self.centralwidget)
        self.advanced_export_button.setObjectName("advanced_export_button")
        self.gridLayout.addWidget(self.advanced_export_button, 4, 0, 1, 3)
        self.selected_fields_list = QtWidgets.QListWidget(self.centralwidget)
        self.selected_fields_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.selected_fields_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.selected_fields_list.setObjectName("selected_fields_list")
        self.gridLayout.addWidget(self.selected_fields_list, 1, 0, 1, 1)
        AdvExportWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdvExportWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        AdvExportWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdvExportWindow)
        self.statusbar.setObjectName("statusbar")
        AdvExportWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AdvExportWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AdvExportWindow)

    def retranslateUi(self, AdvExportWindow):
        _translate = QtCore.QCoreApplication.translate
        AdvExportWindow.setWindowTitle(_translate("AdvExportWindow", "MainWindow"))
        self.selected_field_label.setText(_translate("AdvExportWindow", "-----"))
        self.selected_info_label.setText(_translate("AdvExportWindow", "<html><head/><body><p>Click on an item for more information.</p><p>Note that you can copy fields by dragging fields with left-click held down. (But then you can\'t delete them, so you\'ll have to move them out of the &quot;selected fields&quot; column or reopen this window.)</p></body></html>"))
        self.label_4.setText(_translate("AdvExportWindow", "Field information"))
        self.sample_output_label.setText(_translate("AdvExportWindow", "Sample output (up to 5 rects):"))
        self.label_2.setText(_translate("AdvExportWindow", "Available fields/columns"))
        self.label.setText(_translate("AdvExportWindow", "Selected fields/columns"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AdvExportWindow", "Table"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AdvExportWindow", "Raw"))
        self.advanced_export_button.setText(_translate("AdvExportWindow", "Export to .csv"))
