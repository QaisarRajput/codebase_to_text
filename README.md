# Codebase to Text Converter
For GenAI and LLM usage. This package converts codebase (folder structure with files) into a single text file or a Microsoft Word document (.docx), preserving folder structure and file contents. The tool extracts file contents from various file types, including text files, documents, and more, while retaining their formatting for easy readability.



Converts a codebase (folder structure with files) into a single text file or a Microsoft Word document (.docx), preserving folder structure and file contents.

## Features

- Supports conversion of local codebase or GitHub repositories.
- Retains folder structure in a tree-like format.
- Extracts file contents and metadata.
- Supports multiple file types including text files (.txt) and Microsoft Word documents (.docx).
- Excludes Venv folder

## Installation

Git clone the repo
Go inside the project folder

```bash
pip install -e .
```

## Usage
### Command-line Interface (CLI)
You can use the package via the command line interface (CLI):
```bash
codebase-to-text --input "path_or_github_url" --output "output_path" --output_type "txt"
```

### Pythonic Way
You can also use it programmatically in your Python code:

```python
from codebase_to_text import CodebaseToText

code_to_text = CodebaseToText(input_path="path_or_github_url", output_path="output_path", output_type="txt")
code_to_text.get_file()
```

### Parameters
--input: Input path (local folder or GitHub URL).
--output: Output file path.
--output_type: Output file type (txt or docx).


## Examples
Convert a local codebase to a text file:
```bash
codebase-to-text --input "~/projects/my_project" --output "output.txt" --output_type "txt"
```

Convert a GitHub repository to a Microsoft Word document:

```bash
codebase-to-text --input "https://github.com/username/repo_name" --output "output.docx" --output_type "docx"
```


License
This project is licensed under the MIT License - see the LICENSE file for details.


