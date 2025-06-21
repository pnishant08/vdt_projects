import sys
import os
import pandas as pd
import plotly.io as pio

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl

# from erf2 import plot_erf
# from psafe1 import plot_psafe
# from depth_percent import plot_depth
# from orientation import plot_orientation
# from metal_loss_graph import plot_metal_loss  # You need to have this function

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.current_fig = None
        self.setWindowTitle("Pipeline Defect Graph Viewer")
        self.setGeometry(200, 100, 1100, 800)
        self.layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label, alignment=Qt.AlignLeft)

        self.load_btn = QPushButton("Load Excel File")
        self.load_btn.clicked.connect(self.load_file)
        self.load_btn.setStyleSheet("background-color: skyblue; padding: 8px; width: 200px;")
        self.layout.addWidget(self.load_btn, alignment=Qt.AlignLeft)

        # Graph Type Dropdown
        self.graph_type = QComboBox()
        self.graph_type.addItems(["", "ERF", "Psafe", "Depth", "Orientation", "Metal Loss"])
        self.graph_type.setVisible(False)
        self.graph_type.currentTextChanged.connect(self.update_graph_options)
        self.graph_label = QLabel("Select Graph Type:")
        self.graph_label.setVisible(False)
        self.layout.addWidget(self.graph_label)
        self.layout.addWidget(self.graph_type)

        # Surface View Dropdown
        self.surface_view = QComboBox()
        self.surface_view.addItems(["", "Internal", "External", "Both"])
        self.surface_view.setVisible(False)
        self.surface_label = QLabel("Select Surface View:")
        self.surface_label.setVisible(False)
        self.layout.addWidget(self.surface_label)
        self.layout.addWidget(self.surface_view)

        # Feature Identification Dropdown
        self.feature_type = QComboBox()
        self.feature_type.addItems(["", "Both", "Corrosion", "MFG"])
        self.feature_type.setVisible(False)
        self.feature_label = QLabel("Select Feature Identification:")
        self.feature_label.setVisible(False)
        self.feature_type.currentTextChanged.connect(self.update_feature_options)
        self.layout.addWidget(self.feature_label)
        self.layout.addWidget(self.feature_type)

        # Dimension Classification Dropdown
        self.dimension_class = QComboBox()
        self.dimension_class.addItems([
            "", "All", "Axial Grooving", "Axial Slotting",
            "Circumferential Slotting", "Circumferential Grooving",
            "Pitting", "Pinhole", "General"
        ])
        self.dimension_class.setVisible(False)
        self.dimension_label = QLabel("Select Dimension Classification:")
        self.dimension_label.setVisible(False)
        self.layout.addWidget(self.dimension_label)
        self.layout.addWidget(self.dimension_class)

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
        self.layout.addWidget(self.save_btn, alignment=Qt.AlignCenter)

        # Browser for displaying graphs
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {os.path.basename(path)}")

            # Show graph type dropdown after loading file
            self.graph_label.setVisible(True)
            self.graph_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def update_graph_options(self, text):
        if text == "Metal Loss":
            # Show Feature Type, Hide Surface View
            self.surface_view.setVisible(False)
            self.surface_label.setVisible(False)

            self.feature_label.setVisible(True)
            self.feature_type.setVisible(True)

            self.dimension_class.setVisible(False)
            self.dimension_label.setVisible(False)

        elif text in ["ERF", "Psafe", "Depth", "Orientation"]:
            # Show Surface View, Hide Feature Type and Dimension
            self.surface_view.setVisible(True)
            self.surface_label.setVisible(True)

            self.feature_label.setVisible(False)
            self.feature_type.setVisible(False)

            self.dimension_class.setVisible(False)
            self.dimension_label.setVisible(False)

        else:
            # Hide all if no valid selection
            self.surface_view.setVisible(False)
            self.surface_label.setVisible(False)
            self.feature_label.setVisible(False)
            self.feature_type.setVisible(False)
            self.dimension_class.setVisible(False)
            self.dimension_label.setVisible(False)

    def update_feature_options(self, text):
        if text == "Both":
            self.dimension_class.setVisible(False)
            self.dimension_label.setVisible(False)
        elif text in ["Corrosion", "MFG"]:
            self.dimension_class.setVisible(True)
            self.dimension_label.setVisible(True)
        else:
            self.dimension_class.setVisible(False)
            self.dimension_label.setVisible(False)

    def plot_graph(self):
        try:
            graph_type = self.graph_type.currentText()

            if not graph_type:
                self.file_label.setText("Please select graph type.")
                return

            if graph_type == "Metal Loss":
                feature = self.feature_type.currentText()
                dimension = self.dimension_class.currentText()

                if not feature:
                    self.file_label.setText("Please select feature identification.")
                    return

                if feature != "Both" and not dimension:
                    self.file_label.setText("Please select dimension classification.")
                    return

                # fig, path = plot_metal_loss(self.df.copy(), feature, dimension, return_fig=True)

            else:
                view = self.surface_view.currentText()
                if not view:
                    self.file_label.setText("Please select surface view.")
                    return

            #     if graph_type == "ERF":
            #         fig, path = plot_erf(self.df.copy(), view, return_fig=True)
            #     elif graph_type == "Psafe":
            #         fig, path = plot_psafe(self.df.copy(), view, return_fig=True)
            #     elif graph_type == "Depth":
            #         fig, path = plot_depth(self.df.copy(), view, return_fig=True)
            #     elif graph_type == "Orientation":
            #         fig, path = plot_orientation(self.df.copy(), view, return_fig=True)
            #     else:
            #         self.file_label.setText("Invalid graph type.")
            #         return

            # self.current_fig = fig
            # self.browser.load(QUrl.fromLocalFile(path))
            # self.save_btn.setVisible(True)

        except Exception as e:
            self.file_label.setText(f"Plot failed: {str(e)}")

    def save_graph(self):
        if self.current_fig is not None:
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
