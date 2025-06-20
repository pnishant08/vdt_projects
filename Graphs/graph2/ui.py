
# import sys
# import pandas as pd
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QSizePolicy
# )
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import Qt, QUrl

# from erf2 import plot_erf
# from psafe1 import plot_psafe
# from depth_percent import plot_depth
# from orientation import plot_orientation
# from pitting_graph import plot_pitting
# from general import plot_general
# from corr import plot_corrosion


# class GraphApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.df = None
#         self.setWindowTitle("Pipeline Defect Graph Viewer")
#         self.setGeometry(200, 100, 1100, 800)
#         self.layout = QVBoxLayout()

#         self.file_label = QLabel("No file selected")
#         self.layout.addWidget(self.file_label)

#         self.load_btn = QPushButton("Load Excel File")
#         self.load_btn.clicked.connect(self.load_file)
#         self.layout.addWidget(self.load_btn)

#         self.graph_type = QComboBox()
#         self.graph_type.addItems(["", "ERF", "Psafe", "Depth", "Orientation", "Pitting","GENERAL","Corrison"])
#         self.graph_type.setVisible(False)
#         self.graph_type.currentIndexChanged.connect(self.toggle_view_type)
#         self.layout.addWidget(QLabel("Select Graph Type:"))
#         self.layout.addWidget(self.graph_type)

#         self.view_type = QComboBox()
#         self.view_type.addItems(["", "Internal", "External", "Both"])
#         self.view_type.setVisible(False)
#         self.layout.addWidget(QLabel("Select Surface View:"))
#         self.layout.addWidget(self.view_type)

#         self.plot_btn = QPushButton("Plot Graph")
#         self.plot_btn.clicked.connect(self.plot_graph)
#         self.plot_btn.setVisible(False)
#         self.layout.addWidget(self.plot_btn)

#         self.browser = QWebEngineView()
#         self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.layout.addWidget(self.browser)

#         self.setLayout(self.layout)

#     def load_file(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
#         if path:
#             print("Selected Path:", path)
#             self.df = pd.read_excel(path)
#             self.df.columns = self.df.columns.str.strip()
#             self.file_label.setText(f"Loaded: {path.split('/')[-1]}")
#             self.graph_type.setVisible(True)
#             self.view_type.setVisible(True)
#             self.plot_btn.setVisible(True)

#     def toggle_view_type(self):
#         selected_graph = self.graph_type.currentText()
#         if selected_graph in ["Pitting", "GENERAL", "Corrison"]:
#             self.view_type.setVisible(False)
#         else:
#             self.view_type.setVisible(True)

#     def plot_graph(self):
#         try:
#            graph_type = self.graph_type.currentText()
#            view = self.view_type.currentText()
#            if not graph_type:
#               self.file_label.setText("Please select graph type.")
#               return

#            if graph_type == "Pitting":
#                path = plot_pitting(self.df.copy())
#            elif graph_type == "GENERAL":
#                path = plot_general(self.df.copy())
#            elif graph_type == "Corrison":
#                path = plot_corrosion(self.df.copy())
#            else:
#                if not view:
#                    self.file_label.setText("Please select surface view.")
#                    return
   
#                if graph_type == "ERF":
#                    path = plot_erf(self.df.copy(), view)
#                elif graph_type == "Psafe":
#                    path = plot_psafe(self.df.copy(), view)
#                elif graph_type == "Depth":
#                    path = plot_depth(self.df.copy(), view)
#                elif graph_type == "Orientation":
#                    path = plot_orientation(self.df.copy(), view)
#                else:
#                    self.file_label.setText("Invalid graph type.")
#                    return

#            from PyQt5.QtCore import QUrl
#            self.browser.load(QUrl.fromLocalFile(path))

#         except Exception as e:
#            self.file_label.setText(f"Plot failed: {str(e)}")



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     viewer = GraphApp()
#     viewer.show()
#     sys.exit(app.exec_())





import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl

from erf2 import plot_erf
from psafe1 import plot_psafe
from depth_percent import plot_depth
from orientation import plot_orientation
from pitting_graph import plot_pitting
from general import plot_general
from corr import plot_corrosion


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

        # Main category dropdown
        self.category_type = QComboBox()
        self.category_type.addItems(["", "Main Graphs", "Defects"])
        self.category_type.setVisible(False)
        self.category_type.currentIndexChanged.connect(self.toggle_graph_options)
        self.layout.addWidget(QLabel("Select Category:"))
        self.layout.addWidget(self.category_type)

        # Main graph type dropdown
        self.graph_type = QComboBox()
        self.graph_type.addItems(["", "ERF", "Psafe", "Depth", "Orientation"])
        self.graph_type.setVisible(False)
        self.layout.addWidget(QLabel("Select Graph Type:"))
        self.layout.addWidget(self.graph_type)

        # Defect type dropdown
        self.defect_type = QComboBox()
        self.defect_type.addItems(["", "Pitting", "General", "Corrosion"])
        self.defect_type.setVisible(False)
        self.layout.addWidget(QLabel("Select Defect Type:"))
        self.layout.addWidget(self.defect_type)

        # Surface view dropdown
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
            print("Selected Path:", path)
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {path.split('/')[-1]}")
            self.category_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def toggle_graph_options(self):
        selected_category = self.category_type.currentText()

        if selected_category == "Main Graphs":
            self.graph_type.setVisible(True)
            self.view_type.setVisible(True)
            self.defect_type.setVisible(False)

        elif selected_category == "Defects":
            self.graph_type.setVisible(False)
            self.view_type.setVisible(False)
            self.defect_type.setVisible(True)

        else:
            self.graph_type.setVisible(False)
            self.view_type.setVisible(False)
            self.defect_type.setVisible(False)

    def plot_graph(self):
        try:
            category = self.category_type.currentText()

            if not category:
                self.file_label.setText("Please select a category.")
                return

            # Defects (Pitting, General, Corrosion)
            if category == "Defects":
                defect_graph = self.defect_type.currentText()
                if not defect_graph:
                    self.file_label.setText("Please select a defect type.")
                    return

                if defect_graph == "Pitting":
                    path = plot_pitting(self.df.copy())
                elif defect_graph == "General":
                    path = plot_general(self.df.copy())
                elif defect_graph == "Corrosion":
                    path = plot_corrosion(self.df.copy())
                else:
                    self.file_label.setText("Invalid defect type selected.")
                    return

            # Main Graphs (ERF, Psafe, Depth, Orientation)
            else:
                graph_type = self.graph_type.currentText()
                view = self.view_type.currentText()

                if not graph_type or not view:
                    self.file_label.setText("Please select graph type and surface view.")
                    return

                if graph_type == "ERF":
                    path = plot_erf(self.df.copy(), view)
                elif graph_type == "Psafe":
                    path = plot_psafe(self.df.copy(), view)
                elif graph_type == "Depth":
                    path = plot_depth(self.df.copy(), view)
                elif graph_type == "Orientation":
                    path = plot_orientation(self.df.copy(), view)
                else:
                    self.file_label.setText("Invalid graph type selected.")
                    return

            self.browser.load(QUrl.fromLocalFile(path))

        except Exception as e:
            self.file_label.setText(f"Plot failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GraphApp()
    viewer.show()
    sys.exit(app.exec_())
