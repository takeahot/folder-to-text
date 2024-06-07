import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory_path)

def collect_files_content(directory):
    files_content = []
    error_files = []
    excluded_extensions = ['.md', '.svg']
    for root, dirs, files in os.walk(directory):
        # Пропускаем папки, начинающиеся с точки, и специальные папки
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'build', 'public']]
        for file in files:
            if file.startswith('.') or file == 'package-lock.json':
                continue  # Пропускаем файлы, начинающиеся с точки и package-lock.json
            file_path = os.path.join(root, file)
            if any(file.endswith(ext) for ext in excluded_extensions):
                continue  # Пропускаем файлы с исключёнными расширениями
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                # Форматируем информацию о файле для отображения
                relative_file_path = os.path.relpath(file_path, directory)
                file_info = f"-- {relative_file_path}\n{file_content}\n\n"
                files_content.append(file_info)
            except (UnicodeDecodeError, ValueError) as e:
                error_files.append(f"Cannot read file: {file_path} due to {e}")
    if error_files:
        error_message = "\n".join(error_files)
        print(error_message)
    return ''.join(files_content)

def save_to_file():
    directory = dir_entry.get()
    if not directory or not os.path.isdir(directory):
        messagebox.showerror("Ошибка", "Укажите корректную директорию")
        return
    
    content = collect_files_content(directory)
    
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        messagebox.showinfo("Успех", f"Файлы успешно сохранены в {save_path}")

# Создание основного окна
root = tk.Tk()
root.title("Collect Files Content")

# Поле для ввода пути к директории с предзаполнением
tk.Label(root, text="Directory Path:").grid(row=0, column=0, padx=10, pady=5)
dir_entry = tk.Entry(root, width=50)
dir_entry.grid(row=0, column=1, padx=10, pady=5)
dir_entry.insert(0, "/Users/anton/Documents/vs_projects/download all contact from casavi")
tk.Button(root, text="Browse...", command=select_directory).grid(row=0, column=2, padx=10, pady=5)

# Кнопка для сохранения содержимого файлов
tk.Button(root, text="Save to File", command=save_to_file).grid(row=1, column=1, pady=10)

# Текстовое поле для вывода результатов
output_text = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Функция для отображения файлов в текстовом поле
def display_files():
    directory = dir_entry.get()
    if not directory or not os.path.isdir(directory):
        messagebox.showerror("Ошибка", "Укажите корректную директорию")
        return
    
    content = collect_files_content(directory)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, content)

# Кнопка для отображения файлов
tk.Button(root, text="Display Files", command=display_files).grid(row=1, column=2, pady=10)

# Привязка стандартных шорткатов для работы с текстом
root.bind_class("Text", "<Control-a>", lambda event: event.widget.tag_add("sel", "1.0", "end"))
root.bind_class("Text", "<Control-A>", lambda event: event.widget.tag_add("sel", "1.0", "end"))
root.bind_class("Text", "<Control-c>", lambda event: event.widget.event_generate("<<Copy>>"))
root.bind_class("Text", "<Control-C>", lambda event: event.widget.event_generate("<<Copy>>"))
root.bind_class("Text", "<Control-v>", lambda event: event.widget.event_generate("<<Paste>>"))
root.bind_class("Text", "<Control-V>", lambda event: event.widget.event_generate("<<Paste>>"))
root.bind_class("Text", "<Control-x>", lambda event: event.widget.event_generate("<<Cut>>"))
root.bind_class("Text", "<Control-X>", lambda event: event.widget.event_generate("<<Cut>>"))

# Запуск главного цикла приложения
root.mainloop()
