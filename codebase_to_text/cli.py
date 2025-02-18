import os
import argparse
import git
import shutil
from pathlib import Path
from docx import Document
import tempfile

class CodebaseToText:
    def __init__(self, input_path, output_path, output_type, verbose, exclude_hidden):
        self.input_path = input_path
        self.output_path = output_path
        self.output_type = output_type
        self.verbose = verbose
        self.exclude_hidden = exclude_hidden
        self.temp_folder_path = None

    def _parse_folder(self, folder_path):
        tree = ""
        for root, dirs, files in os.walk(folder_path):
            # Exclude 'venv' directories and hidden directories if exclude_hidden is True.
            dirs[:] = [
                d for d in dirs
                if d != 'venv' and 
                (not self.exclude_hidden or not self._is_hidden_file(os.path.join(root, d)))
            ]

            level = root.replace(folder_path, '').count(os.sep)
            indent = ' ' * 4 * level
            tree += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for f in files: 
                tree += f"{subindent}{f}\n"

        if self.verbose:
            print(f"The file tree to be processed:\n{tree}")

        return tree

    def _is_binary_file(self, file_path):
        """
        Check if a file is binary by reading a small chunk.
        If null bytes are found, consider the file as binary.
        """
        try:
            with open(file_path, 'rb') as file:
                chunk = file.read(1024)
                if b'\0' in chunk:
                    return True
        except Exception as e:
            if self.verbose:
                print(f"Error reading file {file_path} in binary mode: {e}")
            return True  # If we can't read the file, assume it's binary to be safe.
        return False

    def _get_file_contents(self, file_path):
        # Open the file with UTF-8 encoding and replace errors to handle emojis and other characters gracefully.
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()
        
    def _is_hidden_file(self, file_path):
        components = os.path.normpath(file_path).split(os.sep)
        for c in components:
            if c.startswith((".", "__")):
                return True
        return False

    def _process_files(self, path):
        content = ""
        for root, dirs, files in os.walk(path):
            # Exclude 'venv' directories and hidden directories if exclude_hidden is True.
            dirs[:] = [
                d for d in dirs
                if d != 'venv' and 
                (not self.exclude_hidden or not self._is_hidden_file(os.path.join(root, d)))
            ]

            for file in files:
                file_path = os.path.join(root, file)
                if self.exclude_hidden and self._is_hidden_file(os.path.abspath(file_path)):
                    if self.verbose:
                        print(f"Ignoring hidden file {file_path}")
                    continue

                # Check if the file is binary.
                if self._is_binary_file(file_path):
                    if self.verbose:
                        print(f"Skipping binary file content for: {file_path}")
                    # Add an entry indicating that this binary file exists, but content is not included.
                    content += f"\n\n{file_path}\n"
                    content += f"File type: {os.path.splitext(file_path)[1]}\n"
                    content += "Binary file. Content not included.\n"
                    content += f"\n\n{'-' * 50}\nFile End\n{'-' * 50}\n"
                    continue

                try:
                    if self.verbose:
                        print(f"Processing: {file_path}")
                    file_content = self._get_file_contents(file_path)
                    content += f"\n\n{file_path}\n"
                    content += f"File type: {os.path.splitext(file_path)[1]}\n"
                    content += f"{file_content}"
                    # Add section headers and delimiters after each file.
                    content += f"\n\n{'-' * 50}\nFile End\n{'-' * 50}\n"
                except Exception as e:
                    print(f"Couldn't process {file_path}: {e}")
        return content

    def get_text(self):
        folder_structure = ""
        file_contents = ""
        if self.is_github_repo():
            self._clone_github_repo()
            folder_structure = self._parse_folder(self.temp_folder_path)
            file_contents = self._process_files(self.temp_folder_path)
        else:
            folder_structure = self._parse_folder(self.input_path)
            file_contents = self._process_files(self.input_path)
        
        # Section headers.
        folder_structure_header = "Folder Structure"
        file_contents_header = "File Contents"
        
        # Delimiters.
        delimiter = "-" * 50
        
        # Format the final text.
        final_text = f"{folder_structure_header}\n{delimiter}\n{folder_structure}\n\n{file_contents_header}\n{delimiter}\n{file_contents}"
        
        return final_text

    def get_file(self):
        text = self.get_text()
        if self.output_type == "txt":
            with open(self.output_path, "w", encoding="utf-8") as file:
                file.write(text)
        elif self.output_type == "docx":
            doc = Document()
            doc.add_paragraph(text)
            doc.save(self.output_path)
        else:
            raise ValueError("Invalid output type. Supported types: txt, docx")
        
    #### Github-related Methods ####

    def _clone_github_repo(self):
        try:
            self.temp_folder_path = tempfile.mkdtemp(prefix="github_repo_")
            git.Repo.clone_from(self.input_path, self.temp_folder_path)
            if self.verbose:
                print("GitHub repository cloned successfully.")
        except Exception as e:
            print(f"Error cloning GitHub repository: {e}")

    def is_github_repo(self):
        return self.input_path.startswith("https://github.com/") or self.input_path.startswith("git@github.com:")

    def is_temp_folder_used(self):
        return self.temp_folder_path is not None

    def clean_up_temp_folder(self):
        if self.temp_folder_path:
            shutil.rmtree(self.temp_folder_path)

def main():
    parser = argparse.ArgumentParser(description="Generate text from codebase.")
    parser.add_argument("--input", help="Input path (folder or GitHub URL)", required=True)
    parser.add_argument("--output", help="Output file path", required=True)
    parser.add_argument("--output_type", help="Output file type (txt or docx)", required=True)
    parser.add_argument("--exclude_hidden", help="Exclude hidden files and folders", action="store_true")
    parser.add_argument("--verbose", help="Show useful information", action="store_true")
    args = parser.parse_args()

    code_to_text = CodebaseToText(
        input_path=args.input,
        output_path=args.output,
        output_type=args.output_type,
        verbose=args.verbose,
        exclude_hidden=args.exclude_hidden
    )
    code_to_text.get_file()

    # Remove temporary folder if it was used.
    if code_to_text.is_temp_folder_used():
        code_to_text.clean_up_temp_folder()

if __name__ == "__main__":
    main()
