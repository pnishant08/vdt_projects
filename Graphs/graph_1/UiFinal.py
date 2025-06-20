import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QSizePolicy
)

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from graph_plotter import (
    plot_erf_with_dropdown,
    plot_psafe_with_dropdown,
    plot_depth_with_dropdown,
    plot_orientation_with_dropdown
)


class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.setWindowTitle("Pipeline Defect Graph Viewer")
        self.setGeometry(200, 100, 1100, 800)
        self.layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        self.load_btn = QPushButton("Load Excel File")
        self.load_btn.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_btn)

        self.graph_type = QComboBox()
        self.graph_type.addItems(["", "ERF", "Psafe", "Depth", "Orientation"])
        self.graph_type.setVisible(False)
        self.layout.addWidget(QLabel("Select Graph Type:"))
        self.layout.addWidget(self.graph_type)

        self.view_type = QComboBox()
        self.view_type.addItems(["", "Internal", "External", "Both"])
        self.view_type.setVisible(False)
        self.layout.addWidget(QLabel("Select Surface View:"))
        self.layout.addWidget(self.view_type)

        self.plot_btn = QPushButton("Plot Graph")
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.setVisible(False)
        self.layout.addWidget(self.plot_btn)

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {path.split('/')[-1]}")
            self.graph_type.setVisible(True)
            self.view_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def plot_graph(self):
        try:
            graph_type = self.graph_type.currentText()
            view = self.view_type.currentText()
            if not graph_type or not view:
                self.file_label.setText("Please select graph type and view.")
                return

            if graph_type == "ERF":
                path = plot_erf_with_dropdown(self.df.copy(), view)
            # elif graph_type == "Psafe":
            #     path = plot_psafe(self.df.copy(), view)
            # elif graph_type == "Depth":
            #     path = plot_depth(self.df.copy(), view)
            # elif graph_type == "Orientation":
            #     path = plot_orientation(self.df.copy(), view)
            # else:
            #     self.file_label.setText("Invalid graph type.")
                return

            from PyQt5.QtCore import QUrl  # Add this import at the top of the file

            # Then use this to load the file
            self.browser.load(QUrl.fromLocalFile(path))

        except Exception as e:
            self.file_label.setText(f"Plot failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GraphApp()
    viewer.show()
    sys.exit(app.exec_())