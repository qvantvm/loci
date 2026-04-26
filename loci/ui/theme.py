"""Centralized visual styling for Loci."""

from __future__ import annotations


DARK_STYLE = """
QMainWindow, QDialog {
    background: #0F1117;
}
QWidget {
    background: transparent;
    color: #D7DAE0;
    font-family: Inter, "SF Pro Display", "Segoe UI", sans-serif;
    font-size: 13px;
}
QToolBar#topBar {
    background: #0F1117;
    border: 0;
    border-bottom: 1px solid #242832;
    padding: 6px 10px;
    spacing: 8px;
}
QToolButton {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    color: #B8BEC9;
    padding: 6px 10px;
}
QToolButton:hover {
    background: #1A1D25;
    border-color: #2A2F3A;
    color: #F2F4F8;
}
QLineEdit, QTextEdit, QPlainTextEdit {
    background: #151821;
    border: 1px solid #2A2F3A;
    border-radius: 10px;
    color: #E6E8EC;
    padding: 9px 10px;
    selection-background-color: #3657D8;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #4D7DFF;
}
QPushButton {
    background: #1A1D25;
    border: 1px solid #2A2F3A;
    border-radius: 9px;
    color: #D7DAE0;
    padding: 8px 12px;
}
QPushButton:hover {
    background: #222733;
    border-color: #3B4352;
    color: #FFFFFF;
}
QPushButton:pressed {
    background: #171A22;
}
QTreeWidget, QListWidget, QTextBrowser {
    background: #12151D;
    border: 1px solid #242832;
    border-radius: 12px;
    outline: 0;
}
QTreeWidget::item {
    border-radius: 8px;
    color: #BFC5D2;
    margin: 2px 6px;
    padding: 8px;
}
QTreeWidget::item:hover {
    background: #1B202B;
    color: #F2F4F8;
}
QTreeWidget::item:selected {
    background: #26314A;
    color: #FFFFFF;
}
QScrollArea {
    background: transparent;
    border: 0;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
QSplitter::handle {
    background: #181B23;
    margin: 12px 0;
}
QSplitter::handle:hover {
    background: #2A3140;
}
QLabel#PaneTitle {
    font-size: 17px;
    font-weight: 700;
    color: #F5F7FA;
}
QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 650;
    color: #F5F7FA;
}
QLabel#cardTitle {
    color: #F2F4F8;
    font-weight: 650;
}
QLabel#metadataLabel {
    color: #8F98A8;
    font-weight: 650;
}
QLabel#muted {
    color: #8F98A8;
}
QLabel#Badge {
    background: #1D2B45;
    border: 1px solid #304668;
    color: #9FC0FF;
    border-radius: 8px;
    padding: 3px 8px;
}
QLabel#Badge[kind="ai"] {
    background: #251E3F;
    border-color: #45306F;
    color: #C9B6FF;
}
QFrame#card {
    background: #151821;
    border: 1px solid #242832;
    border-radius: 14px;
}
QFrame#card:hover {
    border-color: #303747;
}
QCheckBox {
    color: #BFC5D2;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #3B4352;
    border-radius: 4px;
    background: #151821;
}
QCheckBox::indicator:checked {
    background: #4D7DFF;
    border-color: #4D7DFF;
}
"""


LIGHT_STYLE = """
QMainWindow, QDialog {
    background: #F5F6FA;
}
QWidget {
    background: transparent;
    color: #20242C;
    font-family: Inter, "SF Pro Display", "Segoe UI", sans-serif;
    font-size: 13px;
}
QToolBar#topBar {
    background: #F5F6FA;
    border: 0;
    border-bottom: 1px solid #DDE2EC;
    padding: 6px 10px;
    spacing: 8px;
}
QToolButton, QPushButton {
    background: #FFFFFF;
    border: 1px solid #D7DEEA;
    border-radius: 9px;
    color: #273041;
    padding: 8px 12px;
}
QToolButton:hover, QPushButton:hover {
    background: #EEF3FF;
    border-color: #B8C8F8;
}
QLineEdit, QTextEdit, QPlainTextEdit {
    background: #FFFFFF;
    border: 1px solid #D7DEEA;
    border-radius: 10px;
    color: #20242C;
    padding: 9px 10px;
    selection-background-color: #4D7DFF;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #4D7DFF;
}
QTreeWidget, QListWidget, QTextBrowser {
    background: #FFFFFF;
    border: 1px solid #DDE2EC;
    border-radius: 12px;
    outline: 0;
}
QTreeWidget::item {
    border-radius: 8px;
    color: #404A5C;
    margin: 2px 6px;
    padding: 8px;
}
QTreeWidget::item:hover {
    background: #F1F5FF;
}
QTreeWidget::item:selected {
    background: #E3EBFF;
    color: #18233A;
}
QScrollArea {
    background: transparent;
    border: 0;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
QSplitter::handle {
    background: #E5E9F1;
    margin: 12px 0;
}
QLabel#PaneTitle {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
}
QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 650;
    color: #111827;
}
QLabel#cardTitle {
    color: #111827;
    font-weight: 650;
}
QLabel#metadataLabel, QLabel#muted {
    color: #697386;
}
QLabel#Badge {
    background: #EAF1FF;
    border: 1px solid #C8D9FF;
    color: #254DA0;
    border-radius: 8px;
    padding: 3px 8px;
}
QLabel#Badge[kind="ai"] {
    background: #F0EAFE;
    border-color: #D8C9FB;
    color: #5B35A6;
}
QFrame#card {
    background: #FFFFFF;
    border: 1px solid #DDE2EC;
    border-radius: 14px;
}
"""


def stylesheet(dark: bool = True) -> str:
    return DARK_STYLE if dark else LIGHT_STYLE


def apply_theme(widget, dark: bool = True) -> None:
    """Apply the selected Loci stylesheet to a widget tree."""

    widget.setStyleSheet(stylesheet(dark))
