import sys, os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPlainTextEdit, QLabel, QTreeView, 
                              QFileSystemModel, QToolBar, QStatusBar, QFileDialog,
                              QMessageBox, QDockWidget, QMenu, QComboBox, QSpinBox, 
                              QDialog, QDialogButtonBox, QFormLayout, QTabWidget,
                              QSplitter, QCompleter, QInputDialog, QLineEdit,
                              QFontDialog, QColorDialog, QPushButton, QCheckBox,
                              QListWidget, QTreeWidget, QTreeWidgetItem, QToolTip,
                              QSplashScreen, QGraphicsOpacityEffect, QScrollArea,
                              QGridLayout, QTextEdit, QFrame, QProgressDialog,
                              QListWidgetItem, QGroupBox, QStackedWidget, QTabBar)  # Added QTabBar here
from PySide6.QtCore import (Qt, QRect, QDir, QSize, QProcess, QRegularExpression,
                           QStringListModel, QTimer, QPropertyAnimation, QUrl,  # Added QPropertyAnimation here
                           QEasingCurve, QThread, QObject, Signal)  # Added QThread and QObject here
from PySide6.QtGui import (QColor, QPalette, QTextCharFormat, QSyntaxHighlighter,
                          QFont, QPainter, QBrush, QAction, QIcon, QKeySequence, 
                          QTextCursor, QShortcut, QTextDocument, QPixmap, QPen,
                          QLinearGradient, QTextFormat, QCursor, QFontMetricsF)  # Added QFontMetricsF here
import qdarkstyle
import subprocess
import json
import platform
import keyword
import builtins
import re
import time
from pathlib import Path

# Add these color constants at the top of the file
EDITOR_COLORS = {
    'background': '#1E1E1E',
    'text': '#F8F8F2',
    'keywords': '#FF79C6',
    'strings': '#F1FA8C',
    'comments': '#6272A4',
    'functions': '#50FA7B',
    'numbers': '#BD93F9',
    'operators': '#FF79C6',
    'class_names': '#8BE9FD',
    'decorators': '#FFB86C',
    'constants': '#BD93F9',
    'selection_bg': '#44475A',
    'current_line': '#283593',
    'matching_brackets': '#F8F8F2',
    'line_numbers': '#6272A4',
    'line_numbers_active': '#F8F8F2'
}

# Add these classes right after imports, before any other class definitions
class NewFileDialog(QDialog):
    def __init__(self, directory, parent=None):
        super().__init__(parent)
        self.directory = directory
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("New File")
        layout = QVBoxLayout(self)

        # Current directory label
        dir_label = QLabel(f"Current Directory: {self.directory}")
        dir_label.setStyleSheet("color: #6272A4;")
        layout.addWidget(dir_label)

        # File type combo box
        layout.addWidget(QLabel("File Type:"))
        self.file_type = QComboBox()
        self.file_types = {
            "Python File": ".py",
            "C++ File": ".cpp",
            "C File": ".c",
            "Header File": ".h",
            "HPP File": ".hpp",
            "Java File": ".java",
            "JavaScript File": ".js",
            "HTML File": ".html",
            "CSS File": ".css",
            "Text File": ".txt",
            "Custom": ""
        }
        self.file_type.addItems(self.file_types.keys())
        layout.addWidget(self.file_type)

        # File name input
        layout.addWidget(QLabel("File Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter file name or path/filename")
        layout.addWidget(self.name_input)

        # Custom extension for custom file type
        self.custom_ext_label = QLabel("Custom Extension:")
        self.custom_ext_input = QLineEdit()
        self.custom_ext_input.setPlaceholderText(".ext")
        layout.addWidget(self.custom_ext_label)
        layout.addWidget(self.custom_ext_input)
        
        # Hide custom extension by default
        self.custom_ext_label.hide()
        self.custom_ext_input.hide()

        # Example label
        example = QLabel("Example: utils/helper.py or myfile.cpp")
        example.setStyleSheet("color: #6272A4; font-style: italic;")
        layout.addWidget(example)

        # Connect signals
        self.file_type.currentTextChanged.connect(self.on_file_type_changed)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def on_file_type_changed(self, file_type):
        # Show/hide custom extension input
        is_custom = file_type == "Custom"
        self.custom_ext_label.setVisible(is_custom)
        self.custom_ext_input.setVisible(is_custom)
        
        if not is_custom:
            self.update_extension()

    def update_extension(self):
        name = self.name_input.text()
        if not name:
            return
            
        # Split into path and filename
        parts = os.path.splitext(name)
        base_name = parts[0]
        
        # Add selected extension
        ext = self.file_types[self.file_type.currentText()]
        self.name_input.setText(f"{base_name}{ext}")

    def validate_and_accept(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Error", "File name cannot be empty")
            return
            
        # Check for invalid characters
        invalid_chars = '<>:"|?*'
        if any(c in name for c in invalid_chars):
            QMessageBox.warning(self, "Error", f"File name cannot contain any of these characters: {invalid_chars}")
            return
            
        self.accept()

    def get_file_info(self):
        """Get the complete file name with extension"""
        try:
            # Get base name
            base_name = str(self.name_input.text()).strip()
            if not base_name:
                return None
            
            # Get file type
            file_type = str(self.file_type.currentText())
            
            # Handle file extension
            if file_type == "Custom":
                # For custom type, use custom extension
                ext = str(self.custom_ext_input.text()).strip()
                if ext and not ext.startswith('.'):
                    ext = '.' + ext
            else:
                # For predefined types, use the extension from file_types
                ext = str(self.file_types.get(file_type, ''))
                
            # Combine name and extension
            if ext and not base_name.endswith(ext):
                full_name = base_name + ext
            else:
                full_name = base_name
                
            return full_name
            
        except Exception as e:
            print(f"Error in get_file_info: {str(e)}")  # Debug print
            return None

class NewFolderDialog(QDialog):
    def __init__(self, directory, parent=None):
        super().__init__(parent)
        self.directory = directory
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("New Folder")
        layout = QVBoxLayout(self)

        # Folder name input
        layout.addWidget(QLabel("Folder Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter folder name")
        layout.addWidget(self.name_input)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def validate_and_accept(self):
        """Validate folder name before accepting"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Folder name cannot be empty")
            return
            
        if not any(c.isalnum() for c in name):
            QMessageBox.warning(self, "Error", "Folder name must contain at least one alphanumeric character")
            return
            
        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(c in name for c in invalid_chars):
            QMessageBox.warning(self, "Error", f"Folder name cannot contain any of these characters: {invalid_chars}")
            return
            
        self.accept()

    def get_folder_info(self):
        """Get the folder name"""
        return self.name_input.text().strip()

# Move FileSystemHelper class here, before any other class definitions
class FileSystemHelper:
    def __init__(self, parent=None):
        self.parent = parent

    def create_file(self, directory):
        """Create a new file in the specified directory"""
        name, ok = QInputDialog.getText(
            self.parent,
            "New File",
            "Enter file name:",
            QLineEdit.Normal,
            "untitled.txt"
        )
        
        if ok and name:
            try:
                file_path = Path(directory) / name
                if not file_path.exists():
                    file_path.touch()
                    return str(file_path)
                else:
                    QMessageBox.warning(
                        self.parent,
                        "File Exists",
                        f"File '{name}' already exists in this location."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Could not create file: {str(e)}"
                )
        return None

    def create_folder(self, directory):
        """Create a new folder in the specified directory"""
        name, ok = QInputDialog.getText(
            self.parent,
            "New Folder",
            "Enter folder name:",
            QLineEdit.Normal,
            "New Folder"
        )
        
        if ok and name:
            try:
                folder_path = Path(directory) / name
                if not folder_path.exists():
                    folder_path.mkdir()
                    return str(folder_path)
                else:
                    QMessageBox.warning(
                        self.parent,
                        "Folder Exists",
                        f"Folder '{name}' already exists in this location."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Could not create folder: {str(e)}"
                )
        return None

# Add language-specific syntax highlighters
class BaseHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            matches = expression.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class PythonHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Python-specific formats
        self.init_formats()
        
        # Add Python-specific rules
        self.add_python_rules()
        
        # Add common rules (strings, numbers, etc.)
        self.add_common_rules()

    def init_formats(self):
        # Keywords
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(EDITOR_COLORS['keywords']))
        self.keyword_format.setFontWeight(QFont.Bold)
        
        # Built-ins
        self.builtin_format = QTextCharFormat()
        self.builtin_format.setForeground(QColor("#66D9EF"))
        
        # Decorators
        self.decorator_format = QTextCharFormat()
        self.decorator_format.setForeground(QColor(EDITOR_COLORS['decorators']))

    def add_python_rules(self):
        import builtins as py_builtins  # Import builtins properly
        
        # Python keywords
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((pattern, self.keyword_format))
            
        # Python built-ins
        builtin_funcs = dir(py_builtins)  # Use the imported builtins
        for word in builtin_funcs:
            if not word.startswith('_'):  # Skip private builtins
                pattern = f"\\b{word}\\b"
                self.highlighting_rules.append((pattern, self.builtin_format))
            
        # Decorators
        self.highlighting_rules.append((r"@\w+", self.decorator_format))

    def add_common_rules(self):
        # String formats
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(EDITOR_COLORS['strings']))
        
        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(EDITOR_COLORS['comments']))
        comment_format.setFontItalic(True)
        
        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(EDITOR_COLORS['numbers']))
        
        # Add common rules
        self.highlighting_rules.extend([
            # Strings
            (r'"[^"\\]*(\\.[^"\\]*)*"', string_format),
            (r"'[^'\\]*(\\.[^'\\]*)*'", string_format),
            # Comments
            (r'#[^\n]*', comment_format),
            # Numbers
            (r'\b\d+\b', number_format),
        ])

class CppHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # C++-specific formats
        self.init_formats()
        
        # Add C++-specific rules
        self.add_cpp_rules()
        
        # Add common rules
        self.add_common_rules()

    def init_formats(self):
        # Keywords
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(EDITOR_COLORS['keywords']))
        self.keyword_format.setFontWeight(QFont.Bold)
        
        # Types
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor("#66D9EF"))
        
        # Preprocessor
        self.preprocessor_format = QTextCharFormat()
        self.preprocessor_format.setForeground(QColor("#F92672"))

    def add_cpp_rules(self):
        # C++ keywords
        keywords = [
            "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand",
            "bitor", "bool", "break", "case", "catch", "char", "char8_t",
            "char16_t", "char32_t", "class", "compl", "concept", "const",
            "consteval", "constexpr", "constinit", "const_cast", "continue",
            "co_await", "co_return", "co_yield", "decltype", "default",
            "delete", "do", "double", "dynamic_cast", "else", "enum",
            "explicit", "export", "extern", "false", "float", "for",
            "friend", "goto", "if", "inline", "int", "long", "mutable",
            "namespace", "new", "noexcept", "not", "not_eq", "nullptr",
            "operator", "or", "or_eq", "private", "protected", "public",
            "register", "reinterpret_cast", "requires", "return", "short",
            "signed", "sizeof", "static", "static_assert", "static_cast",
            "struct", "switch", "template", "this", "thread_local", "throw",
            "true", "try", "typedef", "typeid", "typename", "union",
            "unsigned", "using", "virtual", "void", "volatile", "wchar_t",
            "while", "xor", "xor_eq"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((pattern, self.keyword_format))
            
        # Preprocessor directives
        self.highlighting_rules.append((r"#\w+", self.preprocessor_format))

class JavaHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()
        self.add_java_rules()
        self.add_common_rules()

    def init_formats(self):
        # Keywords
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(EDITOR_COLORS['keywords']))
        self.keyword_format.setFontWeight(QFont.Bold)
        
        # Types
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor("#66D9EF"))
        
        # Annotations
        self.annotation_format = QTextCharFormat()
        self.annotation_format.setForeground(QColor(EDITOR_COLORS['decorators']))

    def add_java_rules(self):
        # Java keywords
        keywords = [
            "abstract", "assert", "boolean", "break", "byte", "case", "catch",
            "char", "class", "const", "continue", "default", "do", "double",
            "else", "enum", "extends", "final", "finally", "float", "for",
            "if", "implements", "import", "instanceof", "int", "interface",
            "long", "native", "new", "package", "private", "protected",
            "public", "return", "short", "static", "strictfp", "super",
            "switch", "synchronized", "this", "throw", "throws", "transient",
            "try", "void", "volatile", "while", "true", "false", "null"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((pattern, self.keyword_format))
            
        # Annotations
        self.highlighting_rules.append((r"@\w+", self.annotation_format))

# Add CodeCompleter class for intelligent code completion
class CodeCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(self.get_completion_model())
        self.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)

    def get_completion_model(self):
        words = set()
        # Add Python keywords
        words.update(keyword.kwlist)
        # Add Python builtins
        words.update(dir(builtins))
        # Add common snippets
        snippets = [
            "def __init__(self):",
            "if __name__ == '__main__':",
            "for i in range()",
            "try:\n    \nexcept Exception as e:",
            "class :",
            "print()",
            "return",
            "import",
            "from",
        ]
        words.update(snippets)
        return QStringListModel(sorted(list(words)))

# Add FindReplaceDialog for search functionality
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Find & Replace")
        layout = QVBoxLayout(self)

        # Find section
        find_layout = QHBoxLayout()
        self.find_input = QLineEdit()
        find_button = QPushButton("Find Next")
        find_button.clicked.connect(self.find_text)
        find_layout.addWidget(QLabel("Find:"))
        find_layout.addWidget(self.find_input)
        find_layout.addWidget(find_button)

        # Replace section
        replace_layout = QHBoxLayout()
        self.replace_input = QLineEdit()
        replace_button = QPushButton("Replace")
        replace_all_button = QPushButton("Replace All")
        replace_button.clicked.connect(self.replace_text)
        replace_all_button.clicked.connect(self.replace_all)
        replace_layout.addWidget(QLabel("Replace:"))
        replace_layout.addWidget(self.replace_input)
        replace_layout.addWidget(replace_button)
        replace_layout.addWidget(replace_all_button)

        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_words = QCheckBox("Whole words")
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)

        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addLayout(options_layout)

    def get_editor(self):
        return self.parent.get_current_editor()

    def find_text(self):
        editor = self.get_editor()
        if not editor:
            return

        text = self.find_input.text()
        if not text:
            return

        flags = QTextDocument.FindFlags()
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindWholeWords

        if not editor.find(text, flags):
            cursor = editor.textCursor()
            cursor.movePosition(QTextCursor.Start)
            editor.setTextCursor(cursor)
            editor.find(text, flags)

    def replace_text(self):
        editor = self.get_editor()
        if not editor:
            return

        if editor.textCursor().hasSelection():
            editor.textCursor().insertText(self.replace_input.text())
        self.find_text()

    def replace_all(self):
        count = 0
        editor = self.get_editor()
        if not editor:
            return

        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        editor.setTextCursor(cursor)
        
        while editor.find(self.find_input.text()):
            cursor = editor.textCursor()
            cursor.insertText(self.replace_input.text())
            count += 1
        
        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences")

# Add this new class for advanced code completion
class AdvancedCodeCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize snippets before using them
        self.init_snippets()
        self.setModel(self.create_completion_model())
        self.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)
        self.setMaxVisibleItems(10)

    def init_snippets(self):
        # Store snippets and their expansions
        self.snippets = {
            # Python snippets
            "def": "def ${1:function_name}(${2:parameters}):\n\t${3:pass}",
            "class": "class ${1:ClassName}:\n\tdef __init__(self):\n\t\t${2:pass}",
            "if": "if ${1:condition}:\n\t${2:pass}",
            "for": "for ${1:item} in ${2:items}:\n\t${3:pass}",
            "while": "while ${1:condition}:\n\t${2:pass}",
            "try": "try:\n\t${1:pass}\nexcept ${2:Exception} as ${3:e}:\n\t${4:pass}",
            "with": "with ${1:expression} as ${2:variable}:\n\t${3:pass}",
            
            # C/C++ snippets
            "main": "int main(int argc, char *argv[]) {\n\t${1:return 0;}\n}",
            "inc": "#include <${1:iostream}>",
            "using": "using namespace ${1:std};",
            "class.h": "class ${1:ClassName} {\npublic:\n\t${2:ClassName}();\nprivate:\n\t${3}\n};",
            "struct": "struct ${1:name} {\n\t${2}\n};",
            "printf": 'printf("${1:%s}\\n"${2:, });',
            "scanf": 'scanf("${1:%d}", &${2:var});',
            "cout": 'std::cout << ${1:"Hello"} << std::endl;',
            "cin": 'std::cin >> ${1:var};',
            
            # Common snippets
            "todo": "# TODO: ${1:description}",
            "fixme": "# FIXME: ${1:description}",
            "debug": "print(f'Debug: ${1:variable} = {${1:variable}}')",
            "header": "/*\n * ${1:Description}\n * Author: ${2:Name}\n * Date: ${3:Date}\n */",
            "guard": "#ifndef ${1:HEADER_H}\n#define ${1:HEADER_H}\n\n${2}\n\n#endif // ${1:HEADER_H}",
        }

    def create_completion_model(self):
        words = set()
        
        # Add Python keywords and builtins
        words.update(keyword.kwlist)
        words.update(dir(builtins))
        
        # Add snippet triggers
        words.update(self.snippets.keys())
        
        # Add common Python modules
        common_modules = ['os', 'sys', 'datetime', 'math', 'random', 'json', 're']
        for module in common_modules:
            try:
                module_obj = __import__(module)
                words.update(dir(module_obj))
            except ImportError:
                pass

        # Add C/C++ keywords
        cpp_keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile',
            'while', 'class', 'namespace', 'template', 'virtual', 'public', 'private',
            'protected', 'friend', 'operator', 'explicit', 'inline', 'throw', 'try',
            'catch', 'delete', 'new', 'this', 'using'
        }
        words.update(cpp_keywords)
        
        return QStringListModel(sorted(list(words)))

    def get_snippet(self, trigger):
        return self.snippets.get(trigger)

# Add LineNumberArea class before GlassmorphicCodeEditor
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet(f"""
            background-color: {EDITOR_COLORS['background']}E6;
            color: {EDITOR_COLORS['line_numbers']};
            font-family: 'JetBrains Mono';
            font-size: 11px;
            padding: 8px 12px;
            border-right: 1px solid {EDITOR_COLORS['comments']}40;
        """)

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

# Then update GlassmorphicCodeEditor to include line number methods
class GlassmorphicCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.setup_drag_drop()
        self.setup_completer()
        self.setup_line_numbers()
        self.setup_syntax_highlighter()

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(EDITOR_COLORS['background']))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(EDITOR_COLORS['line_numbers']))
                painter.drawText(0, int(top), self.line_number_area.width(),
                               self.fontMetrics().height(),
                               Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def setup_line_numbers(self):
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def setup_editor(self):
        # Set up font
        font = QFont("JetBrains Mono", 12)  # Using JetBrains Mono for better coding experience
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        
        # Tab settings
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        
        # Set up colors and styling with enhanced glassmorphic effect
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {EDITOR_COLORS['background']}E6;
                color: {EDITOR_COLORS['text']};
                border: none;
                border-radius: 12px;
                selection-background-color: {EDITOR_COLORS['selection_bg']};
                selection-color: {EDITOR_COLORS['text']};
                padding: 8px;
            }}
            QPlainTextEdit:focus {{
                border: 1px solid {EDITOR_COLORS['keywords']}40;
                background-color: {EDITOR_COLORS['background']}F2;
            }}
            QScrollBar:vertical {{
                background: {EDITOR_COLORS['background']}80;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: {EDITOR_COLORS['comments']}80;
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {EDITOR_COLORS['comments']}B3;
            }}
            QScrollBar:horizontal {{
                background: {EDITOR_COLORS['background']}80;
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal {{
                background: {EDITOR_COLORS['comments']}80;
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {EDITOR_COLORS['comments']}B3;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
        """)

    def setup_drag_drop(self):
        """Setup drag and drop support"""
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasUrls():
            # Handle dropped files
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.insertPlainText(f.read())
                    except Exception as e:
                        QMessageBox.critical(self.parent(), "Error", f"Could not read file: {str(e)}")
        elif event.mimeData().hasText():
            # Handle dropped text
            self.insertPlainText(event.mimeData().text())
        
        event.acceptProposedAction()

    def setup_completer(self):
        self.completer = CodeCompleter(self)
        self.completer.setWidget(self)
        self.completer.activated.connect(self.insert_completion)
        
        # Enhanced word list
        words = set()
        words.update(keyword.kwlist)  # Python keywords
        words.update(dir(builtins))   # Python builtins
        
        # Add common Python modules
        common_modules = ['os', 'sys', 'datetime', 'math', 'random', 'json', 're', 'time']
        for module in common_modules:
            try:
                module_obj = __import__(module)
                words.update(dir(module_obj))
            except ImportError:
                pass
        
        # Add code snippets
        snippets = [
            "def __init__(self):",
            "if __name__ == '__main__':",
            "try:\n    \nexcept Exception as e:",
            "for i in range():",
            "while True:",
            "class ClassName:",
            "def function_name():",
            "import ",
            "from  import ",
            "print()",
            "return ",
            "raise Exception",
            "with open() as f:",
        ]
        words.update(snippets)
        
        self.completer.model().setStringList(sorted(list(words)))

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return
                
        # Auto-indent
        if event.key() == Qt.Key_Return:
            tc = self.textCursor()
            block = tc.block()
            text = block.text()
            indent = re.match(r'^\s*', text).group()
            
            # Check if we need to increase indent
            if text.strip().endswith(':'):
                indent += '    '
                
            super().keyPressEvent(event)
            self.insertPlainText(indent)
            return
            
        # Handle tab
        if event.key() == Qt.Key_Tab:
            tc = self.textCursor()
            if tc.hasSelection():
                self.indent_selection()
            else:
                self.insertPlainText('    ')
            return
            
        # Auto-close brackets and quotes
        pairs = {
            '(': ')', '[': ']', '{': '}',
            '"': '"', "'": "'"
        }
        if event.text() in pairs:
            tc = self.textCursor()
            self.insertPlainText(event.text() + pairs[event.text()])
            tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)
            return
            
        super().keyPressEvent(event)
        
        # Show completer
        if event.text().isalnum() or event.text() == '_':
            completion_prefix = self.text_under_cursor()
            if len(completion_prefix) >= 2:
                self.completer.setCompletionPrefix(completion_prefix)
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
                
                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                          + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cr)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def indent_selection(self):
        tc = self.textCursor()
        start = tc.selectionStart()
        end = tc.selectionEnd()
        
        tc.setPosition(start)
        tc.movePosition(QTextCursor.StartOfBlock)
        tc.setPosition(end, QTextCursor.KeepAnchor)
        tc.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        
        selected_text = tc.selectedText()
        indented_text = '    ' + selected_text.replace('\u2029', '\n    ')
        tc.insertText(indented_text)

    def setup_syntax_highlighter(self):
        highlighter = PythonHighlighter(self.document())

    def setup_auto_indent(self):
        self.indent_chars = {
            "py": "    ",  # 4 spaces for Python
            "cpp": "\t",   # tab for C++
            "c": "\t",     # tab for C
            "java": "    " # 4 spaces for Java
        }

    def setup_auto_pairs(self):
        self.auto_pairs = {
            '"': '"',
            "'": "'",
            "(": ")",
            "[": "]",
            "{": "}"
        }

    def setup_minimap(self):
        self.minimap = QPlainTextEdit(self)
        self.minimap.setReadOnly(True)
        self.minimap.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.minimap.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.minimap.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(40, 42, 54, 0.3);
                color: rgba(248, 248, 242, 0.5);
                border: none;
                font-size: 2px;
            }
        """)
        self.minimap.setFixedWidth(100)
        self.minimap.setVisible(False)  # Hidden by default

    def setup_status_info(self):
        self.status_info = QLabel()
        self.status_info.setStyleSheet("""
            QLabel {
                color: #6272A4;
                padding: 2px 10px;
            }
        """)
        self.main_window.statusBar().addPermanentWidget(self.status_info)
        self.cursorPositionChanged.connect(self.update_status_info)

    def update_status_info(self):
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        selected = cursor.selectedText()
        sel_count = len(selected)
        
        info = f"Line {line}, Column {col}"
        if sel_count > 0:
            info += f" | Selected: {sel_count} chars"
        
        # Add file info
        if hasattr(self, 'current_file'):
            ext = os.path.splitext(self.current_file)[1]
            info += f" | {ext[1:].upper()}"
        
        # Add encoding
        info += " | UTF-8"
        
        self.status_info.setText(info)

    def setup_advanced_tools(self):
        editor = self.get_current_editor()
        if editor:
            self.code_runner = CodeRunner(editor)
            self.advanced_debugger = AdvancedDebugger(editor)
            self.performance_profiler = PerformanceProfiler(editor)
            self.code_refactoring = CodeRefactoring(editor)
            self.smart_completion = SmartCompletion(editor)
            self.code_analyzer = CodeAnalyzer(editor)

    # Add this method to the GlassmorphicCodeEditor class
    def highlightCurrentLine(self):
        """Highlight the current line"""
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            # Set the line color
            lineColor = QColor(EDITOR_COLORS['current_line'])
            lineColor.setAlpha(60)  # Make it semi-transparent
            
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            
            extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)

# Add new TabWidget class
class EditorTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setup_style()

    def add_new_tab(self, file_path=None):
        """Add a new tab with a code editor"""
        editor = GlassmorphicCodeEditor(self)
        editor.setPlainText("")
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    editor.setPlainText(f.read())
                editor.current_file = file_path
                tab_name = os.path.basename(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
                return
        else:
            tab_name = "Untitled"
            editor.current_file = None

        # Set up syntax highlighting
        highlighter = PythonHighlighter(editor.document())
        
        index = self.addTab(editor, tab_name)
        self.setCurrentIndex(index)
        editor.setFocus()
        return editor

    def close_tab(self, index):
        """Close the specified tab"""
        editor = self.widget(index)
        if editor and hasattr(editor, 'document') and editor.document().isModified():
            reply = QMessageBox.question(
                self,
                'Save Changes?',
                'Do you want to save changes before closing?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                if hasattr(editor, 'current_file') and editor.current_file:
                    try:
                        with open(editor.current_file, 'w', encoding='utf-8') as f:
                            f.write(editor.toPlainText())
                        editor.document().setModified(False)
                        self.removeTab(index)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
                else:
                    # Handle unsaved new files
                    file_path, _ = QFileDialog.getSaveFileName(
                        self,
                        "Save File As",
                        "",
                        "All Files (*.*);;"
                        "Python Files (*.py);;"
                        "Text Files (*.txt)"
                    )
                    if file_path:
                        try:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(editor.toPlainText())
                            editor.document().setModified(False)
                            self.removeTab(index)
                        except Exception as e:
                            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
            elif reply == QMessageBox.Discard:
                self.removeTab(index)
        else:
            self.removeTab(index)

        # If no tabs left, show welcome screen
        if self.count() == 0:
            if hasattr(self.main_window, 'show_welcome_screen'):
                self.main_window.show_welcome_screen()
            else:
                # Fallback if welcome screen not available
                self.add_new_tab("Untitled")

    def setup_style(self):
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background: rgba(40, 42, 54, 0.7);
                color: #F8F8F2;
                padding: 8px 16px;
                border: none;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: rgba(68, 71, 90, 0.9);
            }
            QTabBar::tab:hover {
                background: rgba(98, 114, 164, 0.8);
            }
        """)
        
    def add_welcome_page(self):
        welcome = WelcomePage(self)
        self.addTab(welcome, "Welcome")
        self.setTabsClosable(False)  # Don't allow closing the welcome page
        
    def add_new_tab(self, title="Untitled", content=""):
        # If this is the first regular tab, make tabs closable
        if self.count() == 1 and isinstance(self.widget(0), WelcomePage):
            self.setTabsClosable(True)
        
        editor = GlassmorphicCodeEditor(self)
        editor.setPlainText(content)
        index = self.addTab(editor, title)
        self.setCurrentIndex(index)
        return editor

    def close_tab(self, index):
        """Close the specified tab"""
        widget = self.widget(index)  # Use self.widget instead of self.tab_widget
        if widget and hasattr(widget, 'document') and widget.document().isModified():
            reply = QMessageBox.question(
                self,
                'Save Changes?',
                'Do you want to save changes before closing?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                if hasattr(widget, 'current_file'):
                    try:
                        with open(widget.current_file, 'w', encoding='utf-8') as f:
                            f.write(widget.toPlainText())
                        widget.document().setModified(False)
                        self.removeTab(index)  # Use self.removeTab instead of self.tab_widget.removeTab
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
                else:
                    self.main_window.save_file_as()
                    if not widget.document().isModified():
                        self.removeTab(index)
            elif reply == QMessageBox.Discard:
                self.removeTab(index)
        else:
            self.removeTab(index)

        # If no tabs left, show welcome screen
        if self.count() == 0 and hasattr(self.main_window, 'show_welcome_screen'):
            self.main_window.show_welcome_screen()

# Improve Terminal class
class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Add terminal toolbar with more options
        self.setup_toolbar()
        
        # Terminal tabs for multiple instances
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)
        self.layout.addWidget(self.terminal_tabs)
        
        # Add initial terminal
        self.add_new_terminal()
        
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background: rgba(40, 42, 54, 0.7);
                border: none;
                padding: 2px;
            }
        """)
        
        # Add new terminal
        new_terminal = QAction("New Terminal", self)
        new_terminal.triggered.connect(self.add_new_terminal)
        toolbar.addAction(new_terminal)
        
        # Terminal type selector
        terminal_type = QComboBox()
        terminal_type.addItems(["CMD", "PowerShell", "Bash", "Python"])
        terminal_type.currentTextChanged.connect(self.change_terminal_type)
        toolbar.addWidget(terminal_type)
        
        toolbar.addSeparator()
        
        # Additional tools
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear_current_terminal)
        toolbar.addAction(clear_action)
        
        self.layout.addWidget(toolbar)

    def add_new_terminal(self):
        terminal = TerminalInstance()
        self.terminal_tabs.addTab(terminal, f"Terminal {self.terminal_tabs.count() + 1}")
        self.terminal_tabs.setCurrentWidget(terminal)

    def close_terminal_tab(self, index):
        if self.terminal_tabs.count() > 1:
            self.terminal_tabs.removeTab(index)
        
    def clear_current_terminal(self):
        current_terminal = self.terminal_tabs.currentWidget()
        if current_terminal:
            current_terminal.clear_terminal()
            
    def change_terminal_type(self, terminal_type):
        current_terminal = self.terminal_tabs.currentWidget()
        if current_terminal:
            current_terminal.start_shell(terminal_type)

class TerminalInstance(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Terminal output
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: none;
                font-family: 'Consolas';
                padding: 5px;
            }
        """)
        
        # Command input with history
        self.command_input = QLineEdit()
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas';
            }
        """)
        
        self.layout.addWidget(self.output)
        self.layout.addWidget(self.command_input)
        
        # Command history
        self.command_history = []
        self.history_index = 0
        
        # Setup process
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        
        # Connect signals
        self.command_input.returnPressed.connect(self.send_command)
        
        # Start default shell
        self.start_shell("CMD")  # Default to CMD on startup

    def start_shell(self, terminal_type="CMD"):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()
            
        if terminal_type == "CMD":
            self.process.start("cmd.exe")
        elif terminal_type == "PowerShell":
            self.process.start("powershell.exe")
        elif terminal_type == "Bash":
            self.process.start("/bin/bash")
        elif terminal_type == "Python":
            self.process.start("python")

    def handle_output(self):
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode('utf-8', errors='replace')
        self.output.appendPlainText(text.rstrip())
        
    def handle_error(self):
        data = self.process.readAllStandardError()
        text = bytes(data).decode('utf-8', errors='replace')
        self.output.appendPlainText(text.rstrip())

    def send_command(self):
        command = self.command_input.text()
        if command:
            self.output.appendPlainText(f"$ {command}")
            if os.name == 'nt':
                command = f"{command}\r\n"
            else:
                command = f"{command}\n"
            self.process.write(command.encode())
            self.command_input.clear()

    def clear_terminal(self):
        self.output.clear()

# Add BuildRunner class to handle different language builds
class BuildRunner:
    LANGUAGE_CONFIGS = {
        'Python': {
            'file_extensions': ['.py'],
            'run_command': lambda file: ['python', file],
            'build_command': None,
            'env_setup': None
        },
        'C++': {
            'file_extensions': ['.cpp', '.cxx', '.cc'],
            'run_command': lambda file: [
                os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + 
                    ('.exe' if platform.system() == 'Windows' else '')
                )
            ],
            'build_command': lambda file: [
                'g++',
                '-std=c++17',
                '-Wall',
                file,
                '-o',
                os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + 
                    ('.exe' if platform.system() == 'Windows' else '')
                )
            ],
            'env_setup': None
        },
        'C': {
            'file_extensions': ['.c'],
            'run_command': lambda file: [
                os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + 
                    ('.exe' if platform.system() == 'Windows' else '')
                )
            ],
            'build_command': lambda file: [
                'gcc',
                '-Wall',
                file,
                '-o',
                os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + 
                    ('.exe' if platform.system() == 'Windows' else '')
                )
            ],
            'env_setup': None
        },
        'Java': {
            'file_extensions': ['.java'],
            'run_command': lambda file: [
                'java',
                '-cp',
                os.path.dirname(file),
                os.path.splitext(os.path.basename(file))[0]
            ],
            'build_command': lambda file: ['javac', file],
            'env_setup': None
        },
        'JavaScript': {
            'file_extensions': ['.js'],
            'run_command': lambda file: ['node', file],
            'build_command': None,
            'env_setup': None
        }
    }

    @classmethod
    def detect_language(cls, file_path):
        if not file_path:
            return None
        ext = os.path.splitext(file_path)[1].lower()
        for lang, config in cls.LANGUAGE_CONFIGS.items():
            if ext in config['file_extensions']:
                return lang
        return None

    @classmethod
    def build_and_run(cls, file_path, output_callback):
        if not file_path:
            output_callback("No file selected")
            return False

        if not os.path.exists(file_path):
            output_callback(f"File not found: {file_path}")
            return False

        language = cls.detect_language(file_path)
        if not language:
            output_callback(f"Unsupported file type: {os.path.splitext(file_path)[1]}")
            return False

        config = cls.LANGUAGE_CONFIGS[language]
        working_dir = os.path.dirname(file_path)

        # Clear previous output
        output_callback("=" * 50)
        output_callback(f"Running: {os.path.basename(file_path)}")
        output_callback("=" * 50 + "\n")

        # Build if necessary
        if config['build_command']:
            try:
                build_cmd = config['build_command'](file_path)
                output_callback(f"Building with: {' '.join(build_cmd)}\n")
                
                process = subprocess.Popen(
                    build_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=working_dir
                )
                stdout, stderr = process.communicate()

                if stdout:
                    output_callback(stdout)
                if stderr:
                    output_callback(f"Build errors:\n{stderr}")
                    return False
                if process.returncode != 0:
                    output_callback("Build failed with error code: " + str(process.returncode))
                    return False
                
                output_callback("Build successful!\n")
            except Exception as e:
                output_callback(f"Build failed: {str(e)}")
                return False

        # Run the program with interactive input/output
        try:
            run_cmd = config['run_command'](file_path)
            output_callback("Program output:\n" + "-" * 50 + "\n")
            
            # Create process with pipes for input/output
            process = subprocess.Popen(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=working_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == 'Windows' else 0
            )

            # Create and show the terminal window
            terminal_window = RunTerminal(process, output_callback)
            terminal_window.exec()  # Use exec() instead of show() to make it modal
            
            return True
            
        except Exception as e:
            output_callback(f"Run failed: {str(e)}")
            return False

    @classmethod
    def build_only(cls, file_path, output_callback):
        if not file_path:
            output_callback("No file selected")
            return False

        language = cls.detect_language(file_path)
        if not language:
            output_callback(f"Unsupported file type: {os.path.splitext(file_path)[1]}")
            return False

        config = cls.LANGUAGE_CONFIGS[language]
        if not config['build_command']:
            output_callback(f"{language} does not require building")
            return True

        try:
            build_cmd = config['build_command'](file_path)
            output_callback(f"Building with command: {' '.join(build_cmd)}\n")
            
            process = subprocess.Popen(
                build_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(file_path)
            )
            stdout, stderr = process.communicate()

            if stdout:
                output_callback(stdout)
            if stderr:
                output_callback(f"Build errors:\n{stderr}")
                return False
            if process.returncode != 0:
                output_callback("Build failed with error code: " + str(process.returncode))
                return False
            
            output_callback("Build successful!")
            return True
            
        except Exception as e:
            output_callback(f"Build failed: {str(e)}")
            return False

    @classmethod
    def run_only(cls, file_path, output_callback):
        if not file_path:
            output_callback("No file selected")
            return False

        language = cls.detect_language(file_path)
        if not language:
            output_callback(f"Unsupported file type: {os.path.splitext(file_path)[1]}")
            return False

        config = cls.LANGUAGE_CONFIGS[language]
        try:
            run_cmd = config['run_command'](file_path)
            output_callback(f"Running: {' '.join(run_cmd)}\n")
            
            process = subprocess.Popen(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(file_path)
            )
            stdout, stderr = process.communicate()

            if stdout:
                output_callback(stdout)
            if stderr:
                output_callback(f"Runtime errors:\n{stderr}")
            if process.returncode != 0:
                output_callback("Program exited with error code: " + str(process.returncode))
                return False
            
            output_callback("Program completed successfully!")
            return True
            
        except Exception as e:
            output_callback(f"Run failed: {str(e)}")
            return False

# Add Settings dialog
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.layout = QFormLayout(self)
        
        # Create tabs
        self.tab_widget = QTabWidget()
        
        # Editor settings
        editor_widget = QWidget()
        editor_layout = QFormLayout(editor_widget)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        editor_layout.addRow("Font Size:", self.font_size)
        
        self.tab_size = QSpinBox()
        self.tab_size.setRange(2, 8)
        editor_layout.addRow("Tab Size:", self.tab_size)
        
        self.tab_widget.addTab(editor_widget, "Editor")
        
        # Theme settings
        theme_widget = QWidget()
        theme_layout = QFormLayout(theme_widget)
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light", "Dracula"])
        theme_layout.addRow("Theme:", self.theme_selector)
        
        self.tab_widget.addTab(theme_widget, "Theme")
        
        self.layout.addWidget(self.tab_widget)
        
        # Dialog buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.font_size.setValue(settings.get('font_size', 12))
                self.tab_size.setValue(settings.get('tab_size', 4))
                self.theme_selector.setCurrentText(settings.get('theme', 'Dark'))
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            'font_size': self.font_size.value(),
            'tab_size': self.tab_size.value(),
            'theme': self.theme_selector.currentText()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        return settings

# Update MainWindow class with new methods
class MainWindow(QMainWindow):
    THEMES = {
        "Dark": {
            "background": "#1E1E1E",
            "editor_bg": "#1E1E1E",
            "editor_text": "#D4D4D4",
            "line_numbers": "#858585",
            "selection": "#264F78",
            "cursor": "#A6A6A6"
        },
        "Light": {
            "background": "#FFFFFF",
            "editor_bg": "#FFFFFF",
            "editor_text": "#000000",
            "line_numbers": "#237893",
            "selection": "#ADD6FF",
            "cursor": "#000000"
        },
        "Dracula": {
            "background": "#282A36",
            "editor_bg": "#282A36",
            "editor_text": "#F8F8F2",
            "line_numbers": "#6272A4",
            "selection": "#44475A",
            "cursor": "#F8F8F2"
        }
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pylight IDE")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize FileSystemHelper first
        self.fs_helper = FileSystemHelper(self)
        
        # Set application icon
        app_icon = QIcon("res/Pyide.png")
        self.setWindowIcon(app_icon)
        QApplication.setWindowIcon(app_icon)
        
        # Initialize current_file and project path
        self.current_file = None
        self.project_path = None
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Add flag to track welcome screen state
        self.welcome_screen_visible = True
        
        # Initialize UI components but don't show them yet
        self.initialize_ui_components()
        
        # Show welcome screen initially
        self.show_welcome_screen()

        # Add window flags for proper closing
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowCloseButtonHint
        )

    def initialize_ui_components(self):
        """Initialize all UI components but keep them hidden"""
        # Create all UI components
        self.create_editor_components()
        self.setup_toolbar()  # Changed from create_toolbar to setup_toolbar
        self.setup_statusbar()  # Changed for consistency
        self.setup_terminal()  # Changed for consistency
        self.setup_build_tools()
        
        # Initialize managers
        self.project_manager = ProjectManager(self)
        self.debug_manager = DebugManager(self)
        self.git_manager = GitManager(self)
        
        # Create dock widgets
        self.setup_dock_widgets()  # Changed for consistency
        self.setup_output_panel()  # Changed for consistency
        self.setup_build_panel()  # Changed for consistency
        
        # Hide all components initially
        self.hide_editor_components()

    def create_editor_components(self):
        """Create editor components"""
        # Create main splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        # Create file tree
        self.file_tree = QTreeView()
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                border: none;
                color: #CCCCCC;
                padding: 5px;
            }
            QTreeView::item {
                padding: 5px;
                border-radius: 3px;
            }
            QTreeView::item:hover {
                background-color: #2A2D2E;
            }
            QTreeView::item:selected {
                background-color: #37373D;
            }
            QTreeView::branch {
                background: transparent;
            }
        """)
        
        # Set up file model with hidden columns
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.file_tree.setModel(self.file_model)
        
        # Hide all columns except name
        self.file_tree.setHeaderHidden(True)
        for i in range(1, self.file_model.columnCount()):
            self.file_tree.hideColumn(i)
        
        self.main_splitter.addWidget(self.file_tree)
        
        # Create tab widget using EditorTabWidget instead of QTabWidget
        self.tab_widget = EditorTabWidget(self)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.close_tab)  # Use EditorTabWidget's close_tab
        
        self.main_splitter.addWidget(self.tab_widget)
        
        # Set splitter proportions
        self.main_splitter.setStretchFactor(0, 0)  # File tree doesn't stretch
        self.main_splitter.setStretchFactor(1, 1)  # Tab widget stretches
        
        # Add to main layout
        self.main_layout.addWidget(self.main_splitter)

    def create_enhanced_editor(self):
        """Create an enhanced code editor"""
        editor = QPlainTextEdit()
        
        # Add line number area methods to editor
        def lineNumberAreaWidth():
            digits = len(str(max(1, editor.blockCount())))
            space = 3 + editor.fontMetrics().horizontalAdvance('9') * digits
            return space

        def updateLineNumberAreaWidth(dummy=0):
            editor.setViewportMargins(lineNumberAreaWidth(), 0, 0, 0)

        def updateLineNumberArea(rect, dy):
            if dy:
                editor.line_number_area.scroll(0, dy)
            else:
                editor.line_number_area.update(0, rect.y(), editor.line_number_area.width(), rect.height())
            if rect.contains(editor.viewport().rect()):
                updateLineNumberAreaWidth()

        def lineNumberAreaPaintEvent(event):
            painter = QPainter(editor.line_number_area)
            painter.fillRect(event.rect(), QColor("#1E1E1E"))

            block = editor.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = editor.contentOffset()
            top = editor.blockBoundingGeometry(block).translated(offset).top()
            bottom = top + editor.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.setPen(QColor("#858585"))
                    painter.drawText(0, int(top), editor.line_number_area.width(), 
                                   editor.fontMetrics().height(),
                                   Qt.AlignRight, number)
                block = block.next()
                top = bottom
                bottom = top + editor.blockBoundingRect(block).height()
                block_number += 1

        # Add methods to editor
        editor.lineNumberAreaWidth = lineNumberAreaWidth
        editor.updateLineNumberAreaWidth = updateLineNumberAreaWidth
        editor.updateLineNumberArea = updateLineNumberArea
        editor.lineNumberAreaPaintEvent = lineNumberAreaPaintEvent

        # Set up editor styling
        editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                selection-background-color: #264F78;
                selection-color: #FFFFFF;
                padding: 5px;
                line-height: 1.5;
            }
            QScrollBar:vertical {
                background: #1E1E1E;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #525252;
            }
            QScrollBar:horizontal {
                background: #1E1E1E;
                height: 12px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: #424242;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #525252;
            }
        """)

        # Set editor features
        editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Set tab width using font metrics
        font_metrics = QFontMetricsF(editor.font())
        tab_width = font_metrics.horizontalAdvance(' ') * 4
        editor.setTabStopDistance(tab_width)
        
        # Add line numbers
        editor.line_number_area = LineNumberArea(editor)
        editor.blockCountChanged.connect(editor.updateLineNumberAreaWidth)
        editor.updateRequest.connect(editor.updateLineNumberArea)
        editor.updateLineNumberAreaWidth()
        
        # Add syntax highlighting
        highlighter = PythonHighlighter(editor.document())
        
        # Add drag & drop support
        editor.setAcceptDrops(True)
        
        def dragEnterEvent(event):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
        
        def dropEvent(event):
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    self.load_file(file_path)
        
        editor.dragEnterEvent = dragEnterEvent
        editor.dropEvent = dropEvent
        
        return editor

    def show_welcome_screen(self):
        """Show the welcome screen"""
        if not hasattr(self, 'welcome_page'):
            self.welcome_page = WelcomePage(self)
            self.welcome_page.project_opened.connect(self.handle_project_open)
            self.main_layout.addWidget(self.welcome_page)
        else:
            self.welcome_page.show()
        
        # Hide editor components
        self.hide_editor_components()
        self.welcome_screen_visible = True

    def toggle_welcome_screen(self):
        """Toggle between welcome screen and editor interface"""
        if self.welcome_screen_visible:
            if hasattr(self, 'project_path') and self.project_path:
                self.show_editor_interface()
        else:
            self.show_welcome_screen()

    def handle_project_open(self, project_path):
        """Handle project opening in an organized way"""
        try:
            # Store project path
            self.project_path = project_path
            
            # Hide welcome screen
            self.cleanup_welcome_screen()
            
            # Create and show project explorer
            self.create_project_panel(project_path)
            
            # Show main editor interface
            if hasattr(self, 'main_splitter'):
                self.main_splitter.show()
            if hasattr(self, 'toolbar'):
                self.toolbar.show()
            self.statusBar().show()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")
            self.show_welcome_screen()

    def create_project_panel(self, project_path):
        """Create project panel with file operations"""
        # Create dock widget
        self.project_dock = QDockWidget("Project Explorer", self)
        self.project_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Create main widget
        explorer_widget = QWidget()
        layout = QVBoxLayout(explorer_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create toolbar for file operations
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(2)
        
        # Add file button with + icon
        new_file_btn = QPushButton("＋")
        new_file_btn.setToolTip("New File (Ctrl+N)")
        new_file_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #50FA7B;
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: rgba(80, 250, 123, 0.1);
                border-radius: 3px;
            }
        """)
        new_file_btn.clicked.connect(self.create_new_file)
        
        # Add folder button with F+ icon
        new_folder_btn = QPushButton("F＋")
        new_folder_btn.setToolTip("New Folder (Ctrl+Shift+N)")
        new_folder_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #BD93F9;
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: rgba(189, 147, 249, 0.1);
                border-radius: 3px;
            }
        """)
        new_folder_btn.clicked.connect(self.create_new_folder)
        
        toolbar_layout.addWidget(new_file_btn)
        toolbar_layout.addWidget(new_folder_btn)
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar)
        
        # Create file system model
        self.project_model = QFileSystemModel()
        self.project_model.setRootPath(project_path)
        
        # Create tree view
        self.project_tree = QTreeView()
        self.project_tree.setModel(self.project_model)
        self.project_tree.setRootIndex(self.project_model.index(project_path))
        self.project_tree.setAnimated(True)
        self.project_tree.setIndentation(20)
        self.project_tree.setSortingEnabled(True)
        
        # Hide unnecessary columns
        self.project_tree.hideColumn(1)  # Size
        self.project_tree.hideColumn(2)  # Type
        self.project_tree.hideColumn(3)  # Date Modified
        
        # Style the tree view
        self.project_tree.setStyleSheet("""
            QTreeView {
                background-color: #282A36;
                border: none;
                color: #F8F8F2;
            }
            QTreeView::item {
                padding: 5px;
                border-radius: 3px;
            }
            QTreeView::item:hover {
                background: rgba(68, 71, 90, 0.3);
            }
            QTreeView::item:selected {
                background: rgba(68, 71, 90, 0.7);
            }
            QTreeView::branch {
                background: transparent;
            }
            QTreeView::branch:has-siblings:!adjoins-item {
                border-image: url(res/vline.png) 0;
            }
            QTreeView::branch:has-siblings:adjoins-item {
                border-image: url(res/branch-more.png) 0;
            }
            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(res/branch-end.png) 0;
            }
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(res/branch-closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                border-image: none;
                image: url(res/branch-open.png);
            }
        """)
        
        # Connect signals
        self.project_tree.doubleClicked.connect(self.open_file_from_tree)
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.project_tree)
        self.project_dock.setWidget(explorer_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

    def show_context_menu(self, position):
        """Show context menu for project tree"""
        index = self.project_tree.indexAt(position)
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #252526;
                color: #CCCCCC;
                border: 1px solid #454545;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: #37373D;
            }
        """)
        
        # Get current path
        current_path = self.project_model.filePath(index) if index.isValid() else self.project_path
        is_dir = os.path.isdir(current_path) if index.isValid() else True
        
        # Add New submenu
        new_menu = menu.addMenu("New")
        
        # Add file action
        new_file_action = new_menu.addAction("New File")
        new_file_action.triggered.connect(lambda checked, path=current_path: self.create_new_file(path))
        
        # Add folder action
        new_folder_action = new_menu.addAction("New Folder")
        new_folder_action.triggered.connect(lambda: self.create_new_folder(current_path))
        
        if index.isValid():
            menu.addSeparator()
            
            # Add rename action
            rename_action = menu.addAction("Rename")
            rename_action.triggered.connect(lambda: self.rename_item(current_path))
            
            # Add delete action
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_item(current_path))
        
        menu.exec(self.project_tree.viewport().mapToGlobal(position))

    def create_new_file(self, directory=None):
        """Create a new file in the specified directory"""
        try:
            # Get directory
            if directory is None:
                directory = self.project_path if hasattr(self, 'project_path') else os.getcwd()
            
            # Show dialog
            dialog = NewFileDialog(str(directory), self)  # Convert directory to string
            if dialog.exec() == QDialog.Accepted:
                # Get the file name and type directly
                name = dialog.name_input.text().strip()
                selected_type = dialog.file_type.currentText()
                
                # Get the extension
                if selected_type == "Custom":
                    ext = dialog.custom_ext_input.text().strip()
                    if ext and not ext.startswith('.'):
                        ext = '.' + ext
                else:
                    ext = dialog.file_types.get(selected_type, '')
                
                # Create full file name
                full_name = name + ext if not name.endswith(ext) else name
                
                # Create full path
                full_path = os.path.join(str(directory), full_name)
                
                # Create the file
                if not os.path.exists(full_path):
                    # Create directories if needed
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    # Create empty file
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    
                    # Refresh view
                    self.project_model.setRootPath(str(directory))
                    
                    # Show success
                    self.statusBar().showMessage(f"Created: {full_name}")
                    
                    # Open file
                    self.open_file_in_editor(full_path)
                    return True
                    
                else:
                    QMessageBox.warning(self, "Error", "File already exists!")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")
        
        return False

    def create_new_folder(self, directory=None):
        """Create a new folder with improved error handling"""
        try:
            if directory is None:
                directory = self.project_path if hasattr(self, 'project_path') else os.getcwd()
                
            dialog = NewFolderDialog(directory, self)
            if dialog.exec() == QDialog.Accepted:
                folder_name = dialog.get_folder_info()
                if folder_name:
                    # Create full path and ensure it's a string
                    folder_path = os.path.join(str(directory), str(folder_name))
                    
                    # Create the folder
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        
                        # Refresh project explorer
                        if hasattr(self, 'project_model'):
                            self.project_model.setRootPath(directory)
                        
                        # Update UI
                        self.statusBar().showMessage(f"Created folder: {folder_name}", 3000)
                        
                        # Select the new folder in project tree
                        if hasattr(self, 'project_tree'):
                            index = self.project_model.index(folder_path)
                            self.project_tree.setCurrentIndex(index)
                            self.project_tree.scrollTo(index)
                        
                        return folder_path
                    else:
                        QMessageBox.warning(
                            self,
                            "Folder Exists",
                            f"Folder '{folder_name}' already exists in this location."
                        )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create folder: {str(e)}"
            )
        return None

    def open_file_in_editor(self, file_path):
        """Open file in editor interface"""
        try:
            # Ensure editor interface is visible
            self.show_editor_interface()
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new tab with file
            editor = self.tab_widget.add_new_tab(os.path.basename(file_path))
            editor.setPlainText(content)
            editor.current_file = file_path
            
            # Apply appropriate syntax highlighting based on file extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.py':
                highlighter = PythonHighlighter(editor.document())
            # Add more syntax highlighters for other file types as needed
            
            # Update status bar
            self.statusBar().showMessage(f"Opened {file_path}")
            
            # Set focus to editor
            editor.setFocus()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def refresh_project_tree(self):
        """Refresh the project tree view"""
        if hasattr(self, 'project_model') and hasattr(self, 'project_tree'):
            current_path = self.project_model.rootPath()
            self.project_model.setRootPath("")
            self.project_model.setRootPath(current_path)
            
            # Restore expanded state
            if hasattr(self, 'project_tree'):
                index = self.project_tree.currentIndex()
                if index.isValid():
                    self.project_tree.expand(index)

    def rename_item(self, path):
        """Rename file or folder"""
        old_name = os.path.basename(path)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=old_name)
        if ok and new_name:
            try:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename: {str(e)}")

    def delete_item(self, path):
        """Delete file or folder"""
        msg = "Are you sure you want to delete this item?"
        reply = QMessageBox.question(self, "Confirm Delete", msg, 
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete: {str(e)}")

    def open_project_file(self, index):
        """Open file from project tree"""
        file_path = self.project_model.filePath(index)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                editor = self.create_new_tab(os.path.basename(file_path))
                editor.setPlainText(content)
                editor.current_file = file_path
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def show_editor_interface(self):
        """Switch from welcome screen to editor interface"""
        # Show editor components
        self.show_editor_components()
        
        # Set up project if path provided
        if self.project_path:
            self.file_model.setRootPath(self.project_path)
            self.file_tree.setRootIndex(self.file_model.index(self.project_path))
            
            # Update window title
            project_name = os.path.basename(self.project_path)
            self.setWindowTitle(f"Pylight IDE - {project_name}")

    def show_editor_components(self):
        """Show all editor components"""
        # Show main components
        self.main_splitter.show()
        self.file_tree.show()
        
        # Show toolbars and dock widgets
        self.toolbar.show()
        for dock in self.findChildren(QDockWidget):
            dock.show()
        
        # Show status bar
        self.statusBar().show()

    def hide_editor_components(self):
        """Hide all editor components"""
        # Hide main components
        self.main_splitter.hide()
        self.file_tree.hide()
        
        # Hide toolbars and dock widgets
        if hasattr(self, 'toolbar'):
            self.toolbar.hide()
        for dock in self.findChildren(QDockWidget):
            dock.hide()
        
        # Hide status bar
        self.statusBar().hide()

    def setup_project(self, path):
        """Set up project when opened"""
        self.project_path = path
        
        # Update file tree
        self.file_model.setRootPath(path)
        self.file_tree.setRootIndex(self.file_model.index(path))
        
        # Update window title
        project_name = os.path.basename(path)
        self.setWindowTitle(f"Pylight IDE - {project_name}")
        
        # Update recent projects
        self.update_recent_projects(path)

    def update_recent_projects(self, path):
        """Update recent projects list"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        recent_projects = settings.get('recent_projects', [])
        
        # Create project entry
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        project_entry = {
            'name': os.path.basename(path),
            'path': path,
            'last_opened': now
        }
        
        # Remove if already exists
        recent_projects = [p for p in recent_projects if p['path'] != path]
        
        # Add to front of list
        recent_projects.insert(0, project_entry)
        
        # Keep only last 10 projects
        settings['recent_projects'] = recent_projects[:10]
        
        # Save settings
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def add_to_recent_projects(self, path):
        """Add project to recent projects list"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        recent_projects = settings.get('recent_projects', [])
        project_entry = {
            'name': os.path.basename(path),
            'path': path
        }
        
        # Add to front of list and remove duplicates
        if project_entry in recent_projects:
            recent_projects.remove(project_entry)
        recent_projects.insert(0, project_entry)
        
        # Keep only last 10 projects
        settings['recent_projects'] = recent_projects[:10]
        
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    # Override these methods to handle project/file opening
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            if not self.project_path:
                # If no project is open, switch to editor interface
                self.show_editor_interface()
            self.load_file(file_name)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            self.show_editor_interface(folder)

    def load_file(self, file_name):
        try:
            with open(file_name, 'r') as f:
                content = f.read()
            editor = self.tab_widget.add_new_tab(
                title=os.path.basename(file_name),
                content=content
            )
            editor.current_file = file_name
            self.statusBar().showMessage(f"Opened {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def setup_ui(self):
        # Create main container with dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
        """)
        
        # Create main toolbar at the top
        self.main_toolbar = QToolBar()
        self.main_toolbar.setStyleSheet("""
            QToolBar {
                background: #2D2D2D;
                border: none;
                padding: 2px;
                spacing: 2px;
            }
            QToolButton {
                background: transparent;
                border: none;
                padding: 6px;
                color: #CCCCCC;
            }
            QToolButton:hover {
                background: #3D3D3D;
            }
        """)
        self.addToolBar(self.main_toolbar)
        
        # Add main actions to toolbar
        self.main_toolbar.addAction("File")
        self.main_toolbar.addAction("Edit")
        self.main_toolbar.addAction("Selection")
        self.main_toolbar.addAction("View")
        self.main_toolbar.addAction("Go")
        self.main_toolbar.addAction("Run")
        self.main_toolbar.addAction("Terminal")
        self.main_toolbar.addAction("Help")
        
        # Create central widget with horizontal layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create activity bar (left sidebar)
        self.activity_bar = self.create_activity_bar()
        self.main_layout.addWidget(self.activity_bar)

        # Create side panel (explorer, search, etc.)
        self.side_panel = self.create_side_panel()
        self.main_layout.addWidget(self.side_panel)

        # Create editor area
        self.editor_area = self.create_editor_area()
        self.main_layout.addWidget(self.editor_area)

        # Set the ratio between components
        self.main_layout.setStretch(0, 0)  # Activity bar - fixed width
        self.main_layout.setStretch(1, 0)  # Side panel - fixed width
        self.main_layout.setStretch(2, 1)  # Editor area - takes remaining space

    def create_activity_bar(self):
        """Create VSCode-style activity bar"""
        activity_bar = QWidget()
        activity_bar.setFixedWidth(48)
        activity_bar.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border: none;
            }
            QPushButton {
                border: none;
                padding: 12px;
                margin: 4px;
                border-radius: 4px;
                background-color: transparent;
                qproperty-iconSize: 24px 24px;
            }
            QPushButton:hover {
                background-color: #464646;
            }
            QPushButton:checked {
                background-color: #37373D;
                border-left: 2px solid #007ACC;
            }
        """)

        layout = QVBoxLayout(activity_bar)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(2)

        # Create activity buttons
        self.files_btn = self.create_activity_button("Files", "res/files.svg", True)
        self.search_btn = self.create_activity_button("Search", "res/search.svg")
        self.git_btn = self.create_activity_button("Source Control", "res/git.svg")
        self.debug_btn = self.create_activity_button("Run and Debug", "res/debug.svg")
        self.extensions_btn = self.create_activity_button("Extensions", "res/extensions.svg")

        layout.addWidget(self.files_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.git_btn)
        layout.addWidget(self.debug_btn)
        layout.addWidget(self.extensions_btn)
        layout.addStretch()

        return activity_bar

    def create_activity_button(self, tooltip, icon_path, checked=False):
        btn = QPushButton()
        btn.setIcon(QIcon(icon_path))
        btn.setToolTip(tooltip)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.clicked.connect(lambda: self.handle_activity_button(btn))
        return btn

    def create_side_panel(self):
        """Create VSCode-style side panel"""
        side_panel = QStackedWidget()
        side_panel.setFixedWidth(300)
        side_panel.setStyleSheet("""
            QWidget {
                background-color: #252526;
                border: none;
            }
        """)

        # Create and add panels
        self.explorer_panel = self.create_explorer_panel()
        self.search_panel = self.create_search_panel()
        self.git_panel = self.create_git_panel()
        self.debug_panel = self.create_debug_panel()
        self.extensions_panel = self.create_extensions_panel()

        side_panel.addWidget(self.explorer_panel)
        side_panel.addWidget(self.search_panel)
        side_panel.addWidget(self.git_panel)
        side_panel.addWidget(self.debug_panel)
        side_panel.addWidget(self.extensions_panel)

        return side_panel

    def create_explorer_panel(self):
        """Create VSCode-style explorer panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Explorer header
        header = QWidget()
        header.setStyleSheet("background-color: #252526;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 8, 8, 8)

        title = QLabel("EXPLORER")
        title.setStyleSheet("color: #BBBBBB; font-size: 11px; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(4)

        new_file_btn = self.create_explorer_action_button("New File", "res/new-file.svg")
        new_folder_btn = self.create_explorer_action_button("New Folder", "res/new-folder.svg")
        refresh_btn = self.create_explorer_action_button("Refresh", "res/refresh.svg")
        collapse_btn = self.create_explorer_action_button("Collapse", "res/collapse.svg")

        actions_layout.addWidget(new_file_btn)
        actions_layout.addWidget(new_folder_btn)
        actions_layout.addWidget(refresh_btn)
        actions_layout.addWidget(collapse_btn)

        header_layout.addWidget(actions_widget)
        layout.addWidget(header)

        # File tree
        self.file_tree = QTreeView()
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                border: none;
                color: #CCCCCC;
                padding: 4px;
            }
            QTreeView::item {
                padding: 4px;
                color: #CCCCCC;
            }
            QTreeView::item:hover {
                background-color: #2A2D2E;
            }
            QTreeView::item:selected {
                background-color: #37373D;
            }
            QTreeView::branch {
                background: transparent;
            }
        """)

        self.file_model = QFileSystemModel()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.hideColumn(1)
        self.file_tree.hideColumn(2)
        self.file_tree.hideColumn(3)

        layout.addWidget(self.file_tree)
        return panel

    def create_editor_area(self):
        """Create VSCode-style editor area"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab bar
        self.tab_bar = QTabBar()
        self.tab_bar.setStyleSheet("""
            QTabBar {
                background: #1E1E1E;
            }
            QTabBar::tab {
                background: #2D2D2D;
                color: #CCCCCC;
                border: none;
                padding: 8px 25px 8px 15px;
                margin: 0;
            }
            QTabBar::tab:selected {
                background: #1E1E1E;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background: #2A2A2A;
            }
            QTabBar::close-button {
                image: url(res/close.svg);
                subcontrol-position: right;
                padding: 2px;
            }
            QTabBar::close-button:hover {
                background: #C84E4E;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.tab_bar)

        # Create editor stack
        self.editor_stack = QStackedWidget()
        layout.addWidget(self.editor_stack)

        # Create glassmorphic editor
        editor = GlassmorphicCodeEditor()
        editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(30, 30, 30, 0.95);
                color: #CCCCCC;
                border: none;
                selection-background-color: #264F78;
                selection-color: #FFFFFF;
            }
        """)
        self.editor_stack.addWidget(editor)

        return container

    def create_editor_tabs(self):
        """Create VSCode-style editor tabs"""
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #2D2D2D;
                color: #969696;
                border: none;
                padding: 8px 16px;
                min-width: 120px;
                max-width: 200px;
            }
            QTabBar::tab:selected {
                background: #1E1E1E;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background: #2A2A2A;
            }
            QTabBar::close-button {
                image: url(res/close.svg);
            }
            QTabBar::close-button:hover {
                background: #C84E4E;
                border-radius: 4px;
            }
        """)
        tabs.setTabsClosable(True)
        tabs.setMovable(True)
        return tabs

    def setup_toolbar(self):
        # Create main menu bar
        self.menubar = self.menuBar()
        self.menubar.setStyleSheet("""
            QMenuBar {
                background: #2D2D2D;
                color: #CCCCCC;
                border: none;
                padding: 2px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background: #3D3D3D;
            }
            QMenu {
                background: #2D2D2D;
                color: #CCCCCC;
                border: 1px solid #3D3D3D;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background: #3D3D3D;
            }
        """)

        # File Menu
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.create_action("New File", "Ctrl+N", self.new_file))
        file_menu.addAction(self.create_action("New Project", "Ctrl+Shift+N", self.create_new_project))
        file_menu.addAction(self.create_action("Open File", "Ctrl+O", self.open_file))
        file_menu.addAction(self.create_action("Open Folder", "Ctrl+K Ctrl+O", self.open_folder))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action("Save", "Ctrl+S", self.save_file))
        file_menu.addAction(self.create_action("Save As", "Ctrl+Shift+S", self.save_file_as))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action("Exit", "Alt+F4", self.close))

        # Edit Menu
        edit_menu = self.menubar.addMenu("Edit")
        edit_menu.addAction(self.create_action("Undo", "Ctrl+Z", lambda: self.get_current_editor().undo()))
        edit_menu.addAction(self.create_action("Redo", "Ctrl+Y", lambda: self.get_current_editor().redo()))
        edit_menu.addSeparator()
        edit_menu.addAction(self.create_action("Cut", "Ctrl+X", lambda: self.get_current_editor().cut()))
        edit_menu.addAction(self.create_action("Copy", "Ctrl+C", lambda: self.get_current_editor().copy()))
        edit_menu.addAction(self.create_action("Paste", "Ctrl+V", lambda: self.get_current_editor().paste()))

        # View Menu
        view_menu = self.menubar.addMenu("View")
        view_menu.addAction(self.create_action("Command Palette", "Ctrl+Shift+P", self.show_command_palette))
        view_menu.addSeparator()
        view_menu.addAction(self.create_action("Explorer", "Ctrl+Shift+E", self.toggle_explorer))
        view_menu.addAction(self.create_action("Search", "Ctrl+Shift+F", self.toggle_search))
        view_menu.addAction(self.create_action("Source Control", "Ctrl+Shift+G", self.toggle_source_control))
        view_menu.addAction(self.create_action("Debug", "Ctrl+Shift+D", self.toggle_debug))

        # Run Menu
        run_menu = self.menubar.addMenu("Run")
        run_menu.addAction(self.create_action("Start Debugging", "F5", self.start_debugging))
        run_menu.addAction(self.create_action("Run Without Debugging", "Ctrl+F5", self.run_without_debugging))
        run_menu.addAction(self.create_action("Stop", "Shift+F5", self.stop_debugging))

        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #2D2D2D;
                border: none;
                spacing: 2px;
            }
            QToolButton {
                background: transparent;
                border: none;
                padding: 6px;
                color: #CCCCCC;
            }
            QToolButton:hover {
                background: #3D3D3D;
            }
        """)
        self.addToolBar(self.toolbar)

        # Add main actions to toolbar
        self.toolbar.addAction(self.create_action("New File", "Ctrl+N", self.new_file, "new-file"))
        self.toolbar.addAction(self.create_action("Open File", "Ctrl+O", self.open_file, "open-file"))
        self.toolbar.addAction(self.create_action("Save", "Ctrl+S", self.save_file, "save"))
        self.toolbar.addSeparator()
        
        self.toolbar.addAction(self.create_action("Undo", "Ctrl+Z", lambda: self.get_current_editor().undo(), "undo"))
        self.toolbar.addAction(self.create_action("Redo", "Ctrl+Y", lambda: self.get_current_editor().redo(), "redo"))
        self.toolbar.addSeparator()
        
        self.toolbar.addAction(self.create_action("Run", "F5", self.run_current_file, "run"))
        self.toolbar.addAction(self.create_action("Debug", "Ctrl+F5", self.debug_current_file, "debug"))
        self.toolbar.addSeparator()
        
        # Add theme selector
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #CCCCCC; padding: 0 5px;")
        self.toolbar.addWidget(theme_label)
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light", "Dracula"])
        theme_combo.setStyleSheet("""
            QComboBox {
                background: #3D3D3D;
                color: #CCCCCC;
                border: none;
                padding: 5px;
                min-width: 100px;
            }
        """)
        theme_combo.currentTextChanged.connect(self.change_theme)
        self.toolbar.addWidget(theme_combo)

    def create_action(self, text, shortcut=None, callback=None, icon=None):
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
        if callback:
            action.triggered.connect(callback)
        if icon:
            action.setIcon(QIcon(f"res/{icon}.png"))
        return action
    
    def setup_statusbar(self):
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(40, 42, 54, 0.9);
                color: #F8F8F2;
            }
        """)
        self.setStatusBar(status_bar)
    
    def setup_terminal(self):
        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal = Terminal()
        self.terminal_dock.setWidget(self.terminal)
        self.terminal_dock.setStyleSheet("""
            QDockWidget {
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            QDockWidget::title {
                background: rgba(40, 42, 54, 0.9);
                color: #F8F8F2;
                padding-left: 5px;
            }
        """)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.terminal_dock)
    
    def new_file(self):
        self.tab_widget.add_new_tab()

    def save_file(self):
        editor = self.tab_widget.currentWidget()
        if not editor:
            return
        
        if not hasattr(editor, 'current_file') or not editor.current_file:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File")
            if file_name:
                editor.current_file = file_name
                self.tab_widget.setTabText(
                    self.tab_widget.currentIndex(),
                    os.path.basename(file_name))
        
        if hasattr(editor, 'current_file') and editor.current_file:
            try:
                with open(editor.current_file, 'w') as f:
                    f.write(editor.toPlainText())
                self.statusBar().showMessage(f"Saved {editor.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def setup_build_tools(self):
        # Add build and run actions to toolbar
        self.toolbar.addSeparator()
        
        build_action = QAction("Build", self)
        build_action.triggered.connect(self.build_current_file)
        self.toolbar.addAction(build_action)
        
        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_current_file)
        self.toolbar.addAction(run_action)
        
        build_run_action = QAction("Build & Run", self)
        build_run_action.triggered.connect(self.build_and_run_current_file)
        self.toolbar.addAction(build_run_action)
        
        # Add settings action
        self.toolbar.addSeparator()
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        self.toolbar.addAction(settings_action)

    def build_current_file(self):
        current_file = self.get_current_file()
        if not current_file:
            self.statusBar().showMessage("No file to build")
            return
        BuildRunner.build_and_run(current_file, self.output_to_terminal)

    def run_current_file(self):
        current_file = self.get_current_file()
        if not current_file:
            self.statusBar().showMessage("No file to run")
            return
        BuildRunner.build_and_run(current_file, self.output_to_terminal)

    def build_and_run_current_file(self):
        current_file = self.get_current_file()
        if not current_file:
            self.statusBar().showMessage("No file to build and run")
            return
        BuildRunner.build_and_run(current_file, self.output_to_terminal)

    def output_to_terminal(self, text):
        if hasattr(self, 'terminal'):
            self.terminal.terminal_output.appendPlainText(text)

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            settings = dialog.save_settings()
            self.apply_settings(settings)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.apply_settings(settings)
        except FileNotFoundError:
            pass

    def apply_settings(self, settings):
        editor = self.get_current_editor()
        if editor:
            # Apply font size
            font = editor.font()
            font.setPointSize(settings.get('font_size', 12))
            editor.setFont(font)
            
            # Apply tab size
            editor.setTabStopDistance(
                settings.get('tab_size', 4) * editor.fontMetrics().horizontalAdvance(' ')
            )  # Added closing parenthesis here
            
            # Apply theme
            theme = settings.get('theme', 'Dark')
            self.apply_theme(theme)

    def apply_theme(self, theme_name):
        if theme_name in self.THEMES:
            theme = self.THEMES[theme_name]
            self.setStyleSheet(f"""
                QMainWindow {{
                    background: {theme['background']};
                }}
            """)
            editor = self.get_current_editor()
            if editor:
                editor.setStyleSheet(f"""
                    QPlainTextEdit {{
                        background-color: {theme['editor_bg']};
                        color: {theme['editor_text']};
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 10px;
                    }}
                """)

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New", self.new_file, "Ctrl+N")
        file_menu.addAction("Open", self.open_file, "Ctrl+O")
        file_menu.addAction("Save", self.save_file, "Ctrl+S")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Alt+F4")

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", lambda: self.get_current_editor().undo(), "Ctrl+Z")
        edit_menu.addAction("Redo", lambda: self.get_current_editor().redo(), "Ctrl+Y")
        edit_menu.addSeparator()
        edit_menu.addAction("Find/Replace", self.show_find_replace, "Ctrl+F")
        edit_menu.addAction("Go to Line", self.goto_line, "Ctrl+G")

        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Terminal", self.toggle_terminal, "Ctrl+`")
        view_menu.addAction("Toggle File Tree", self.toggle_file_tree, "Ctrl+B")
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings", self.show_settings)
        tools_menu.addAction("Change Font", self.change_font)
        tools_menu.addAction("Color Picker", self.show_color_picker)

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation", self.show_documentation)
        help_menu.addAction("Check for Updates", self.check_updates)
        help_menu.addSeparator()
        help_menu.addAction("About Pylight IDE", self.show_about)

    def show_find_replace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    def goto_line(self):
        line, ok = QInputDialog.getInt(self, "Go to Line", "Line number:",
                                     1, 1, self.editor.blockCount())
        if ok:
            cursor = QTextCursor(self.editor.document().findBlockByLineNumber(line - 1))
            self.editor.setTextCursor(cursor)

    def toggle_terminal(self):
        if hasattr(self, 'terminal_dock'):
            self.terminal_dock.setVisible(not self.terminal_dock.isVisible())

    def toggle_file_tree(self):
        self.file_tree.setVisible(not self.file_tree.isVisible())

    def change_font(self):
        font, ok = QFontDialog.getFont(self.editor.font(), self)
        if ok:
            self.editor.setFont(font)

    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.editor.textCursor()
            cursor.insertText(f"#{color.name()[1:]}")

    def get_current_editor(self):
        return self.tab_widget.currentWidget()

    def setup_dock_widgets(self):
        try:
            # Project explorer
            project_dock = QDockWidget("Project Explorer", self)
            project_tree = self.project_manager.get_project_tree()
            project_dock.setWidget(project_tree)
            self.addDockWidget(Qt.LeftDockWidgetArea, project_dock)
            
            # Debug panel
            debug_dock = QDockWidget("Debug", self)
            debug_panel = self.debug_manager.get_debug_panel()
            debug_dock.setWidget(debug_panel)
            self.addDockWidget(Qt.RightDockWidgetArea, debug_dock)
            
            # Git panel
            git_dock = QDockWidget("Git", self)
            git_panel = self.git_manager.get_git_panel()
            git_dock.setWidget(git_panel)
            self.addDockWidget(Qt.BottomDockWidgetArea, git_dock)
            
        except Exception as e:
            QMessageBox.warning(self, "Setup Warning", f"Error setting up dock widgets: {str(e)}")

    def get_current_file(self):
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            return editor.current_file
        return None

    def setup_output_panel(self):
        """Setup the output panel for build/run results"""
        output_dock = QDockWidget("Output", self)
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        # Create output text area
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: none;
                font-family: 'Consolas';
                padding: 5px;
            }
        """)
        output_layout.addWidget(self.output_text)
        
        # Add toolbar for output panel
        output_toolbar = QToolBar()
        output_toolbar.setStyleSheet("""
            QToolBar {
                background: rgba(40, 42, 54, 0.7);
                border: none;
                padding: 2px;
            }
        """)
        
        # Add clear action
        clear_action = QAction("Clear Output", self)
        clear_action.triggered.connect(self.output_text.clear)
        output_toolbar.addAction(clear_action)
        
        output_layout.addWidget(output_toolbar)
        
        output_dock.setWidget(output_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, output_dock)
        
        # Update output_to_terminal to use both terminal and output panel
        def new_output_to_terminal(text):
            if hasattr(self, 'terminal'):
                current_terminal = self.terminal.terminal_tabs.currentWidget()
                if current_terminal:
                    current_terminal.output.appendPlainText(text)
            self.output_text.appendPlainText(text)
        
        self.output_to_terminal = new_output_to_terminal

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def show_documentation(self):
        QDesktopServices.openUrl(QUrl("https://pylight-ide.readthedocs.io"))

    def check_updates(self):
        # Implement update checking logic here
        QMessageBox.information(self, "Updates", "You are using the latest version of Pylight IDE")

    def setup_build_panel(self):
        self.build_panel = BuildRunPanel(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.build_panel)

    def setup_file_tree(self):
        """Setup file tree with drag & drop and context menu"""
        self.file_tree.setDragEnabled(True)
        self.file_tree.setAcceptDrops(True)
        self.file_tree.setDropIndicatorShown(True)
        self.file_tree.setDragDropMode(QTreeView.InternalMove)
        
        # Add context menu
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_file_context_menu)

    def show_file_context_menu(self, position):
        """Show context menu for file tree"""
        index = self.file_tree.indexAt(position)
        menu = QMenu()
        
        # Add actions
        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        
        # Get selected item path
        if index.isValid():
            path = self.file_model.filePath(index)
            menu.addSeparator()
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            
            # Connect actions with the path
            rename_action.triggered.connect(lambda: self.rename_item(path))
            delete_action.triggered.connect(lambda: self.delete_item(path))
        
        # Connect new file/folder actions
        new_file_action.triggered.connect(self.create_new_file)
        new_folder_action.triggered.connect(self.create_new_folder)
        
        menu.exec(self.file_tree.viewport().mapToGlobal(position))

    def create_new_file_at(self, parent_index):
        """Create new file at specified location"""
        parent_path = self.file_model.filePath(parent_index) if parent_index.isValid() else self.project_path
        
        name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and name:
            try:
                file_path = os.path.join(parent_path, name)
                with open(file_path, 'w') as f:
                    f.write("")
                self.load_file(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {str(e)}")

    def create_new_folder_at(self, parent_index):
        """Create new folder at specified location"""
        parent_path = self.file_model.filePath(parent_index) if parent_index.isValid() else self.project_path
        
        name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and name:
            try:
                folder_path = os.path.join(parent_path, name)
                os.makedirs(folder_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder: {str(e)}")

    def delete_file_or_folder(self, index):
        """Delete file or folder"""
        path = self.file_model.filePath(index)
        name = self.file_model.fileName(index)
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    # Close tab if file is open
                    self.close_file_tab(path)
                else:
                    import shutil
                    shutil.rmtree(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete: {str(e)}")

    def rename_file_or_folder(self, index):
        """Rename file or folder"""
        old_path = self.file_model.filePath(index)
        old_name = self.file_model.fileName(index)
        
        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "Enter new name:",
            QInputDialog.Normal,
            old_name
        )
        
        if ok and new_name:
            try:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                # Update tab if file is open
                self.update_file_tab(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename: {str(e)}")

    def close_file_tab(self, file_path):
        """Close tab for specified file"""
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if hasattr(editor, 'current_file') and editor.current_file == file_path:
                self.tab_widget.removeTab(i)
                break

    def update_file_tab(self, old_path, new_path):
        """Update tab for renamed file"""
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if hasattr(editor, 'current_file') and editor.current_file == old_path:
                editor.current_file = new_path
                self.tab_widget.setTabText(i, os.path.basename(new_path))
                break

    def create_new_file(self):
        """Create a new file in the current project"""
        if not self.project_path:
            QMessageBox.warning(self, "Warning", "Please open a project first")
            return
            
        dialog = NewFileDialog(self.project_path, self)
        if dialog.exec():
            file_info = dialog.get_file_info()
            try:
                # Create the file
                file_path = os.path.join(self.project_path, file_info['path'])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['template'])
                
                # Open the file in editor
                self.load_file(file_path)
                
                # Refresh file tree
                self.file_model.setRootPath(self.project_path)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")

    def create_new_folder(self):
        """Create a new folder in the current project"""
        if not self.project_path:
            QMessageBox.warning(self, "Warning", "Please open a project first")
            return
            
        dialog = NewFolderDialog(self.project_path, self)
        if dialog.exec():
            folder_path = dialog.get_folder_info()
            try:
                # Create the folder
                full_path = os.path.join(self.project_path, folder_path)
                os.makedirs(full_path, exist_ok=True)
                
                # Refresh file tree
                self.file_model.setRootPath(self.project_path)
                
                self.statusBar().showMessage(f"Created folder: {folder_path}", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")

    def create_new_project(self):
        """Create a new project"""
        dialog = NewProjectDialog(self)
        if dialog.exec():
            project_info = dialog.get_project_info()
            try:
                # Create project directory
                project_path = os.path.join(project_info['location'], project_info['name'])
                if os.path.exists(project_path):
                    raise ValueError(f"Project directory already exists: {project_path}")
                
                os.makedirs(project_path, exist_ok=True)
                
                # Create project structure
                os.makedirs(os.path.join(project_path, 'src'), exist_ok=True)
                os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
                os.makedirs(os.path.join(project_path, 'docs'), exist_ok=True)
                
                # Create initial files
                self.create_initial_project_files(project_path, project_info['type'])
                
                # Open the project
                self.show_editor_interface(project_path)
                
                # Show success message
                self.statusBar().showMessage(f"Created project: {project_info['name']}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")

    def create_initial_project_files(self, project_path, project_type):
        """Create initial project files based on type"""
        try:
            if project_type == "Python":
                with open(os.path.join(project_path, 'src', 'main.py'), 'w') as f:
                    f.write('def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()')
            elif project_type == "C++":
                with open(os.path.join(project_path, 'src', 'main.cpp'), 'w') as f:
                    f.write('#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}')
            elif project_type == "Java":
                with open(os.path.join(project_path, 'src', 'Main.java'), 'w') as f:
                    f.write('public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}')
        except Exception as e:
            raise Exception(f"Failed to create project files: {str(e)}")

    def save_file_as(self):
        """Save current file with a new name"""
        editor = self.get_current_editor()
        if editor:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save File As",
                "",
                "All Files (*.*);;"
                "Python Files (*.py);;"
                "C++ Files (*.cpp *.h);;"
                "Text Files (*.txt)"
            )
            if file_name:
                try:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    
                    # Update editor's current file
                    editor.current_file = file_name
                    
                    # Update tab text
                    current_index = self.tab_widget.currentIndex()
                    self.tab_widget.setTabText(current_index, os.path.basename(file_name))
                    
                    # Show success message
                    self.statusBar().showMessage(f"Saved as: {file_name}")
                    
                    # Add to recent files
                    self.add_to_recent_files(file_name)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def add_to_recent_files(self, file_path):
        """Add file to recent files list"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        recent_files = settings.get('recent_files', [])
        file_entry = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'last_opened': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to front of list and remove duplicates
        if file_entry in recent_files:
            recent_files.remove(file_entry)
        recent_files.insert(0, file_entry)
        
        # Keep only last 10 files
        settings['recent_files'] = recent_files[:10]
        
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def show_command_palette(self):
        """Show command palette for quick actions"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #252526;
                color: #CCCCCC;
                border: 1px solid #454545;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
        """)

        # Add common actions
        actions = [
            ("New File", self.create_new_file),
            ("Open File", self.open_file),
            ("Save", self.save_file),
            ("Save As", self.save_file_as),
            None,  # Separator
            ("Toggle Terminal", self.toggle_terminal),
            ("Toggle Explorer", self.toggle_explorer),
            None,  # Separator
            ("Run File", self.run_current_file),
            ("Build", self.build_current_file),
            ("Debug", self.debug_current_file)
        ]

        for action in actions:
            if action is None:
                menu.addSeparator()
            else:
                name, callback = action
                menu.addAction(name, callback)

        # Show menu at cursor position
        cursor = self.mapFromGlobal(QCursor.pos())
        menu.exec_(self.mapToGlobal(cursor))

    def toggle_explorer(self):
        """Toggle explorer panel visibility"""
        if hasattr(self, 'explorer_panel'):
            self.explorer_panel.setVisible(not self.explorer_panel.isVisible())

    def toggle_terminal(self):
        """Toggle terminal panel visibility"""
        if hasattr(self, 'terminal_dock'):
            self.terminal_dock.setVisible(not self.terminal_dock.isVisible())

    def toggle_search(self):
        """Toggle search panel visibility"""
        if hasattr(self, 'search_panel'):
            self.search_panel.setVisible(not self.search_panel.isVisible())

    def toggle_source_control(self):
        """Toggle source control panel visibility"""
        if hasattr(self, 'git_panel'):
            self.git_panel.setVisible(not self.git_panel.isVisible())

    def toggle_debug(self):
        """Toggle debug panel visibility"""
        if hasattr(self, 'debug_panel'):
            self.debug_panel.setVisible(not self.debug_panel.isVisible())

    def build_current_file(self):
        """Build the current file"""
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            BuildRunner.build_only(editor.current_file, self.output_to_terminal)

    def debug_current_file(self):
        """Debug the current file"""
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            if hasattr(self, 'debug_manager'):
                self.debug_manager.debug_file(editor.current_file)

    def start_debugging(self):
        """Start debugging session"""
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            if hasattr(self, 'debug_manager'):
                self.debug_manager.start_debugging(editor.current_file)
            else:
                self.statusBar().showMessage("Debug manager not initialized")

    def run_without_debugging(self):
        """Run current file without debugging"""
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            self.run_current_file()

    def stop_debugging(self):
        """Stop debugging session"""
        if hasattr(self, 'debug_manager'):
            self.debug_manager.stop_debugging()
            self.statusBar().showMessage("Debugging stopped")

    def run_current_file(self):
        """Run the current file"""
        editor = self.get_current_editor()
        if editor and hasattr(editor, 'current_file'):
            BuildRunner.build_and_run(editor.current_file, self.output_to_terminal)

    def change_theme(self, theme_name):
        """Change editor theme"""
        if theme_name in self.THEMES:
            theme = self.THEMES[theme_name]
            
            # Update main window style
            self.setStyleSheet(f"""
                QMainWindow {{
                    background: {theme['background']};
                }}
            """)
            
            # Update editor style
            editor = self.get_current_editor()
            if editor:
                editor.setStyleSheet(f"""
                    QPlainTextEdit {{
                        background-color: {theme['editor_bg']};
                        color: {theme['editor_text']};
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 10px;
                    }}
                """)
            
            # Update terminal style if it exists
            if hasattr(self, 'terminal_dock'):
                self.terminal_dock.setStyleSheet(f"""
                    QWidget {{
                        background-color: {theme['editor_bg']};
                        color: {theme['editor_text']};
                    }}
                """)
            
            # Save theme preference
            try:
                with open('settings.json', 'r+') as f:
                    settings = json.load(f)
                    settings['theme'] = theme_name
                    f.seek(0)
                    json.dump(settings, f, indent=4)
                    f.truncate()
            except FileNotFoundError:
                with open('settings.json', 'w') as f:
                    json.dump({'theme': theme_name}, f, indent=4)
            except Exception as e:
                print(f"Error saving theme preference: {str(e)}")

    def closeEvent(self, event):
        """Handle window close event"""
        # Check if there are unsaved changes
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                'Save Changes?',
                'Do you want to save changes before closing?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                # Save all unsaved files
                self.save_all_files()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def has_unsaved_changes(self):
        """Check if any open files have unsaved changes"""
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if hasattr(editor, 'document') and editor.document().isModified():
                return True
        return False

    def save_all_files(self):
        """Save all open files"""
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if hasattr(editor, 'current_file'):
                try:
                    with open(editor.current_file, 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    editor.document().setModified(False)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def cleanup_welcome_screen(self):
        """Clean up welcome screen properly"""
        if hasattr(self, 'welcome_page'):
            self.welcome_page.hide()
            if self.welcome_page.parent():
                self.welcome_page.parent().layout().removeWidget(self.welcome_page)
            self.welcome_page.deleteLater()
            delattr(self, 'welcome_page')
            self.welcome_screen_visible = False

    def setup_file_explorer(self):
        """Setup file explorer panel"""
        # Create dock widget for file explorer
        self.explorer_dock = QDockWidget("Explorer", self)
        self.explorer_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Create main widget
        explorer_widget = QWidget()
        layout = QVBoxLayout(explorer_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create header with title and buttons
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 5, 5)
        
        title = QLabel("EXPLORER")
        title.setStyleSheet("color: #6272A4; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Add action buttons with proper icons
        new_file_btn = QPushButton()
        new_file_btn.setIcon(QIcon("res/new-file.png"))
        new_file_btn.setIconSize(QSize(16, 16))
        new_file_btn.setToolTip("New File")
        new_file_btn.clicked.connect(self.create_new_file)
        
        new_folder_btn = QPushButton()
        new_folder_btn.setIcon(QIcon("res/new-folder.png"))
        new_folder_btn.setIconSize(QSize(16, 16))
        new_folder_btn.setToolTip("New Folder")
        new_folder_btn.clicked.connect(self.create_new_folder)
        
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon("res/refresh.png"))
        refresh_btn.setIconSize(QSize(16, 16))
        refresh_btn.setToolTip("Refresh")
        refresh_btn.clicked.connect(self.refresh_explorer)
        
        # Style buttons
        button_style = """
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: rgba(98, 114, 164, 0.3);
            }
        """
        new_file_btn.setStyleSheet(button_style)
        new_folder_btn.setStyleSheet(button_style)
        refresh_btn.setStyleSheet(button_style)
        
        header_layout.addWidget(new_file_btn)
        header_layout.addWidget(new_folder_btn)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header)
        
        # Create custom file system model with icons
        class CustomFileSystemModel(QFileSystemModel):
            def data(self, index, role=Qt.DisplayRole):
                if role == Qt.DecorationRole:
                    info = self.fileInfo(index)
                    if info.isDir():
                        return QIcon("res/folder.png")
                    elif info.suffix() == 'py':
                        return QIcon("res/python-file.png")
                    else:
                        return QIcon("res/file.png")
                return super().data(index, role)
        
        # Create file tree with custom model
        self.file_tree = QTreeView()
        self.file_model = CustomFileSystemModel()
        self.file_model.setRootPath(self.project_path if hasattr(self, 'project_path') else "")
        self.file_tree.setModel(self.file_model)
        
        if hasattr(self, 'project_path'):
            self.file_tree.setRootIndex(self.file_model.index(self.project_path))
        
        # Hide unnecessary columns
        self.file_tree.setHeaderHidden(True)
        self.file_tree.hideColumn(1)  # Size
        self.file_tree.hideColumn(2)  # Type
        self.file_tree.hideColumn(3)  # Date Modified
        
        # Style the tree
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                border: none;
                color: #CCCCCC;
            }
            QTreeView::item {
                padding: 5px;
                border-radius: 3px;
            }
            QTreeView::item:hover {
                background-color: #2A2D2E;
            }
            QTreeView::item:selected {
                background-color: #37373D;
            }
            QTreeView::branch {
                background: transparent;
            }
        """)
        
        # Enable drag and drop
        self.file_tree.setDragEnabled(True)
        self.file_tree.setAcceptDrops(True)
        self.file_tree.setDropIndicatorShown(True)
        self.file_tree.setDragDropMode(QTreeView.InternalMove)
        
        # Add context menu
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_file_context_menu)
        
        # Connect double-click to open files
        self.file_tree.doubleClicked.connect(self.open_file_from_tree)
        
        layout.addWidget(self.file_tree)
        self.explorer_dock.setWidget(explorer_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)

    def show_file_context_menu(self, position):
        """Show context menu for file tree"""
        index = self.file_tree.indexAt(position)
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #252526;
                color: #CCCCCC;
                border: 1px solid #454545;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: #37373D;
            }
        """)
        
        # Add actions
        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        menu.addSeparator()
        
        if index.isValid():
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            
            # Connect actions
            rename_action.triggered.connect(lambda: self.rename_file(index))
            delete_action.triggered.connect(lambda: self.delete_file(index))
        
        new_file_action.triggered.connect(self.create_new_file)
        new_folder_action.triggered.connect(self.create_new_folder)
        
        menu.exec(self.file_tree.viewport().mapToGlobal(position))

    def refresh_explorer(self):
        """Refresh file explorer"""
        if hasattr(self, 'file_model'):
            self.file_model.setRootPath(self.file_model.rootPath())

    def open_file_from_tree(self, index):
        """Open file when double-clicked in tree"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create new tab with file
                editor = self.tab_widget.add_new_tab(os.path.basename(file_path))
                editor.setPlainText(content)
                editor.current_file = file_path
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

# Add these new tool classes
class DevTools:
    def __init__(self, main_window):
        self.main = main_window
        self.setup_tools()

    def setup_tools(self):
        # Add Tools menu items
        tools_menu = self.main.menuBar().addMenu("Developer Tools")
        
        # Code Analysis
        analysis_menu = tools_menu.addMenu("Code Analysis")
        analysis_menu.addAction("Lint Code", self.lint_code)
        analysis_menu.addAction("Format Code", self.format_code)
        analysis_menu.addAction("Check Complexity", self.check_complexity)
        
        # Debugging
        debug_menu = tools_menu.addMenu("Debug")
        debug_menu.addAction("Start Debugger", self.start_debugger)
        debug_menu.addAction("Add Breakpoint", self.add_breakpoint)
        debug_menu.addAction("Step Over", self.step_over)
        
        # Git Integration
        git_menu = tools_menu.addMenu("Git")
        git_menu.addAction("Initialize Repository", self.git_init)
        git_menu.addAction("Stage Changes", self.git_stage)
        git_menu.addAction("Commit", self.git_commit)
        git_menu.addAction("Push", self.git_push)
        
        # Project Tools
        project_menu = tools_menu.addMenu("Project")
        project_menu.addAction("Project Settings", self.project_settings)
        project_menu.addAction("Dependencies", self.manage_dependencies)
        project_menu.addAction("Virtual Environment", self.manage_venv)
        
        # Database Tools
        db_menu = tools_menu.addMenu("Database")
        db_menu.addAction("SQL Console", self.sql_console)
        db_menu.addAction("Database Browser", self.db_browser)
        
        # Testing
        test_menu = tools_menu.addMenu("Testing")
        test_menu.addAction("Run Tests", self.run_tests)
        test_menu.addAction("Coverage Report", self.coverage_report)
        
        # Documentation
        docs_menu = tools_menu.addMenu("Documentation")
        docs_menu.addAction("Generate Docs", self.generate_docs)
        docs_menu.addAction("Preview Markdown", self.preview_markdown)

    # Tool implementations...
    def lint_code(self):
        editor = self.main.get_current_editor()
        if editor:
            # Add pylint integration
            pass

    def format_code(self):
        editor = self.main.get_current_editor()
        if editor:
            # Add black/autopep8 integration
            pass

    # ... (implement other tool methods)

class LanguageSupport:
    COMPILERS = {
        'C': {
            'Windows': {
                'compiler': 'gcc',
                'flags': ['-Wall', '-O2']
            },
            'Linux': {
                'compiler': 'gcc',
                'flags': ['-Wall', '-O2']
            },
            'Darwin': {
                'compiler': 'gcc',
                'flags': ['-Wall', '-O2']
            }  # Added missing closing brace here
        },  # Added missing closing brace here
        'C++': {
            'Windows': {
                'compiler': 'g++',
                'flags': ['-Wall', '-std=c++17', '-O2']
            },
            'Linux': {
                'compiler': 'g++',
                'flags': ['-Wall', '-std=c++17', '-O2']
            },
            'Darwin': {
                'compiler': 'g++',
                'flags': ['-Wall', '-std=c++17', '-O2']
            }
        }
    }
    
    @staticmethod
    def get_compiler_config(language):
        system = platform.system()
        return LanguageSupport.COMPILERS[language][system]

    @staticmethod
    def build_and_run(file_path, output_callback):
        if not file_path:
            output_callback("No file selected")
            return

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        file_base = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_name)[1].lower()

        # Determine language
        language = None
        if ext == '.c':
            language = 'C'
        elif ext in ['.cpp', '.cxx', '.cc']:
            language = 'C++'
        elif ext == '.py':
            language = 'Python'
        elif ext == '.js':
            language = 'JavaScript'

        if not language:
            output_callback(f"Unsupported file type: {ext}")
            return

        # Handle compilation for C/C++
        if language in ['C', 'C++']:
            try:
                config = LanguageSupport.get_compiler_config(language)
                compiler = config['compiler']
                flags = config['flags']

                # Output file name
                output_file = os.path.join(
                    file_dir,
                    f"{file_base}.exe" if platform.system() == 'Windows' else file_base
                )

                # Build command
                cmd = [compiler, *flags, file_path, '-o', output_file]
                
                output_callback(f"Compiling with: {' '.join(cmd)}\n")
                
                # Compile
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=file_dir
                )

                if result.returncode != 0:
                    output_callback(f"Compilation failed:\n{result.stderr}")
                    return

                # Run the compiled program
                output_callback("Running program...\n")
                run_cmd = [output_file]
                result = subprocess.run(
                    run_cmd,
                    capture_output=True,
                    text=True,
                    cwd=file_dir
                )

                if result.stdout:
                    output_callback(result.stdout)
                if result.stderr:
                    output_callback(f"Runtime errors:\n{result.stderr}")

            except Exception as e:
                output_callback(f"Error: {str(e)}")

        # Handle interpreted languages
        elif language == 'Python':
            try:
                cmd = ['python', file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=file_dir)
                if result.stdout:
                    output_callback(result.stdout)
                if result.stderr:
                    output_callback(f"Errors:\n{result.stderr}")
            except Exception as e:
                output_callback(f"Error: {str(e)}")

        elif language == 'JavaScript':
            try:
                cmd = ['node', file_path]
                result = subprocess.run(cmd, captureoutput=True, text=True, cwd=file_dir)
                if result.stdout:
                    output_callback(result.stdout)
                if result.stderr:
                    output_callback(f"Errors:\n{result.stderr}")
            except Exception as e:
                output_callback(f"Error: {str(e)}")

class ProjectManager:
    def __init__(self, main_window):
        self.main = main_window
        self.project_root = None
        self.project_config = {}
        self.setup_project_tools()

    def setup_project_tools(self):
        # Add Project menu items
        project_menu = self.main.menuBar().addMenu("Project")
        
        # Project operations
        project_menu.addAction("New Project", self.new_project)
        project_menu.addAction("Open Project", self.open_project)
        project_menu.addAction("Project Structure", self.show_project_structure)
        
        # Build configurations
        build_menu = project_menu.addMenu("Build Configuration")
        build_menu.addAction("Debug", lambda: self.set_build_config("debug"))
        build_menu.addAction("Release", lambda: self.set_build_config("release"))
        
        # Run configurations
        run_menu = project_menu.addMenu("Run Configuration")
        run_menu.addAction("Configure...", self.configure_run)
        
        # Dependencies
        project_menu.addAction("Manage Dependencies", self.manage_dependencies)

    def new_project(self):
        project_dir = QFileDialog.getExistingDirectory(self.main, "Select Project Directory")
        if project_dir:
            self.project_root = project_dir
            self.create_project_structure()
            self.save_project_config()

    def create_project_structure(self):
        # Create standard project directories
        os.makedirs(os.path.join(self.project_root, "src"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "tests"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "docs"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "build"), exist_ok=True)

    def create_project_files(self):
        # Create project configuration file
        config = {
            "name": os.path.basename(self.project_root),
            "version": "0.1.0",
            "build_config": "debug",
            "dependencies": [],
            "run_config": {
                "main_file": "src/main.py",
                "args": [],
                "env": {}
            }
        }
        
        with open(os.path.join(self.project_root, "project.json"), "w") as f:
            json.dump(config, f, indent=4)

    def open_project(self):
        project_dir = QFileDialog.getExistingDirectory(self.main, "Open Project")
        if project_dir:
            self.project_root = project_dir
            self.load_project_config()

    def show_project_structure(self):
        if self.project_root:
            dialog = QDialog(self.main)
            dialog.setWindowTitle("Project Structure")
            layout = QVBoxLayout(dialog)
            
            tree = QTreeWidget()
            tree.setHeaderLabels(["Name", "Type"])
            self.populate_project_tree(tree, self.project_root)
            layout.addWidget(tree)
            
            dialog.exec()

    def set_build_config(self, config):
        if self.project_root:
            self.project_config["build_config"] = config
            self.save_project_config()

    def configure_run(self):
        if self.project_root:
            dialog = QDialog(self.main)
            dialog.setWindowTitle("Run Configuration")
            layout = QFormLayout(dialog)
            
            main_file = QLineEdit(self.project_config.get("run_config", {}).get("main_file", ""))
            layout.addRow("Main File:", main_file)
            
            args = QLineEdit(" ".join(self.project_config.get("run_config", {}).get("args", [])))
            layout.addRow("Arguments:", args)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            if dialog.exec():
                self.project_config.setdefault("run_config", {})
                self.project_config["run_config"]["main_file"] = main_file.text()
                self.project_config["run_config"]["args"] = args.text().split()
                self.save_project_config()

    def manage_dependencies(self):
        if self.project_root:
            dialog = QDialog(self.main)
            dialog.setWindowTitle("Manage Dependencies")
            layout = QVBoxLayout(dialog)
            
            deps_list = QListWidget()
            deps_list.addItems(self.project_config.get("dependencies", []))
            layout.addWidget(deps_list)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            if dialog.exec():
                self.project_config["dependencies"] = [deps_list.item(i).text() 
                                                     for i in range(deps_list.count())]
                self.save_project_config()

    def get_project_tree(self):
        tree = QTreeWidget()
        tree.setHeaderLabels(["Name", "Type"])
        if self.project_root:
            root_item = QTreeWidgetItem([os.path.basename(self.project_root), "Project"])
            tree.addTopLevelItem(root_item)
            self.populate_project_tree(root_item, self.project_root)
        return tree

    def populate_project_tree(self, parent_item, directory):
        try:
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                tree_item = QTreeWidgetItem([item, "Directory" if os.path.isdir(path) else "File"])
                parent_item.addChild(tree_item)
                if os.path.isdir(path):
                    self.populate_project_tree(tree_item, path)
        except Exception as e:
            print(f"Error populating project tree: {str(e)}")

class DebugManager:
    def __init__(self, main_window):
        self.main = main_window
        self.breakpoints = set()
        self.is_debugging = False
        self.debugger = None
        self.setup_debug_tools()

    def setup_debug_tools(self):
        debug_toolbar = QToolBar("Debug")
        self.main.addToolBar(Qt.TopToolBarArea, debug_toolbar)
        
        # Debug actions
        start_debug = QAction("Start Debug", self.main)
        start_debug.triggered.connect(self.start_debugging)
        debug_toolbar.addAction(start_debug)
        
        stop_debug = QAction("Stop", self.main)
        stop_debug.triggered.connect(self.stop_debugging)
        debug_toolbar.addAction(stop_debug)
        
        step_over = QAction("Step Over", self.main)
        step_over.triggered.connect(self.step_over)
        debug_toolbar.addAction(step_over)
        
        step_into = QAction("Step Into", self.main)
        step_into.triggered.connect(self.step_into)
        debug_toolbar.addAction(step_into)
        
        step_out = QAction("Step Out", self.main)
        step_out.triggered.connect(self.step_out)
        debug_toolbar.addAction(step_out)

    def toggle_breakpoint(self):
        editor = self.main.get_current_editor()
        if editor:
            line_number = editor.textCursor().blockNumber()
            if line_number in self.breakpoints:
                self.breakpoints.remove(line_number)
            else:
                self.breakpoints.add(line_number)
            editor.update()  # Refresh to show/hide breakpoint marker

    def start_debugging(self):
        if not self.is_debugging:
            self.is_debugging = True
            editor = self.main.get_current_editor()
            if editor and hasattr(editor, 'current_file'):
                # Initialize debugger
                self.main.statusBar().showMessage("Debugging started")

    def stop_debugging(self):
        if self.is_debugging:
            self.is_debugging = False
            self.main.statusBar().showMessage("Debugging stopped")

    def step_over(self):
        if self.is_debugging:
            self.main.statusBar().showMessage("Step over")

    def step_into(self):
        if self.is_debugging:
            self.main.statusBar().showMessage("Step into")

    def step_out(self):
        if self.is_debugging:
            self.main.statusBar().showMessage("Step out")

    def get_debug_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add debug controls
        variables_list = QTreeWidget()
        variables_list.setHeaderLabels(["Name", "Value", "Type"])
        layout.addWidget(variables_list)
        
        # Add call stack
        call_stack = QListWidget()
        layout.addWidget(call_stack)
        
        return widget

class GitManager:
    def __init__(self, main_window):
        self.main = main_window
        self.setup_git_tools()

    def setup_git_tools(self):
        git_toolbar = QToolBar("Git")
        self.main.addToolBar(Qt.TopToolBarArea, git_toolbar)
        
        # Git actions
        commit = QAction("Commit", self.main)
        commit.triggered.connect(self.commit_changes)
        git_toolbar.addAction(commit)
        
        push = QAction("Push", self.main)
        push.triggered.connect(self.push_changes)
        git_toolbar.addAction(push)
        
        pull = QAction("Pull", self.main)
        pull.triggered.connect(self.pull_changes)
        git_toolbar.addAction(pull)
        
        branch = QAction("Branch", self.main)
        branch.triggered.connect(self.manage_branches)
        git_toolbar.addAction(branch)

    def commit_changes(self):
        dialog = GitCommitDialog(self.main)
        if dialog.exec():
            message = dialog.commit_message.toPlainText()
            try:
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', message], check=True)
                self.main.statusBar().showMessage("Changes committed successfully")
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self.main, "Git Error", str(e))

    def push_changes(self):
        try:
            subprocess.run(['git', 'push'], check=True)
            self.main.statusBar().showMessage("Changes pushed successfully")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.main, "Git Error", str(e))

    def pull_changes(self):
        try:
            subprocess.run(['git', 'pull'], check=True)
            self.main.statusBar().showMessage("Changes pulled successfully")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.main, "Git Error", str(e))

    def manage_branches(self):
        try:
            result = subprocess.run(['git', 'branch'], capture_output=True, text=True, check=True)
            branches = result.stdout.splitlines()
            current_branch = next((b[2:] for b in branches if b.startswith('* ')), None)
            
            dialog = QDialog(self.main)
            dialog.setWindowTitle("Git Branches")
            layout = QVBoxLayout(dialog)
            
            branch_list = QListWidget()
            branch_list.addItems(b[2:] if b.startswith('* ') else b.strip() for b in branches)
            layout.addWidget(branch_list)
            
            buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            if dialog.exec():
                selected = branch_list.currentItem()
                if selected and selected.text() != current_branch:
                    subprocess.run(['git', 'checkout', selected.text()], check=True)
                    self.main.statusBar().showMessage(f"Switched to branch {selected.text()}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.main, "Git Error", str(e))

    def get_git_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Git status
        status_list = QTreeWidget()
        status_list.setHeaderLabels(["File", "Status"])
        layout.addWidget(status_list)
        
        # Commit history
        history_list = QTreeWidget()
        history_list.setHeaderLabels(["Commit", "Author", "Date", "Message"])
        layout.addWidget(history_list)
        
        # Branch info
        branch_label = QLabel("Current Branch: ")
        layout.addWidget(branch_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_git_panel)
        button_layout.addWidget(refresh_button)
        
        fetch_button = QPushButton("Fetch")
        fetch_button.clicked.connect(self.fetch_changes)
        button_layout.addWidget(fetch_button)
        
        layout.addLayout(button_layout)
        
        return widget

    def refresh_git_panel(self):
        try:
            # Get git status
            status = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True, check=True)
            # Get current branch
            branch = subprocess.run(['git', 'branch', '--show-current'],
                                  capture_output=True, text=True, check=True)
            self.main.statusBar().showMessage(f"On branch: {branch.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self.main, "Git Warning", str(e))

    def fetch_changes(self):
        try:
            subprocess.run(['git', 'fetch'], check=True)
            self.main.statusBar().showMessage("Fetched changes from remote")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.main, "Git Error", str(e))

class GitCommitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Commit Changes")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Commit message input
        self.commit_message = QPlainTextEdit()
        self.commit_message.setPlaceholderText("Enter commit message...")
        layout.addWidget(self.commit_message)
        
        # Changed files list
        self.files_list = QListWidget()
        try:
            result = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                self.files_list.addItem(line)
        except subprocess.CalledProcessError:
            self.files_list.addItem("Error getting git status")
        
        layout.addWidget(self.files_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Pylight IDE")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add logo
        logo_label = QLabel()
        logo = QPixmap("res/Pyide.png")  # Changed from Pyide.ico
        scaled_logo = logo.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        layout.addWidget(logo_label)
        
        # Add title
        title = QLabel("Pylight IDE")
        title.setAlignment(Qt.AlignCenter)
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Add version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Add description
        description = QLabel(
            "A modern, feature-rich IDE for Python, C/C++, and more.\n"
            "Built with PySide6 and love for coding."
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

class SplashScreen(QSplashScreen):
    def __init__(self):
        # Create a larger, more professional splash screen
        pixmap = QPixmap(800, 500)
        pixmap.fill(QColor("#1E1F29"))  # Darker background
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Initialize progress
        self.progress = 0
        self.max_progress = 100
        
        # Create gradient effect
        self.gradient = QLinearGradient(0, 0, self.width(), 0)
        self.gradient.setColorAt(0, QColor("#BD93F9"))
        self.gradient.setColorAt(1, QColor("#FF79C6"))
        
        # Load and scale logo
        logo = QPixmap("res/Pyide.png")  # Changed from Pyide.ico
        self.logo = logo.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Setup animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_progress)
        self.animation_timer.start(50)  # Update every 50ms
        
        # Initialize loading state
        self.current_state = 0
        self.loading_states = [
            "Initializing core components...",
            "Loading syntax highlighter...",
            "Setting up development environment...",
            "Configuring workspace...",
            "Loading project templates...",
            "Initializing git integration...",
            "Setting up debugging tools...",
            "Loading language servers...",
            "Preparing IDE features...",
            "Starting Pylight IDE..."
        ]

    def drawContents(self, painter):
        # Draw background with subtle gradient
        painter.fillRect(self.rect(), QColor("#1E1F29"))
        
        # Draw logo
        logo_x = (self.width() - self.logo.width()) // 2
        logo_y = 50
        painter.drawPixmap(logo_x, logo_y, self.logo)
        
        # Draw title
        font = QFont("Segoe UI", 36, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(self.gradient, 2))
        title_rect = QRect(0, logo_y + self.logo.height() + 20, self.width(), 50)
        painter.drawText(title_rect, Qt.AlignCenter, "Pylight IDE")
        
        # Draw version
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(QColor("#6272A4"))
        version_rect = QRect(0, title_rect.bottom() + 10, self.width(), 30)
        painter.drawText(version_rect, Qt.AlignCenter, "Version 1.0.0")
        
        # Draw loading message
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(QColor("#F8F8F2"))
        message_rect = QRect(50, self.height() - 150, self.width() - 100, 30)
        current_message = self.loading_states[min(self.current_state, len(self.loading_states) - 1)]
        painter.drawText(message_rect, Qt.AlignLeft, current_message)
        
        # Draw progress bar
        progress_height = 4
        progress_width = self.width() - 100
        progress_x = 50
        progress_y = self.height() - 100
        
        # Draw progress bar background
        painter.fillRect(progress_x, progress_y, progress_width, progress_height, 
                        QColor("#44475A"))
        
        # Draw progress bar
        progress_fill_width = int(progress_width * (self.progress / self.max_progress))
        progress_gradient = QLinearGradient(progress_x, 0, progress_x + progress_width, 0)
        progress_gradient.setColorAt(0, QColor("#BD93F9"))
        progress_gradient.setColorAt(1, QColor("#FF79C6"))
        painter.fillRect(progress_x, progress_y, progress_fill_width, progress_height, 
                        progress_gradient)
        
        # Draw percentage
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor("#6272A4"))
        percentage_rect = QRect(0, progress_y + 10, self.width(), 20)
        painter.drawText(percentage_rect, Qt.AlignCenter, f"{int(self.progress)}%")

    def update_progress(self):
        self.progress += 1
        if self.progress > self.max_progress:
            self.animation_timer.stop()
            return
            
        # Update loading state based on progress
        self.current_state = int((self.progress / self.max_progress) * len(self.loading_states))
        self.repaint()

# Add this new class for the welcome page
class WelcomePage(QWidget):
    project_opened = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet(f"""
            QWidget#WelcomePage {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {EDITOR_COLORS['background']},
                    stop: 1 #2C1F4A
                );
            }}
            QLabel#WelcomeTitle {{
                color: {EDITOR_COLORS['text']};
                font-size: 36px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QLabel#WelcomeSubtitle {{
                color: {EDITOR_COLORS['comments']};
                font-size: 18px;
                font-family: 'Segoe UI';
            }}
            QPushButton#ActionButton {{
                background: rgba(68, 71, 90, 0.5);
                border: 1px solid {EDITOR_COLORS['comments']}40;
                border-radius: 15px;
                padding: 15px;
                color: {EDITOR_COLORS['text']};
                font-family: 'Segoe UI';
            }}
            QPushButton#ActionButton:hover {{
                background: rgba(98, 114, 164, 0.6);
                border: 1px solid {EDITOR_COLORS['keywords']}80;
            }}
            QGroupBox {{
                background: rgba(40, 42, 54, 0.5);
                border: 1px solid {EDITOR_COLORS['comments']}40;
                border-radius: 15px;
                padding: 20px;
                margin-top: 30px;
            }}
            QGroupBox::title {{
                color: {EDITOR_COLORS['keywords']};
                padding: 0 15px;
                subcontrol-position: top center;
            }}
        """)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Header with gradient background
        header = QWidget()
        header.setObjectName("HeaderSection")
        header.setStyleSheet(f"""
            #HeaderSection {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {EDITOR_COLORS['background']},
                    stop: 1 #2C1F4A
                );
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
            }}
        """)
        header_layout = QVBoxLayout(header)

        # Logo and title section
        logo_title = QHBoxLayout()
        
        # Logo with glow effect
        logo_label = QLabel()
        logo = QPixmap("res/Pyide.png")
        scaled_logo = logo.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_title.addWidget(logo_label)

        # Title section with gradient text
        title_section = QVBoxLayout()
        title = QLabel("Welcome to Pylight IDE")
        title.setObjectName("WelcomeTitle")
        subtitle = QLabel("A Modern Development Environment")
        subtitle.setObjectName("WelcomeSubtitle")
        
        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        title_section.addStretch()
        
        logo_title.addLayout(title_section)
        logo_title.addStretch()
        
        header_layout.addLayout(logo_title)

        # Quick action buttons with glass effect
        actions = QHBoxLayout()
        actions.setSpacing(20)
        
        # Create action buttons with modern design
        new_project = self.create_action_button(
            "New Project",
            "Start a fresh project",
            "Ctrl+Shift+N",
            self.new_file,
            "project"
        )
        open_project = self.create_action_button(
            "Open Project",
            "Open existing project",
            "Ctrl+O",
            self.open_file,
            "folder"
        )
        clone_repo = self.create_action_button(
            "Clone Repository",
            "Clone from Git",
            "Ctrl+Shift+G",
            self.clone_repo,
            "git"
        )
        
        actions.addWidget(new_project)
        actions.addWidget(open_project)
        actions.addWidget(clone_repo)
        
        header_layout.addLayout(actions)
        main_layout.addWidget(header)

        # Main content area with glass panels
        content = QHBoxLayout()
        
        # Recent projects panel
        recent_panel = QGroupBox("Recent Projects")
        recent_layout = QVBoxLayout(recent_panel)
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
            QListWidget::item {{
                background: rgba(68, 71, 90, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
                color: {EDITOR_COLORS['text']};
            }}
            QListWidget::item:hover {{
                background: rgba(98, 114, 164, 0.4);
            }}
            QListWidget::item:selected {{
                background: rgba(98, 114, 164, 0.6);
                border: 1px solid {EDITOR_COLORS['keywords']}80;
            }}
        """)
        recent_layout.addWidget(self.recent_list)
        content.addWidget(recent_panel)

        # Getting Started panel with features
        started_panel = QGroupBox("Getting Started")
        started_layout = QGridLayout(started_panel)
        
        features = [
            ("🚀 Quick Setup", "Set up your development environment in minutes"),
            ("🛠 Multiple Languages", "Support for Python, C++, Java, and more"),
            ("🔍 Smart Features", "Intelligent code completion and syntax highlighting"),
            ("⚡ Fast Performance", "Optimized for speed and efficiency"),
            ("🎨 Customizable", "Themes and extensions support"),
            ("🔧 Built-in Tools", "Debugger, terminal, and Git integration")
        ]
        
        for i, (title, desc) in enumerate(features):
            feature = self.create_feature_widget(title, desc)
            started_layout.addWidget(feature, i // 2, i % 2)
        
        content.addWidget(started_panel)
        main_layout.addLayout(content)

        # Learn more section with gradient buttons
        learn_more = self.create_learn_more_section()
        main_layout.addWidget(learn_more)

    def create_feature_widget(self, title, description):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['keywords']};
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['comments']};
            font-size: 14px;
            padding: 5px;
        """)
        desc_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        widget.setStyleSheet(f"""
            QWidget {{
                background: rgba(40, 42, 54, 0.3);
                border-radius: 10px;
                padding: 10px;
            }}
            QWidget:hover {{
                background: rgba(68, 71, 90, 0.4);
                border: 1px solid {EDITOR_COLORS['comments']}40;
            }}
        """)
        
        return widget

    def create_learn_more_section(self):
        section = QWidget()
        layout = QHBoxLayout(section)
        layout.setSpacing(20)
        
        links = [
            ("Documentation", self.open_docs),
            ("Video Tutorials", self.open_tutorials),
            ("Community Forum", self.join_community),
            ("Report Issues", self.report_issues)
        ]
        
        for text, callback in links:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 {EDITOR_COLORS['keywords']}80,
                        stop: 1 {EDITOR_COLORS['functions']}80
                    );
                    border: none;
                    border-radius: 10px;
                    padding: 12px 25px;
                    color: {EDITOR_COLORS['text']};
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 {EDITOR_COLORS['keywords']},
                        stop: 1 {EDITOR_COLORS['functions']}
                    );
                }}
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        return section

    def create_action_button(self, title, tooltip, shortcut, callback, icon_name=None):
        """Create a more attractive action button with icon"""
        btn = QPushButton(title)
        btn.setObjectName("ActionButton")
        
        # Create layout for button content
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Add icon if provided
        if icon_name:
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(f"res/{icon_name}.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(icon_label)
        
        # Add text and description
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #F8F8F2;")
        desc_label = QLabel(tooltip)
        desc_label.setStyleSheet("font-size: 12px; color: #6272A4;")
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Add shortcut label
        if shortcut:
            shortcut_label = QLabel(shortcut)
            shortcut_label.setStyleSheet("color: #6272A4; font-size: 12px;")
            layout.addWidget(shortcut_label)
        
        btn.clicked.connect(callback)
        btn.setMinimumWidth(250)
        btn.setMinimumHeight(70)
        
        return btn

    def new_file(self):
        """Handle new project creation"""
        dialog = NewProjectDialog(self)
        if dialog.exec():
            project_info = dialog.get_project_info()
            if project_info:
                self.create_new_project(project_info)

    def create_new_project(self, project_info):
        """Create a new project with the given information"""
        try:
            # Create project directory
            project_path = os.path.join(project_info['location'], project_info['name'])
            os.makedirs(project_path, exist_ok=True)
            
            # Create project structure
            os.makedirs(os.path.join(project_path, 'src'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'docs'), exist_ok=True)
            
            # Create initial files based on template
            self.create_project_files(project_path, project_info)
            
            # Emit signal to open the project
            self.project_opened.emit(project_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")

    def open_file(self):
        """Handle opening existing project"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Project",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.project_opened.emit(folder)

    def clone_repo(self):
        """Handle repository cloning"""
        dialog = CloneRepoDialog(self)
        if dialog.exec():
            repo_url, target_dir = dialog.get_repo_info()
            if repo_url and target_dir:
                self.clone_repository(repo_url, target_dir)

    def clone_repository(self, repo_url, target_dir):
        """Clone a git repository"""
        try:
            # Show progress dialog
            progress = QProgressDialog("Cloning repository...", "Cancel", 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            # Clone repository in a separate thread
            thread = GitCloneThread(repo_url, target_dir)
            thread.finished.connect(progress.close)
            thread.error.connect(self.handle_clone_error)
            thread.success.connect(lambda: self.project_opened.emit(target_dir))
            thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to clone repository: {str(e)}")

    def handle_clone_error(self, error_msg):
        QMessageBox.critical(self, "Clone Error", error_msg)

    def create_recent_projects_section(self):
        """Create an enhanced recent projects section"""
        section = self.create_section_widget("Recent Projects")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Add recent projects list
        self.recent_projects_list = QListWidget()
        self.recent_projects_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                background: rgba(40, 42, 54, 0.3);
                border-radius: 5px;
                margin: 5px 0;
                padding: 0;
            }
            QListWidget::item:hover {
                background: rgba(68, 71, 90, 0.5);
            }
        """)
        self.recent_projects_list.itemDoubleClicked.connect(self.open_recent_project)
        
        # Load and display recent projects
        self.load_recent_projects()
        
        layout.addWidget(self.recent_projects_list)
        section.layout().addLayout(layout)
        return section

    def loadrecent_projects(self):
        """Load recent projects from settings"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                recent_projects = settings.get('recent_projects', [])
                
                self.recent_projects_list.clear()
                
                for project in recent_projects:
                    if os.path.exists(project['path']):
                        item_widget = self.create_recent_project_item(project)
                        item = QListWidgetItem(self.recent_projects_list)
                        item.setSizeHint(item_widget.sizeHint())
                        self.recent_projects_list.setItemWidget(item, item_widget)
                        
        except FileNotFoundError:
            with open('settings.json', 'w') as f:
                json.dump({'recent_projects': []}, f)
        except Exception as e:
            print(f"Error loading recent projects: {str(e)}")

    def create_recent_project_item(self, project):
        """Create a widget for a recent project item"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)

        # Project icon
        icon_label = QLabel()
        icon = QPixmap("res/folder.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon)
        layout.addWidget(icon_label)

        # Project info
        info_layout = QVBoxLayout()
        
        name_label = QLabel(project['name'])
        name_label.setStyleSheet("""
            color: #F8F8F2;
            font-size: 14px;
            font-weight: bold;
        """)
        
        path_label = QLabel(project['path'])
        path_label.setStyleSheet("""
            color: #6272A4;
            font-size: 12px;
        """)
        
        last_opened = project.get('last_opened', 'Never')
        time_label = QLabel(f"Last opened: {last_opened}")
        time_label.setStyleSheet("color: #6272A4; font-size: 11px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(path_label)
        info_layout.addWidget(time_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open")
        open_btn.setStyleSheet("""
            QPushButton {
                background: #50FA7B;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                color: #282A36;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #69FF94;
            }
        """)
        open_btn.clicked.connect(lambda: self.open_project(project['path']))
        
        remove_btn = QPushButton("×")
        remove_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 85, 85, 0.5);
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                color: #F8F8F2;
            }
            QPushButton:hover {
                background: rgba(255, 85, 85, 0.8);
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_recent_project(project))
        
        button_layout.addWidget(open_btn)
        button_layout.addWidget(remove_btn)
        layout.addLayout(button_layout)

        return widget

    def open_recent_project(self, item):
        """Handle double-click on recent project"""
        widget = self.recent_projects_list.itemWidget(item)
        if widget:
            path_label = widget.findChild(QLabel)
            if path_label:
                path = path_label.text()
                self.open_project(path)

    def open_project(self, project_path):
        """Open a project and update recent projects"""
        if os.path.exists(project_path):
            self.project_path = project_path
            self.welcome_page.add_to_recent_projects(project_path)
            self.show_editor_interface()
            self.setup_project_explorer()
            
            # Update window title
            project_name = os.path.basename(project_path)
            self.setWindowTitle(f"Pylight IDE - {project_name}")
            
            # Show success message
            self.statusBar().showMessage(f"Opened project: {project_name}")
        else:
            QMessageBox.warning(
                self,
                "Project Not Found",
                f"The project directory no longer exists:\n{project_path}"
            )

    def update_recent_project(self, path):
        """Update last opened time for a project"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            recent_projects = settings.get('recent_projects', [])
            
            # Update or add project
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            updated = False
            
            for project in recent_projects:
                if project['path'] == path:
                    project['last_opened'] = now
                    updated = True
                    break
            
            if not updated:
                recent_projects.insert(0, {
                    'name': os.path.basename(path),
                    'path': path,
                    'last_opened': now
                })
            
            # Keep only last 10 projects
            settings['recent_projects'] = recent_projects[:10]
            
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
                
            # Reload the list
            self.load_recent_projects()
            
        except Exception as e:
            print(f"Error updating recent project: {str(e)}")

    def remove_recent_project(self, project):
        """Remove a project from recent projects"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            recent_projects = settings.get('recent_projects', [])
            settings['recent_projects'] = [
                p for p in recent_projects if p['path'] != project['path']
            ]
            
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            
            # Reload the list
            self.load_recent_projects()
            
        except Exception as e:
            print(f"Error removing recent project: {str(e)}")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Main content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # Header with gradient background
        header = QWidget()
        header.setObjectName("HeaderSection")
        header.setStyleSheet(f"""
            #HeaderSection {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {EDITOR_COLORS['background']},
                    stop: 1 #2C1F4A
                );
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
            }}
        """)
        header_layout = QVBoxLayout(header)

        # Logo and title section
        logo_title = QHBoxLayout()
        
        # Logo with glow effect
        logo_label = QLabel()
        logo = QPixmap("res/Pyide.png")
        scaled_logo = logo.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_title.addWidget(logo_label)

        # Title section with gradient text
        title_section = QVBoxLayout()
        title = QLabel("Welcome to Pylight IDE")
        title.setObjectName("WelcomeTitle")
        subtitle = QLabel("A Modern Development Environment")
        subtitle.setObjectName("WelcomeSubtitle")
        
        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        title_section.addStretch()
        
        logo_title.addLayout(title_section)
        logo_title.addStretch()
        
        header_layout.addLayout(logo_title)

        # Quick action buttons with glass effect
        actions = QHBoxLayout()
        actions.setSpacing(20)
        
        # Create action buttons with modern design
        new_project = self.create_action_button(
            "New Project",
            "Start a fresh project",
            "Ctrl+Shift+N",
            self.new_file,
            "project"
        )
        open_project = self.create_action_button(
            "Open Project",
            "Open existing project",
            "Ctrl+O",
            self.open_file,
            "folder"
        )
        clone_repo = self.create_action_button(
            "Clone Repository",
            "Clone from Git",
            "Ctrl+Shift+G",
            self.clone_repo,
            "git"
        )
        
        actions.addWidget(new_project)
        actions.addWidget(open_project)
        actions.addWidget(clone_repo)
        
        header_layout.addLayout(actions)
        main_layout.addWidget(header)

        # Main content area with glass panels
        content = QHBoxLayout()
        
        # Recent projects panel
        recent_panel = QGroupBox("Recent Projects")
        recent_layout = QVBoxLayout(recent_panel)
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
            QListWidget::item {{
                background: rgba(68, 71, 90, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
                color: {EDITOR_COLORS['text']};
            }}
            QListWidget::item:hover {{
                background: rgba(98, 114, 164, 0.4);
            }}
            QListWidget::item:selected {{
                background: rgba(98, 114, 164, 0.6);
                border: 1px solid {EDITOR_COLORS['keywords']}80;
            }}
        """)
        recent_layout.addWidget(self.recent_list)
        content.addWidget(recent_panel)

        # Getting Started panel with features
        started_panel = QGroupBox("Getting Started")
        started_layout = QGridLayout(started_panel)
        
        features = [
            ("🚀 Quick Setup", "Set up your development environment in minutes"),
            ("🛠 Multiple Languages", "Support for Python, C++, Java, and more"),
            ("🔍 Smart Features", "Intelligent code completion and syntax highlighting"),
            ("⚡ Fast Performance", "Optimized for speed and efficiency"),
            ("🎨 Customizable", "Themes and extensions support"),
            ("🔧 Built-in Tools", "Debugger, terminal, and Git integration")
        ]
        
        for i, (title, desc) in enumerate(features):
            feature = self.create_feature_widget(title, desc)
            started_layout.addWidget(feature, i // 2, i % 2)
        
        content.addWidget(started_panel)
        main_layout.addLayout(content)

        # Learn more section with gradient buttons
        learn_more = self.create_learn_more_section()
        main_layout.addWidget(learn_more)

    def create_feature_widget(self, title, description):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['keywords']};
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['comments']};
            font-size: 14px;
            padding: 5px;
        """)
        desc_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        widget.setStyleSheet(f"""
            QWidget {{
                background: rgba(40, 42, 54, 0.3);
                border-radius: 10px;
                padding: 10px;
            }}
            QWidget:hover {{
                background: rgba(68, 71, 90, 0.4);
                border: 1px solid {EDITOR_COLORS['comments']}40;
            }}
        """)
        
        return widget

    def create_learn_more_section(self):
        section = QWidget()
        layout = QHBoxLayout(section)
        layout.setSpacing(20)
        
        links = [
            ("Documentation", self.open_docs),
            ("Video Tutorials", self.open_tutorials),
            ("Community Forum", self.join_community),
            ("Report Issues", self.report_issues)
        ]
        
        for text, callback in links:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 {EDITOR_COLORS['keywords']}80,
                        stop: 1 {EDITOR_COLORS['functions']}80
                    );
                    border: none;
                    border-radius: 10px;
                    padding: 12px 25px;
                    color: {EDITOR_COLORS['text']};
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 {EDITOR_COLORS['keywords']},
                        stop: 1 {EDITOR_COLORS['functions']}
                    );
                }}
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        return section

    def load_recent_projects(self):
        """Load and display recent projects"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                recent_projects = settings.get('recent_projects', [])
                
                self.recent_list.clear()
                for project in recent_projects:
                    if os.path.exists(project['path']):
                        item = QListWidgetItem()
                        widget = RecentProjectItem(project, self)
                        item.setSizeHint(widget.sizeHint())
                        self.recent_list.addItem(item)
                        self.recent_list.setItemWidget(item, widget)
                        
        except FileNotFoundError:
            with open('settings.json', 'w') as f:
                json.dump({'recent_projects': []}, f)
        except Exception as e:
            print(f"Error loading recent projects: {str(e)}")

    def add_to_recent_projects(self, project_path):
        """Add project to recent projects list"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            recent_projects = settings.get('recent_projects', [])
            
            # Create project entry
            project_entry = {
                'name': os.path.basename(project_path),
                'path': project_path,
                'last_opened': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Remove if already exists
            recent_projects = [p for p in recent_projects if p['path'] != project_path]
            
            # Add to front of list
            recent_projects.insert(0, project_entry)
            
            # Keep only last 10 projects
            settings['recent_projects'] = recent_projects[:10]
            
            # Save settings
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
                
            # Reload the list
            self.load_recent_projects()
            
        except Exception as e:
            print(f"Error adding to recent projects: {str(e)}")

    # Action handlers
    def open_docs(self): 
        QDesktopServices.openUrl(QUrl("https://pylight-ide.readthedocs.io"))

    def open_tutorials(self): 
        QDesktopServices.openUrl(QUrl("https://pylight-ide.readthedocs.io/tutorials"))

    def open_tips(self): 
        QDesktopServices.openUrl(QUrl("https://pylight-ide.readthedocs.io/tips"))

    def join_community(self): 
        QDesktopServices.openUrl(QUrl("https://github.com/pylight-ide/community"))

    # Add these methods to the WelcomePage class
    def report_issues(self):
        """Open the GitHub issues page"""
        QDesktopServices.openUrl(QUrl("https://github.com/pylight-ide/issues"))

    def create_project_files(self, project_path, project_info):
        """Create initial project files based on project type"""
        project_type = project_info['type']
        
        try:
            # Create base directories
            os.makedirs(os.path.join(project_path, 'src'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'docs'), exist_ok=True)
            
            # Create project files based on type
            if project_type == "Python":
                self.create_python_project_files(project_path)
            elif project_type == "C++":
                self.create_cpp_project_files(project_path)
            elif project_type == "Java":
                self.create_java_project_files(project_path)
            elif project_type == "Web":
                self.create_web_project_files(project_path)
                
        except Exception as e:
            raise Exception(f"Failed to create project files: {str(e)}")

    def create_python_project_files(self, project_path):
        """Create Python project structure"""
        try:
            # Create main.py
            main_file = os.path.join(project_path, 'src', 'main.py')
            os.makedirs(os.path.dirname(main_file), exist_ok=True)
            with open(main_file, 'w') as f:
                f.write('''def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''')
            
            # Create requirements.txt
            with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
                f.write('# Project dependencies\n')
            
            # Create README.md
            with open(os.path.join(project_path, 'README.md'), 'w') as f:
                f.write(f'''# {os.path.basename(project_path)}

A Python project created with Pylight IDE.

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the project:
   ```
   python src/main.py
   ```
''')
            
            # Create .gitignore
            with open(os.path.join(project_path, '.gitignore'), 'w') as f:
                f.write('''# Python
__pycache__/
*.py[cod]
venv/
.env
.idea/
.vscode/
''')

        except Exception as e:
            raise Exception(f"Failed to create Python project files: {str(e)}")

    def create_cpp_project_files(self, project_path):
        """Create C++ project structure"""
        try:
            # Create main.cpp
            main_file = os.path.join(project_path, 'src', 'main.cpp')
            os.makedirs(os.path.dirname(main_file), exist_ok=True)
            with open(main_file, 'w') as f:
                f.write('''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
''')
            
            # Create CMakeLists.txt
            with open(os.path.join(project_path, 'CMakeLists.txt'), 'w') as f:
                project_name = os.path.basename(project_path)
                f.write(f'''cmake_minimum_required(VERSION 3.10)
project({project_name})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(${{PROJECT_NAME}} src/main.cpp)
''')

        except Exception as e:
            raise Exception(f"Failed to create C++ project files: {str(e)}")

    def create_java_project_files(self, project_path):
        """Create Java project structure"""
        try:
            # Create main Java file
            main_file = os.path.join(project_path, 'src', 'Main.java')
            os.makedirs(os.path.dirname(main_file), exist_ok=True)
            with open(main_file, 'w') as f:
                f.write('''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
''')

        except Exception as e:
            raise Exception(f"Failed to create Java project files: {str(e)}")

    def create_web_project_files(self, project_path):
        """Create Web project structure"""
        try:
            # Create directories
            os.makedirs(os.path.join(project_path, 'src', 'css'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'src', 'js'), exist_ok=True)
            
            # Create index.html
            with open(os.path.join(project_path, 'src', 'index.html'), 'w') as f:
                f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Project</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Hello, World!</h1>
    <script src="js/main.js"></script>
</body>
</html>
''')
            
            # Create style.css
            with open(os.path.join(project_path, 'src', 'css', 'style.css'), 'w') as f:
                f.write('''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}
''')
            
            # Create main.js
            with open(os.path.join(project_path, 'src', 'js', 'main.js'), 'w') as f:
                f.write('console.log("Hello from JavaScript!");')

        except Exception as e:
            raise Exception(f"Failed to create Web project files: {str(e)}")

    def create_new_project(self, project_info):
        """Create a new project with the given information"""
        try:
            # Validate project info
            if not project_info.get('name') or not project_info.get('location'):
                raise ValueError("Project name and location are required")

            # Create project directory
            project_path = os.path.join(project_info['location'], project_info['name'])
            if os.path.exists(project_path):
                raise ValueError(f"Project directory already exists: {project_path}")

            # Create base project structure
            os.makedirs(project_path, exist_ok=True)
            
            # Create project files
            self.create_project_files(project_path, project_info)
            
            # Emit signal to open the project
            self.project_opened.emit(project_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Create preview tree before setup_ui
        self.preview_tree = QTreeWidget()
        self.preview_tree.setHeaderLabel("Project Structure")
        
        # Now setup UI
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left side - Project Settings
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(20)
        
        # Project Header
        header = QLabel("Create New Project")
        header.setStyleSheet("""
            font-size: 24px;
            color: #BD93F9;
            font-weight: bold;
            padding: 10px 0;
        """)
        settings_layout.addWidget(header)
        
        # Project Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Project name
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: rgba(40, 42, 54, 0.5);
                border: 1px solid rgba(98, 114, 164, 0.5);
                border-radius: 5px;
                color: #F8F8F2;
            }
        """)
        self.name_input.textChanged.connect(self.update_preview)
        form_layout.addRow("Project Name:", self.name_input)
        
        # Project location
        location_widget = QWidget()
        location_layout = QHBoxLayout(location_widget)
        location_layout.setContentsMargins(0, 0, 0, 0)
        
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: rgba(40, 42, 54, 0.5);
                border: 1px solid rgba(98, 114, 164, 0.5);
                border-radius: 5px;
                color: #F8F8F2;
            }
        """)
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background: rgba(98, 114, 164, 0.5);
                border: none;
                border-radius: 5px;
                color: #F8F8F2;
            }
            QPushButton:hover {
                background: rgba(98, 114, 164, 0.8);
            }
        """)
        browse_btn.clicked.connect(self.browse_location)
        
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_btn)
        form_layout.addRow("Location:", location_widget)
        
        # Project type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Python", "C++", "Java", "Web"])
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background: rgba(40, 42, 54, 0.5);
                border: 1px solid rgba(98, 114, 164, 0.5);
                border-radius: 5px;
                color: #F8F8F2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(res/down-arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.type_combo.currentTextChanged.connect(self.update_preview)
        form_layout.addRow("Project Type:", self.type_combo)
        
        settings_layout.addLayout(form_layout)
        
        # Add template selection
        template_group = QGroupBox("Project Template")
        template_group.setStyleSheet("""
            QGroupBox {
                background: rgba(40, 42, 54, 0.3);
                border: 1px solid rgba(98, 114, 164, 0.3);
                border-radius: 5px;
                margin-top: 15px;
                padding: 15px;
            }
            QGroupBox::title {
                color: #BD93F9;
                padding: 0 10px;
            }
        """)
        template_layout = QVBoxLayout(template_group)
        
        self.template_list = QListWidget()
        self.template_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                margin: 2px 0;
                border-radius: 5px;
                color: #F8F8F2;
            }
            QListWidget::item:selected {
                background: rgba(98, 114, 164, 0.5);
            }
            QListWidget::item:hover {
                background: rgba(68, 71, 90, 0.5);
            }
        """)
        self.update_templates()
        template_layout.addWidget(self.template_list)
        
        settings_layout.addWidget(template_group)
        settings_layout.addStretch()
        
        # Right side - Preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        preview_label = QLabel("Project Preview")
        preview_label.setStyleSheet("""
            font-size: 18px;
            color: #50FA7B;
            font-weight: bold;
            padding: 10px 0;
        """)
        preview_layout.addWidget(preview_label)
        
        self.preview_tree = QTreeWidget()
        self.preview_tree.setHeaderLabel("Project Structure")
        self.preview_tree.setStyleSheet("""
            QTreeWidget {
                background: rgba(40, 42, 54, 0.3);
                border: 1px solid rgba(98, 114, 164, 0.3);
                border-radius: 5px;
                color: #F8F8F2;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background: rgba(98, 114, 164, 0.5);
            }
        """)
        preview_layout.addWidget(self.preview_tree)
        
        # Add buttons at the bottom
        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Project")
        create_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: #50FA7B;
                border: none;
                border-radius: 5px;
                color: #282A36;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #69FF94;
            }
        """)
        create_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: rgba(98, 114, 164, 0.5);
                border: none;
                border-radius: 5px;
                color: #F8F8F2;
            }
            QPushButton:hover {
                background: rgba(98, 114, 164, 0.8);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(create_btn)
        
        # Add all widgets to main layout
        main_layout.addWidget(settings_widget, stretch=1)
        preview_layout.addLayout(button_layout)
        main_layout.addWidget(preview_widget, stretch=1)

    def update_templates(self):
        """Update template list based on selected project type"""
        self.template_list.clear()
        project_type = self.type_combo.currentText()
        
        templates = {
            "Python": ["Empty Project", "Basic Application", "Web Application (Flask)", "GUI Application (Qt)"],
            "C++": ["Empty Project", "Console Application", "GUI Application (Qt)", "Library Project"],
            "Java": ["Empty Project", "Console Application", "GUI Application (Swing)", "Spring Boot Application"],
            "Web": ["Empty Project", "HTML/CSS/JS", "React Application", "Vue.js Application"]
        }
        
        self.template_list.addItems(templates.get(project_type, []))
        self.template_list.setCurrentRow(0)
        self.update_preview()

    def update_preview(self):
        """Update project structure preview"""
        self.preview_tree.clear()
        if not self.name_input.text():
            return
            
        root = QTreeWidgetItem([self.name_input.text()])
        self.preview_tree.addTopLevelItem(root)
        
        # Add basic structure
        src = QTreeWidgetItem(root, ["src"])
        tests = QTreeWidgetItem(root, ["tests"])
        docs = QTreeWidgetItem(root, ["docs"])
        
        # Add project-type specific files
        project_type = self.type_combo.currentText()
        if project_type == "Python":
            QTreeWidgetItem(src, ["main.py"])
            QTreeWidgetItem(root, ["requirements.txt"])
            QTreeWidgetItem(root, ["README.md"])
            QTreeWidgetItem(root, [".gitignore"])
        elif project_type == "C++":
            QTreeWidgetItem(src, ["main.cpp"])
            QTreeWidgetItem(root, ["CMakeLists.txt"])
            QTreeWidgetItem(root, ["README.md"])
        elif project_type == "Java":
            QTreeWidgetItem(src, ["Main.java"])
            QTreeWidgetItem(root, ["pom.xml"])
            QTreeWidgetItem(root, ["README.md"])
        elif project_type == "Web":
            QTreeWidgetItem(src, ["index.html"])
            css = QTreeWidgetItem(src, ["css"])
            QTreeWidgetItem(css, ["style.css"])
            js = QTreeWidgetItem(src, ["js"])
            QTreeWidgetItem(js, ["main.js"])
            QTreeWidgetItem(root, ["README.md"])
        
        root.setExpanded(True)
        src.setExpanded(True)

    def browse_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Location")
        if folder:
            self.location_input.setText(folder)
            self.update_preview()

    def get_project_info(self):
        return {
            'name': self.name_input.text(),
            'location': self.location_input.text(),
            'type': self.type_combo.currentText(),
            'template': self.template_list.currentItem().text() if self.template_list.currentItem() else "Empty Project"
        }

class CloneRepoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clone Repository")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Repository URL
        self.url_input = QLineEdit()
        layout.addWidget(QLabel("Repository URL:"))
        layout.addWidget(self.url_input)
        
        # Target directory
        target_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_target)
        target_layout.addWidget(self.target_input)
        target_layout.addWidget(browse_btn)
        
        layout.addWidget(QLabel("Target Directory:"))
        layout.addLayout(target_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def browse_target(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if folder:
            self.target_input.setText(folder)

    def get_repo_info(self):
        return (self.url_input.text(), self.target_input.text())

class GitCloneThread(QThread):
    finished = Signal()
    error = Signal(str)
    success = Signal()

    def __init__(self, repo_url, target_dir):
        super().__init__()
        self.repo_url = repo_url
        self.target_dir = target_dir

    def run(self):
        try:
            import git
            git.Repo.clone_from(self.repo_url, self.target_dir)
            self.success.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

# Add new RunTerminal class for interactive I/O
class RunTerminal(QDialog):
    def __init__(self, process, output_callback, parent=None):
        super().__init__(parent)
        self.process = process
        self.output_callback = output_callback
        self.setup_ui()
        self.start_io_handlers()
        
        # Set window properties
        self.setWindowTitle("Program Output")
        self.setModal(True)  # Make the dialog modal
        self.resize(800, 600)  # Set a reasonable default size

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Output display
        self.output_display = QPlainTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: none;
                font-family: 'Consolas';
                padding: 5px;
            }
        """)
        layout.addWidget(self.output_display)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas';
            }
        """)
        self.input_line.returnPressed.connect(self.send_input)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_input)
        
        input_layout.addWidget(QLabel("Input:"))
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        stop_button = QPushButton("Stop Program")
        stop_button.clicked.connect(self.stop_program)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        
        button_layout.addWidget(stop_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def start_io_handlers(self):
        # Start output reader thread
        self.output_thread = QThread()
        self.output_worker = OutputWorker(self.process)
        self.output_worker.moveToThread(self.output_thread)
        self.output_worker.output_received.connect(self.handle_output)
        self.output_thread.started.connect(self.output_worker.run)
        self.output_thread.start()

    def handle_output(self, text):
        self.output_display.appendPlainText(text)
        self.output_callback(text)

    def send_input(self):
        if self.input_line.text():
            try:
                text = self.input_line.text() + '\n'
                self.process.stdin.write(text)
                self.process.stdin.flush()
                self.output_display.appendPlainText(f"> {text.strip()}")
                self.input_line.clear()
            except Exception as e:
                self.output_display.appendPlainText(f"Error sending input: {str(e)}")

    def stop_program(self):
        try:
            self.process.terminate()
            self.output_display.appendPlainText("\nProgram terminated by user.")
        except Exception as e:
            self.output_display.appendPlainText(f"\nError terminating program: {str(e)}")

    def closeEvent(self, event):
        try:
            if self.process.poll() is None:  # If process is still running
                self.process.terminate()  # Try to terminate it gracefully
                self.process.wait(timeout=1)  # Wait for it to finish
        except Exception:
            try:
                self.process.kill()  # Force kill if terminate doesn't work
            except Exception:
                pass
        
        if hasattr(self, 'output_thread'):
            self.output_thread.quit()
            self.output_thread.wait()
        
        event.accept()

# Add OutputWorker class for handling program output
class OutputWorker(QObject):
    output_received = Signal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self):
        while True:
            output = self.process.stdout.readline()
            if output:
                self.output_received.emit(output.strip())
            error = self.process.stderr.readline()
            if error:
                self.output_received.emit("Error: " + error.strip())
            
            if not output and not error and self.process.poll() is not None:
                self.output_received.emit("\nProgram finished with exit code: " + 
                                       str(self.process.returncode))
                break

# Add BuildRunPanel class to handle build and run actions
class BuildRunPanel(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Build & Run", parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Toolbar
        toolbar = QHBoxLayout()
        
        # Build configuration
        self.config_combo = QComboBox()
        self.config_combo.addItems(["Debug", "Release"])
        self.config_combo.setStyleSheet("""
            QComboBox {
                background: rgba(68, 71, 90, 0.7);
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: #F8F8F2;
                min-width: 100px;
            }
        """)
        toolbar.addWidget(QLabel("Configuration:"))
        toolbar.addWidget(self.config_combo)
        
        # Build and Run buttons
        build_btn = self.create_button("Build", "F7", self.build)
        run_btn = self.create_button("Run", "F5", self.run)
        build_run_btn = self.create_button("Build & Run", "Ctrl+F5", self.build_and_run)
        stop_btn = self.create_button("Stop", "Shift+F5", self.stop)
        
        toolbar.addWidget(build_btn)
        toolbar.addWidget(run_btn)
        toolbar.addWidget(build_run_btn)
        toolbar.addWidget(stop_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)

        # Output tabs
        self.output_tabs = QTabWidget()
        self.output_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: rgba(40, 42, 54, 0.7);
                color: #F8F8F2;
                padding: 8px 16px;
                border: none;
            }
            QTabBar::tab:selected {
                background: rgba(68, 71, 90, 0.9);
            }
        """)
        
        # Build output
        self.build_output = QPlainTextEdit()
        self.build_output.setReadOnly(True)
        self.setup_output_style(self.build_output)
        self.output_tabs.addTab(self.build_output, "Build")
        
        # Run output
        self.run_output = QPlainTextEdit()
        self.run_output.setReadOnly(True)
        self.setup_output_style(self.run_output)
        self.output_tabs.addTab(self.run_output, "Run")
        
        layout.addWidget(self.output_tabs)
        
        self.setWidget(widget)

    def create_button(self, text, shortcut, callback):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(68, 71, 90, 0.7);
                color: #F8F8F2;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                margin: 0 5px;
            }
            QPushButton:hover {
                background: rgba(98, 114, 164, 0.8);
            }
        """)
        btn.setToolTip(f"{text} ({shortcut}")
        btn.clicked.connect(callback)
        return btn

    def setup_output_style(self, widget):
        widget.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(40, 42, 54, 0.95);
                color: #F8F8F2;
                border: none;
                font-family: 'Consolas';
                padding: 5px;
            }
        """)

    def build(self):
        self.output_tabs.setCurrentIndex(0)
        self.build_output.clear()
        file = self.main_window.get_current_file()
        if file:
            config = self.config_combo.currentText().lower()
            BuildRunner.build_only(file, self.build_output.appendPlainText)

    def run(self):
        self.output_tabs.setCurrentIndex(1)
        self.run_output.clear()
        file = self.main_window.get_current_file()
        if file:
            BuildRunner.run_only(file, self.run_output.appendPlainText)

    def build_and_run(self):
        self.output_tabs.setCurrentIndex(1)
        self.run_output.clear()
        file = self.main_window.get_current_file()
        if file:
            BuildRunner.build_and_run(file, self.run_output.appendPlainText)

    def stop(self):
        # Implement process termination
        pass

# Update main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Process events
    app.processEvents()
    
    # Create main window but don't show it yet
    window = MainWindow()
    
    # Simulate loading with smoother progress
    total_time = 10  # 10 seconds total
    steps = 100
    step_time = total_time / steps
    
    for i in range(steps):
        time.sleep(step_time)
        app.processEvents()
    
    # Show main window
    window.show()
    
    # Fade out splash screen
    fade_effect = QGraphicsOpacityEffect()
    splash.setGraphicsEffect(fade_effect)
    
    fade_anim = QPropertyAnimation(fade_effect, b"opacity")
    fade_anim.setDuration(1000)  # 1 second fade
    fade_anim.setStartValue(1)
    fade_anim.setEndValue(0)
    fade_anim.finished.connect(splash.close)
    fade_anim.start()
    
    sys.exit(app.exec())

# Add FileSystemHelper class to handle file/folder operations
class FileSystemHelper:
    def __init__(self, parent=None):
        self.parent = parent

    def create_file(self, directory):
        """Create a new file in the specified directory"""
        name, ok = QInputDialog.getText(
            self.parent,
            "New File",
            "Enter file name:",
            QLineEdit.Normal,
            "untitled.txt"
        )
        
        if ok and name:
            try:
                file_path = Path(directory) / name
                if not file_path.exists():
                    file_path.touch()
                    return str(file_path)
                else:
                    QMessageBox.warning(
                        self.parent,
                        "File Exists",
                        f"File '{name}' already exists in this location."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Could not create file: {str(e)}"
                )
        return None

    def create_folder(self, directory):
        """Create a new folder in the specified directory"""
        name, ok = QInputDialog.getText(
            self.parent,
            "New Folder",
            "Enter folder name:",
            QLineEdit.Normal,
            "New Folder"
        )
        
        if ok and name:
            try:
                folder_path = Path(directory) / name
                if not folder_path.exists():
                    folder_path.mkdir()
                    return str(folder_path)
                else:
                    QMessageBox.warning(
                        self.parent,
                        "Folder Exists",
                        f"Folder '{name}' already exists in this location."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Could not create folder: {str(e)}"
                )
        return None

# Add ProjectExplorer class for better file system organization
class ProjectExplorer(QTreeView):
    def __init__(self, root_path, parent=None):
        super().__init__(parent)
        self.root_path = root_path
        self.parent = parent
        self.setup_ui()
        self.setup_model()
        self.setup_context_menu()
        self.setup_file_icons()

    def setup_file_icons(self):
        """Setup custom icons for different file types"""
        self.file_icons = {
            '.py': QIcon('icons/python.png'),
            '.cpp': QIcon('icons/cpp.png'),
            '.c': QIcon('icons/c.png'),
            '.h': QIcon('icons/h.png'),
            '.hpp': QIcon('icons/hpp.png'),
            '.java': QIcon('icons/java.png'),
            '.js': QIcon('icons/javascript.png'),
            '.html': QIcon('icons/html.png'),
            '.css': QIcon('icons/css.png'),
            '.txt': QIcon('icons/text.png'),
            'folder': QIcon('icons/folder.png'),
            'default': QIcon('icons/file.png')
        }

    def setup_model(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(self.root_path)
        
        # Set filters to show all files and folders
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden)
        
        # Set name filters for supported file types
        self.model.setNameFilters([
            "*.py", "*.cpp", "*.c", "*.h", "*.hpp",
            "*.java", "*.js", "*.html", "*.css", "*.txt"
        ])
        self.model.setNameFilterDisables(False)
        
        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.root_path))
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # Set column width
        self.setColumnWidth(0, 250)  # Adjust name column width
        
        # Enable sorting
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        
        # Enable selection
        self.setSelectionMode(QTreeView.SingleSelection)
        self.setSelectionBehavior(QTreeView.SelectRows)
        
        # Connect signals
        self.doubleClicked.connect(self.handle_double_click)
        self.model.directoryLoaded.connect(self.expand_created_item)

    def expand_created_item(self, path):
        """Expand and select newly created item"""
        index = self.model.index(path)
        if index.isValid():
            # Expand parent
            parent = index.parent()
            if parent.isValid():
                self.expand(parent)
            # Select the new item
            self.setCurrentIndex(index)
            self.scrollTo(index)

    def handle_double_click(self, index):
        """Handle double-click on items"""
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.parent.open_file(path)

    def show_context_menu(self, position):
        menu = QMenu()
        
        # Get current item
        index = self.indexAt(position)
        current_path = self.model.filePath(index) if index.isValid() else self.root_path
        is_dir = os.path.isdir(current_path)
        
        # Add actions
        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        menu.addSeparator()
        
        if index.isValid():
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            
            # Connect item-specific actions
            rename_action.triggered.connect(lambda: self.rename_item(index))
            delete_action.triggered.connect(lambda: self.delete_item(index))
        
        # Connect new file/folder actions
        target_path = current_path if is_dir else os.path.dirname(current_path)
        new_file_action.triggered.connect(lambda: self.parent.create_new_file(target_path))
        new_folder_action.triggered.connect(lambda: self.parent.create_new_folder(target_path))
        
        menu.exec(self.viewport().mapToGlobal(position))

    def get_current_path(self):
        """Get the currently selected directory path"""
        index = self.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            return path if os.path.isdir(path) else os.path.dirname(path)
        return self.root_path

    def refresh(self):
        """Refresh the view"""
        self.model.setRootPath(self.root_path)

    def rename_item(self, index):
        """Rename selected item"""
        if not index.isValid():
            return
            
        old_path = self.model.filePath(index)
        old_name = os.path.basename(old_path)
        
        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "Enter new name:",
            QLineEdit.Normal,
            old_name
        )
        
        if ok and new_name and new_name != old_name:
            try:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Could not rename: {str(e)}"
                )

    def delete_item(self, index):
        """Delete selected item"""
        if not index.isValid():
            return
            
        path = self.model.filePath(index)
        name = os.path.basename(path)
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Could not delete: {str(e)}"
                )

    def setup_project_explorer(self):
        """Setup project explorer panel"""
        # Create dock widget for project explorer
        self.project_dock = QDockWidget("Project Explorer", self)
        self.project_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Create main widget
        explorer_widget = QWidget()
        layout = QVBoxLayout(explorer_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create header with title and buttons
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 5, 5)
        
        title = QLabel("EXPLORER")
        title.setStyleSheet("color: #6272A4; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Add action buttons
        new_file_btn = QPushButton("＋")
        new_file_btn.setToolTip("New File (Ctrl+N)")
        new_file_btn.clicked.connect(self.create_new_file)
        
        new_folder_btn = QPushButton("F＋")
        new_folder_btn.setToolTip("New Folder (Ctrl+Shift+N)")
        new_folder_btn.clicked.connect(self.create_new_folder)
        
        refresh_btn = QPushButton("⟳")
        refresh_btn.setToolTip("Refresh")
        refresh_btn.clicked.connect(self.refresh_project_tree)
        
        # Style buttons
        button_style = """
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                border-radius: 3px;
                color: #6272A4;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(98, 114, 164, 0.3);
            }
        """
        new_file_btn.setStyleSheet(button_style)
        new_folder_btn.setStyleSheet(button_style)
        refresh_btn.setStyleSheet(button_style)
        
        header_layout.addWidget(new_file_btn)
        header_layout.addWidget(new_folder_btn)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header)
        
        # Create file system model
        self.project_model = QFileSystemModel()
        self.project_model.setRootPath("")
        
        # Create tree view
        self.project_tree = QTreeView()
        self.project_tree.setModel(self.project_model)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setAnimated(True)
        self.project_tree.setIndentation(20)
        
        # Hide unnecessary columns
        self.project_tree.hideColumn(1)  # Size
        self.project_tree.hideColumn(2)  # Type
        self.project_tree.hideColumn(3)  # Date Modified
        
        # Style the tree
        self.project_tree.setStyleSheet("""
            QTreeView {
                background-color: #282A36;
                border: none;
                color: #F8F8F2;
            }
            QTreeView::item {
                padding: 5px;
                border-radius: 3px;
            }
            QTreeView::item:hover {
                background: rgba(68, 71, 90, 0.7);
            }
            QTreeView::item:selected {
                background: rgba(68, 71, 90, 0.9);
            }
        """)
        
        # Connect signals
        self.project_tree.doubleClicked.connect(self.open_file_from_tree)
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.project_tree)
        self.project_dock.setWidget(explorer_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

def create_placeholder_icon(size=64, color="#6272A4"):
    """Create a placeholder icon if image file is missing"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw background
    painter.setBrush(QColor(color))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 8, 8)
    
    painter.end()
    return pixmap

# Add this function to load images safely
def load_icon(path, size=64):
    """Load an icon, return placeholder if file not found"""
    if os.path.exists(path):
        return QPixmap(path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    else:
        return create_placeholder_icon(size)

# Update the WelcomePage class to use the safe image loading
class WelcomePage(QWidget):
    def setup_ui(self):
        # ... other code ...
        
        # Logo with fallback
        logo_label = QLabel()
        logo = load_icon("res/Pyide.png", 120)
        logo_label.setPixmap(logo)
        
        # ... rest of the code ...

    def create_action_button(self, title, tooltip, shortcut, callback, icon_name=None):
        # ... other code ...
        
        # Add icon with fallback
        if icon_name:
            icon_label = QLabel()
            icon = load_icon(f"res/{icon_name}.png", 24)
            icon_label.setPixmap(icon)
            layout.addWidget(icon_label)
            
        # ... rest of the code ...

def create_default_logo():
    """Create a default logo if none exists"""
    size = 120
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw background
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor("#BD93F9"))
    gradient.setColorAt(1, QColor("#FF79C6"))
    
    painter.setBrush(gradient)
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 20, 20)
    
    # Draw text
    painter.setPen(QColor("#F8F8F2"))
    font = QFont("Segoe UI", 24, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Py")
    
    painter.end()
    return pixmap

# Use this in WelcomePage
logo = load_icon("res/Pyide.png", 120) if os.path.exists("res/Pyide.png") else create_default_logo()

# Add this class to handle recent project items
class RecentProjectItem(QWidget):
    def __init__(self, project_info, parent=None):
        super().__init__(parent)
        self.project_info = project_info
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Project info section
        info_layout = QVBoxLayout()
        
        # Project name
        name_label = QLabel(self.project_info['name'])
        name_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['text']};
            font-size: 14px;
            font-weight: bold;
        """)
        
        # Project path
        path_label = QLabel(self.project_info['path'])
        path_label.setStyleSheet(f"""
            color: {EDITOR_COLORS['comments']};
            font-size: 12px;
        """)
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(path_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()

        # Action buttons
        open_btn = QPushButton("Open")
        open_btn.setStyleSheet(f"""
            QPushButton {{
                background: {EDITOR_COLORS['functions']}80;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                color: {EDITOR_COLORS['text']};
            }}
            QPushButton:hover {{
                background: {EDITOR_COLORS['functions']};
            }}
        """)
        open_btn.clicked.connect(self.open_project)
        layout.addWidget(open_btn)

    def open_project(self):
        if os.path.exists(self.project_info['path']):
            self.parent().parent().project_opened.emit(self.project_info['path'])
        else:
            QMessageBox.warning(
                self,
                "Project Not Found",
                f"The project directory no longer exists:\n{self.project_info['path']}"
            )
