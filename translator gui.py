import os
import re
from googletrans import Translator, LANGUAGES
import tkinter as tk
from tkinter import filedialog

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Translator")
        
        # Default values
        self.target_language = 'en'
        self.destination_language = 'en'
        self.api_key = None

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Select target language:").grid(row=0, column=0, sticky='w')
        self.target_lang_entry = tk.Entry(self.master)
        self.target_lang_entry.grid(row=0, column=1)
        self.target_lang_entry.insert(0, self.target_language)

        tk.Label(self.master, text="Select destination language:").grid(row=1, column=0, sticky='w')
        self.dest_lang_entry = tk.Entry(self.master)
        self.dest_lang_entry.grid(row=1, column=1)
        self.dest_lang_entry.insert(0, self.destination_language)

        tk.Button(self.master, text="Select Directory", command=self.select_directory).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.master, text="Translate Code", command=self.translate_code).grid(row=3, column=0, columnspan=2, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.translate_code_in_directory(directory)

    def translate_code(self):
        self.target_language = self.target_lang_entry.get()
        self.destination_language = self.dest_lang_entry.get()

        directory = filedialog.askdirectory()
        if directory:
            self.translate_code_in_directory(directory)

    def translate_code_in_directory(self, directory):
        translator = Translator(service_urls=['translate.googleapis.com'], timeout=5)

        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        script_content = file.read()

                    def translate(match):
                        text_to_translate = match.group(0)
                        translated_text = translator.translate(text_to_translate, dest=self.destination_language).text
                        return translated_text

                    # Translate code comments
                    script_content = re.sub(r'#.*', translate, script_content)

                    # Translate print statements
                    script_content = re.sub(r'print\(.*\)', translate, script_content)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(script_content)

        print("Translation process completed.")


def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
