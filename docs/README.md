# Codebase to Text Converter

Converts a codebase (folder structure with files) into a single text file or a Microsoft Word document (.docx), preserving folder structure and file contents.

## Features

- Supports conversion of local codebase or GitHub repositories.
- Retains folder structure in a tree-like format.
- Extracts file contents and metadata.
- Supports multiple file types including text files (.txt) and Microsoft Word documents (.docx).

## Installation

You can install the package using pip:

```bash
pip install codebase-to-text

Usage
Command-line Interface (CLI)
You can use the package via the command line interface (CLI):

codebase-to-text --input "path_or_github_url" --output "output_path" --output_type "txt"


Pythonic Way
You can also use it programmatically in your Python code:

from codebase_to_text import CodebaseToText

code_to_text = CodebaseToText(input_path="path_or_github_url", output_path="output_path", output_type="txt")
code_to_text.get_file()


Parameters
--input: Input path (local folder or GitHub URL).
--output: Output file path.
--output_type: Output file type (txt or docx).
Examples
Convert a local codebase to a text file:

codebase-to-text --input "~/projects/my_project" --output "output.txt" --output_type "txt"


Convert a GitHub repository to a Microsoft Word document:

codebase-to-text --input "https://github.com/username/repo_name" --output "output.docx" --output_type "docx"

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature_branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature_branch).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.


Feel free to customize this template to better suit your project's specifics. Ensure you update placeholders like `"path_or_github_url"`, `"output_path"`, `"txt"`, and `"docx"` with actual values and add any additional sections or information that you think would be useful for your users.
