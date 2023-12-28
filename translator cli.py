import os
import re
from googletrans import Translator, LANGUAGES

def translate_comments_and_prints(file_path, target_language='en', destination_language='en', api_key=None):
    translator = Translator(service_urls=['translate.googleapis.com'], timeout=5)

    if api_key:
        translator.raise_Exception = True
        translator.raise_NotImplementedError = True
        translator.service_urls = ['translate.googleapis.com']
        translator.headers = {'X-Goog-Api-Key': api_key}

    with open(file_path, 'r', encoding='utf-8') as file:
        script_content = file.read()

    def translate(match):
        text_to_translate = match.group(0)
        translated_text = translator.translate(text_to_translate, dest=destination_language).text
        return translated_text

    # Translate code comments
    script_content = re.sub(r'#.*', translate, script_content)

    # Translate print statements
    script_content = re.sub(r'print\(.*\)', translate, script_content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(script_content)

def show_files_in_directory(directory='.'):
    print("Files found in the directory:")
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                print(file_path)

def get_api_key():
    print("\nTo use the Google Translate API, you need an API key. Follow these steps:")
    print("1. Go to the Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one.")
    print("3. Enable the 'Cloud Translation API' for your project.")
    print("4. Create API credentials and download the JSON file.")
    print("5. Set the environment variable 'GOOGLE_APPLICATION_CREDENTIALS' to the path of the downloaded JSON file.")
    print("For more details, refer to the Google Cloud documentation.")
    print("Note: Be cautious with your API key, and keep it secure.")

def select_target_language():
    print("\nSelect target language:")
    for code, lang in LANGUAGES.items():
        print(f"{code}: {lang}")

    target_language = input("Enter the code for the target language: ")
    return target_language.lower()

def select_destination_language():
    print("\nSelect destination language:")
    for code, lang in LANGUAGES.items():
        print(f"{code}: {lang}")

    destination_language = input("Enter the code for the destination language: ")
    return destination_language.lower()

def translate_code_in_directory(directory='.', api_key=None):
    target_language = 'en'  # Default target language
    destination_language = 'en'  # Default destination language

    while True:
        print("\nMenu:")
        print("1. Show all files found")
        print("2. Begin translation process")
        print("3. Get Google Translate API key instructions")
        print("4. Select target language")
        print("5. Select destination language")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            show_files_in_directory(directory)
        elif choice == '2':
            confirmation = input("Are you sure you want to start the translation process? (yes/no): ").lower()
            if confirmation == 'yes':
                target_language = select_target_language()
                destination_language = select_destination_language()
                for root, dirs, files in os.walk(directory):
                    for file_name in files:
                        if file_name.endswith('.py'):
                            file_path = os.path.join(root, file_name)
                            translate_comments_and_prints(file_path, target_language, destination_language, api_key)
                print("Translation process completed.")
            else:
                print("Translation process aborted.")
        elif choice == '3':
            get_api_key()
        elif choice == '4':
            target_language = select_target_language()
            print(f"Target language set to: {LANGUAGES.get(target_language, 'Unknown')}")
        elif choice == '5':
            destination_language = select_destination_language()
            print(f"Destination language set to: {LANGUAGES.get(destination_language, 'Unknown')}")
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please enter 0, 1, 2, 3, 4, or 5.")

# Example usage
translate_code_in_directory()

# Footer statement for copyright by Curtis Click
print("\nCopyright © 2023 Curtis Click. All rights reserved.")
