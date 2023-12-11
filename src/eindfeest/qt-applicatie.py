import sys
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from eindfeest.diode_experiment2 import DiodeExperiment,list_devices
import csv
import numpy as np

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        """ sets up graphical user interface creating boxes for start, end and repeat values, restart and save option, list of devices
        """
        super().__init__()

        # make widget in pop up diagram
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # create vertical box
        vbox = QtWidgets.QVBoxLayout(central_widget)

        # make plotwidget, add to vbox
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)

        # create horizontal box, add to vbox
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        # make spinboxes for start, end and numpoint values, set default values
        self.start = QtWidgets.QDoubleSpinBox()
        self.start.setValue(0)
        self.end = QtWidgets.QDoubleSpinBox()
        self.end.setRange(0,10)
        self.end.setValue(6.091935483870968)
        self.repeats = QtWidgets.QSpinBox()
        self.repeats.setValue(2)
        self.new = QtWidgets.QPushButton("Start")
        self.save_file = QtWidgets.QPushButton("Save")

        # make combobox and add all devices
        self.arduino = QtWidgets.QComboBox()
        lists = list_devices()
        for device in lists:
            self.arduino.addItems([device])

        # add values to hbox
        hbox.addWidget(self.start)
        hbox.addWidget(self.end)
        hbox.addWidget(self.repeats)
        hbox.addWidget(self.new)
        hbox.addWidget(self.save_file)
        hbox.addWidget(self.arduino)

        # give values to plot function
        self.new.clicked.connect(self.plot)
        self.save_file.clicked.connect(self.save_data)

        self.list_V = []
        self.list_I = []
        self.list_error_V = []
        self.list_error_I = []

    @Slot()
    # make function to plot V and I with errors
    def plot(self):
        """calls on DiodeExperiment class, plots UI-graph
        """
        # clear graph when values are changed by user
        self.plot_widget.clear()

        # call on values made in class UserInterface, make floats
        start = self.start.value()
        end = self.end.value()
        repeats = self.repeats.value()

        # get lists from DiodeExperiment
        measurements = DiodeExperiment(self.arduino.currentText())
        self.list_V, self.list_I, self.list_error_V, self.list_error_I = measurements.scan(start, end, repeats)
        
        # plot average and errorbars
        self.plot_widget.plot(self.list_V, self.list_I, symbol="o", symbolSize=5, pen=None)
        self.plot_widget.setLabel("left", "I (Ampere)")
        self.plot_widget.setLabel("bottom", "V (volt)")
        error_bars = pg.ErrorBarItem(x=np.array(self.list_V), y=np.array(self.list_I), width=2 * np.array(self.list_error_V), height=2 * np.array(self.list_error_I))
        self.plot_widget.addItem(error_bars)

    # make function to save data in csv with chosen name
    def save_data(self):
        """saves data in csv-file on computer
        """
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['V (Volt)','I (Ampere)', 'V_err (Volt)', 'I_err (Ampere)'])
            for V, I, err_V, err_I in zip(self.list_V, self.list_I, self.list_error_V, self.list_error_I):
                writer.writerow([V, I, err_V, err_I])

# call on functions made in UserInterface to plot and show graph
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 