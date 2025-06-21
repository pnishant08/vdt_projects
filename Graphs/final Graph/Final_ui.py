#this is final by deepak sir

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
from metal_loss_plot import plot_metal_loss


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

        self.graph_type_label = QLabel("Select Graph Type:")
        self.graph_type_label.setVisible(False)
        self.layout.addWidget(self.graph_type_label)

        self.graph_type = QComboBox()
        self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation"])
        self.graph_type.setVisible(False)
        self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
        self.layout.addWidget(self.graph_type)

        self.feature_identification_label = QLabel("Select Feature Identification:")
        self.feature_identification_label.setVisible(False)
        self.layout.addWidget(self.feature_identification_label)

        self.feature_identification = QComboBox()
        self.feature_identification.addItems(["", "Corrosion", "MFG"])
        self.feature_identification.setVisible(False)
        self.layout.addWidget(self.feature_identification)

        self.dimension_classification_label = QLabel("Select Dimensional Classification:")
        self.dimension_classification_label.setVisible(False)
        self.layout.addWidget(self.dimension_classification_label)

        self.dimension_classification = QComboBox()
        self.dimension_classification.addItems([
            "", "Pitting", "Axial Grooving", "Axial Slotting",
            "Circumferential Grooving", "Circumferential Slotting", "Pinhole", "General"
        ])
        self.dimension_classification.setVisible(False)
        self.layout.addWidget(self.dimension_classification)

        self.view_type_label = QLabel("Select Surface View:")
        self.view_type_label.setVisible(False)
        self.layout.addWidget(self.view_type_label)

        self.view_type = QComboBox()
        self.view_type.addItems(["", "Internal", "External", "Both"])
        self.view_type.setVisible(False)
        self.layout.addWidget(self.view_type)

        self.plot_btn = QPushButton("Plot Graph")
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.setVisible(False)
        self.layout.addWidget(self.plot_btn)

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

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

    def on_graph_type_changed(self, text):
        if text == "Defects":
            self.feature_identification_label.setVisible(True)
            self.feature_identification.setVisible(True)
            self.dimension_classification_label.setVisible(True)
            self.dimension_classification.setVisible(True)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        elif text in ["ERF", "Psafe", "Depth", "Orientation"]:
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(True)
            self.view_type.setVisible(True)
        else:
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {os.path.basename(path)}")

            self.graph_type_label.setVisible(True)
            self.graph_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def plot_graph(self):
        try:
            graph_type = self.graph_type.currentText()
            view = self.view_type.currentText()
            feature = self.feature_identification.currentText()
            dimension = self.dimension_classification.currentText()

            print(f"[DEBUG] Graph Type: {graph_type}, Feature: {feature}, Dimension: {dimension}, View: {view}")
            if graph_type == "Defects":
                feature_id = feature if feature else None
                dimension_class = dimension if dimension != "ALL" else None

                fig, path = plot_metal_loss(self.df.copy(), feature_type=feature_id, dimension_class=dimension_class, return_fig=True)

                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            elif graph_type in ["ERF", "Psafe", "Depth", "Orientation"]:
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
