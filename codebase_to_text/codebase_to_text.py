import os
import argparse
import shutil
from pathlib import Path
from docx import Document

class CodebaseToText:
    def __init__(self, input_path, output_path, output_type):
        self.input_path = input_path
        self.output_path = output_path
        self.output_type = output_type

    def _parse_folder(self, folder_path):
        tree = ""
        for root, dirs, files in os.walk(folder_path):
            level = root.replace(folder_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree += '{}{}/\n'.format(indent, os.path.basename(root))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree += '{}{}\n'.format(subindent, f)
        return tree

    def _get_file_contents(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def _process_files(self):
        content = ""
        for root, _, files in os.walk(self.input_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_content = self._get_file_contents(file_path)
                content += f"\n\n{file_path}\n"
                content += f"File type: {os.path.splitext(file_path)[1]}\n"
                content += f"{file_content}"
                # Add section headers and delimiters after each file
                content += f"\n\n{'-' * 50}\nFile End\n{'-' * 50}\n"
        return content

    def get_text(self):
        folder_structure = self._parse_folder(self.input_path)
        file_contents = self._process_files()
        
        # Section headers
        folder_structure_header = "Folder Structure"
        file_contents_header = "File Contents"
        
        # Delimiters
        delimiter = "-" * 50
        
        # Format the final text
        final_text = f"{folder_structure_header}\n{delimiter}\n{folder_structure}\n\n{file_contents_header}\n{delimiter}\n{file_contents}"
        
        return final_text


    def get_file(self):
        text = self.get_text()
        if self.output_type == "txt":
            with open(self.output_path, "w") as file:
                file.write(text)
        elif self.output_type == "docx":
            doc = Document()
            doc.add_paragraph(text)
            doc.save(self.output_path)
        else:
            raise ValueError("Invalid output type. Supported types: txt, docx")

def main():
    parser = argparse.ArgumentParser(description="Generate text from codebase.")
    parser.add_argument("--input", help="Input path (folder or GitHub URL)", required=True)
    parser.add_argument("--output", help="Output file path", required=True)
    parser.add_argument("--output_type", help="Output file type (txt or docx)", required=True)
    args = parser.parse_args()

    code_to_text = CodebaseToText(input_path=args.input, output_path=args.output, output_type=args.output_type)
    code_to_text.get_file()

if __name__ == "__main__":
    main()
