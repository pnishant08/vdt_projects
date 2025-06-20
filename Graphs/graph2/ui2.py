# import sys
# import os
# import pandas as pd
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QSizePolicy, QMessageBox
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
# from PyQt5.QtWidgets import QHBoxLayout



# class GraphApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.df = None
#         self.current_fig = None  # To store the active figure
#         self.setWindowTitle("Pipeline Defect Graph Viewer")
#         self.setGeometry(200, 100, 1100, 800)
#         self.layout = QVBoxLayout()

#         self.file_label = QLabel("No file selected")
#         self.layout.addWidget(self.file_label)

#         self.load_btn = QPushButton("Load Excel File")
#         self.load_btn.clicked.connect(self.load_file)
#         self.layout.addWidget(self.load_btn)

#         self.graph_type = QComboBox()
#         self.graph_type.addItems(["", "ERF", "Psafe", "Depth", "Orientation", "Pitting", "GENERAL", "Corrison"])
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

#         # Download button with custom styling

#         # Download Button with sky blue color and center alignment
#         self.download_btn = QPushButton("⬇ Download Graph as PNG")
#         self.download_btn.clicked.connect(self.download_graph)
#         self.download_btn.setVisible(False)
#         self.download_btn.setFixedWidth(self.width() // 4)  # One fourth of the window width
        
#         self.download_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: skyblue;
#                 color: white;
#                 font-size: 16px;
#                 padding: 10px 20px;
#                 border-radius: 8px;
#                 border: 1px solid #3399FF;
#             }
#             QPushButton:hover {
#                 background-color: #66CCFF;
#             }
#         """)
        
#         # Center align using a horizontal layout
#         button_layout = QHBoxLayout()
#         button_layout.addStretch()
#         button_layout.addWidget(self.download_btn)
#         button_layout.addStretch()
        
#         self.layout.addLayout(button_layout)


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
#             self.file_label.setText(f"Loaded: {os.path.basename(path)}")
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
#             graph_type = self.graph_type.currentText()
#             view = self.view_type.currentText()

#             if not graph_type:
#                 self.file_label.setText("Please select graph type.")
#                 return

#             if graph_type == "Pitting":
#                 fig, path = plot_pitting(self.df.copy())
#             elif graph_type == "GENERAL":
#                 fig, path = plot_general(self.df.copy())
#             elif graph_type == "Corrison":
#                 fig, path = plot_corrosion(self.df.copy())
#             else:
#                 if not view:
#                     self.file_label.setText("Please select surface view.")
#                     return

#                 if graph_type == "ERF":
#                     fig, path = plot_erf(self.df.copy(), view)
#                 elif graph_type == "Psafe":
#                     fig, path = plot_psafe(self.df.copy(), view)
#                 elif graph_type == "Depth":
#                     fig, path = plot_depth(self.df.copy(), view)
#                 elif graph_type == "Orientation":
#                     fig, path = plot_orientation(self.df.copy(), view)
#                 else:
#                     self.file_label.setText("Invalid graph type.")
#                     return

#             self.current_fig = fig
#             self.browser.load(QUrl.fromLocalFile(path))
#             self.download_btn.setVisible(True)

#         except Exception as e:
#             self.file_label.setText(f"Plot failed: {str(e)}")

#     def download_graph(self):
#         if self.current_fig:
#             save_path, _ = QFileDialog.getSaveFileName(self, "Save Graph as PNG", "", "PNG Files (*.png)")
#             if save_path:
#                 try:
#                     self.current_fig.write_image(save_path)
#                     os.startfile(save_path)  # Automatically open the saved file
#                     self.file_label.setText("Graph saved successfully as PNG.")

#                     # Show confirmation popup
#                     msg = QMessageBox()
#                     msg.setIcon(QMessageBox.Information)
#                     msg.setWindowTitle("Download Successful")
#                     msg.setText("Graph has been saved successfully and opened!")
#                     msg.setStandardButtons(QMessageBox.Ok)
#                     msg.exec_()

#                 except Exception as e:
#                     self.file_label.setText(f"Save failed: {str(e)}")
#         else:
#             self.file_label.setText("No graph available to download.")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     viewer = GraphApp()
#     viewer.show()
#     sys.exit(app.exec_())/




import sys
import os
import pandas as pd
import plotly.io as pio

# Ensure PNG saving using kaleido
pio.kaleido.scope.default_format = "png"

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QSizePolicy
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

        # Graph Type Dropdown
        self.graph_type = QComboBox()
        self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation"])
        self.graph_type.setVisible(False)
        self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
        self.layout.addWidget(QLabel("Select Graph Type:"))
        self.layout.addWidget(self.graph_type)

        # Defect Category Dropdown
        self.defect_category = QComboBox()
        self.defect_category.addItems(["", "Corrosion", "General", "Pitting"])
        self.defect_category.setVisible(False)
        self.layout.addWidget(QLabel("Select Defect Category:"))
        self.layout.addWidget(self.defect_category)

        # Surface View Dropdown
        self.view_type = QComboBox()
        self.view_type.addItems(["", "Internal", "External", "Both"])
        self.view_type.setVisible(False)
        self.layout.addWidget(QLabel("Select Surface View:"))
        self.layout.addWidget(self.view_type)

        # Plot Button
        self.plot_btn = QPushButton("Plot Graph")
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.setVisible(False)
        self.layout.addWidget(self.plot_btn)

        # Save Button
        self.save_btn = QPushButton("Save Graph as PNG")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px 15px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.save_btn.setFixedWidth(200)
        self.save_btn.setVisible(False)
        self.save_btn.clicked.connect(self.save_graph)
        self.layout.addWidget(self.save_btn)

        # Browser for displaying graphs
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

    def on_graph_type_changed(self, text):
        if text == "Defects":
            # Enable defect category dropdown and disable Surface View dropdown
            self.defect_category.setVisible(True)
            self.view_type.setVisible(False)
        elif text in ["ERF", "Psafe", "Depth", "Orientation"]:
            # Enable Surface View dropdown and disable Defect Category dropdown
            self.defect_category.setVisible(False)
            self.view_type.setVisible(True)
        else:
            # If no valid graph type is selected, hide both dropdowns
            self.defect_category.setVisible(False)
            self.view_type.setVisible(False)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {os.path.basename(path)}")
            self.graph_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def plot_graph(self):
        try:
            graph_type = self.graph_type.currentText()
            defect_type = self.defect_category.currentText()
            view = self.view_type.currentText()

            if graph_type:
                if graph_type == "Defects":
                    if not defect_type:
                        self.file_label.setText("Please select defect category.")
                        return

                    if defect_type == "Pitting":
                        fig, path = plot_pitting(self.df.copy(), return_fig=True)
                    elif defect_type == "General":
                        fig, path = plot_general(self.df.copy(), return_fig=True)
                    elif defect_type == "Corrosion":
                        fig, path = plot_corrosion(self.df.copy(), return_fig=True)
                    else:
                        self.file_label.setText("Invalid defect category.")
                        return

                    self.current_fig = fig
                    self.browser.load(QUrl.fromLocalFile(path))
                    self.save_btn.setVisible(True)

                else:  # For ERF, Psafe, Depth, Orientation
                    if not view:
                        self.file_label.setText("Please select surface view.")
                        return

                    if graph_type == "ERF":
                        fig, path = plot_erf(self.df.copy(), view, return_fig=True)
                    elif graph_type == "Psafe":
                        fig, path = plot_psafe(self.df.copy(), view, return_fig=True)
                    elif graph_type == "Depth":
                        fig, path = plot_depth(self.df.copy(), view, return_fig=True)
                    elif graph_type == "Orientation":
                        fig, path = plot_orientation(self.df.copy(), view, return_fig=True)
                    else:
                        self.file_label.setText("Invalid graph type.")
                        return

                    self.current_fig = fig
                    self.browser.load(QUrl.fromLocalFile(path))
                    self.save_btn.setVisible(True)

            else:
                self.file_label.setText("Please select a graph type.")

        except Exception as e:
            self.file_label.setText(f"Plot failed: {str(e)}")
            self.current_fig = None

    def save_graph(self):
        if hasattr(self, 'current_fig') and self.current_fig is not None:
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            default_file = os.path.join(downloads_folder, "graph.png")

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Plot as PNG",
                default_file,
                "PNG Files (*.png);;All Files (*)"
            )

            if file_path:
                try:
                    if not file_path.lower().endswith(".png"):
                        file_path += ".png"

                    self.current_fig.write_image(file_path)
                    self.file_label.setText(f"Graph saved as: {file_path}")
                except Exception as e:
                    self.file_label.setText(f"Failed to save graph: {str(e)}")
            else:
                self.file_label.setText("No file path selected.")
        else:
            self.file_label.setText("No graph to save.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GraphApp()
    viewer.show()
    sys.exit(app.exec_())
