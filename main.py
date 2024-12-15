import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import StringVar, IntVar, Checkbutton, Label, Button, Entry

from config.development_config import DevelopmentConfig
from src.services.project_scanner.filter_settings import FilterSettings
from src.services.project_scanner.project_overview_service import ProjectOverviewService


class ProjectScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Scanner")
        self.root.geometry("800x750")

        self.config = DevelopmentConfig()

        self.file_filters = StringVar(value=", ".join(self.config.FILE_FILTERS.ignore_files))
        self.dir_filters = StringVar(value=", ".join(self.config.FILE_FILTERS.ignore_dirs))
        self.ext_filters = StringVar(value=", ".join(self.config.FILE_FILTERS.ignore_extensions))

        self.show_structure = IntVar(value=1)
        self.show_content = IntVar(value=0)
        self.show_documentation = IntVar(value=0)

        self.build_ui()

    def build_ui(self):
        self.select_dir_button = Button(self.root, text="Select Project Directory", command=self.select_directory)
        self.select_dir_button.pack(pady=5)

        Label(self.root, text="File Filters (comma-separated):").pack(anchor="w", padx=10)
        self.file_filters_entry = Entry(self.root, textvariable=self.file_filters, width=80)
        self.file_filters_entry.pack(pady=2, padx=10)

        Label(self.root, text="Directory Filters (comma-separated):").pack(anchor="w", padx=10)
        self.dir_filters_entry = Entry(self.root, textvariable=self.dir_filters, width=80)
        self.dir_filters_entry.pack(pady=2, padx=10)

        Label(self.root, text="Extension Filters (comma-separated):").pack(anchor="w", padx=10)
        self.ext_filters_entry = Entry(self.root, textvariable=self.ext_filters, width=80)
        self.ext_filters_entry.pack(pady=2, padx=10)

        Label(self.root, text="Options:").pack(anchor="w", padx=10, pady=5)
        Checkbutton(self.root, text="Show Project Structure", variable=self.show_structure).pack(anchor="w", padx=20)
        Checkbutton(self.root, text="Show Project Content", variable=self.show_content).pack(anchor="w", padx=20)
        Checkbutton(self.root, text="Show Project Documentation", variable=self.show_documentation).pack(anchor="w", padx=20)

        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=20)
        self.result_text.pack(pady=10, padx=10)

        self.analyze_button = Button(self.root, text="Analyze Project", command=self.analyze_project, state=tk.DISABLED)
        self.analyze_button.pack(pady=5)

        self.copy_button = Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Project Directory")
        if directory:
            self.project_path = os.path.abspath(directory)
            self.result_text.insert(tk.END, f"Selected directory: {self.project_path}\n")
            self.analyze_button.config(state=tk.NORMAL)

    def analyze_project(self):
        if not hasattr(self, "project_path"):
            self.result_text.insert(tk.END, "No directory selected!\n")
            return

        file_filters = [f.strip() for f in self.file_filters.get().split(",") if f.strip()]
        dir_filters = [d.strip() for d in self.dir_filters.get().split(",") if d.strip()]
        ext_filters = [e.strip() for e in self.ext_filters.get().split(",") if e.strip()]

        filter_settings = FilterSettings(
            ignored_files=file_filters,
            ignored_directories=dir_filters,
            ignored_extensions=ext_filters,
        )

        service = ProjectOverviewService(self.project_path, filter_settings)

        try:
            result = []

            if self.show_structure.get():
                structure = service.get_project_structure()
                result.append("=================\n# структура проекта в виде дерева папок и файлов\n<project_structure>\n")
                result.append(structure)
                result.append("\n</project_structure>\n")

            if self.show_documentation.get():
                documentation = service.get_project_documentation()
                result.append("=================\n# Документация проекта. Перечисление всех классов и их функционала, а также в каких файлах из структуры они находятся\n<project_documentation>\n")
                result.append(documentation)
                result.append("\n</project_documentation>\n")

            if self.show_content.get():
                content = service.get_project_content()
                result.append("=================\n# Содержание файлов без комментариев\n<project_content>\n")
                result.append(content)
                result.append("\n</project_content>\n")

            formatted_result = "\n".join(result)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, formatted_result)

        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def copy_to_clipboard(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectScannerApp(root)
    root.mainloop()
