# Codebase to Text Converter

A powerful Python tool that converts codebases (folder structures with files) into a single text file or Microsoft Word document (.docx), while preserving folder structure and file contents. Perfect for AI/LLM processing, documentation generation, and code analysis.

## ✨ Features

- **Multi-source input**: Local directories and GitHub repositories
- **Flexible output**: Text files (.txt) and Microsoft Word documents (.docx)
- **Smart exclusions**: Advanced pattern matching for files and directories
- **Performance optimized**: Efficient traversal of large codebases
- **Comprehensive logging**: Detailed verbose mode for transparency
- **Encoding support**: Handles various file encodings gracefully

## 🚀 Installation

```bash
pip install codebase-to-text
```

## 📖 Usage

### Command Line Interface (CLI)

#### Basic Usage
```bash
codebase-to-text --input "path_or_github_url" --output "output_path" --output_type "txt"
```

#### Advanced Usage with Exclusions
```bash
# Exclude specific patterns
codebase-to-text --input "./my_project" --output "output.txt" --output_type "txt" --exclude "*.log,temp/,**/__pycache__/**"

# Multiple exclude arguments
codebase-to-text --input "./my_project" --output "output.txt" --output_type "txt" --exclude "*.pyc" --exclude "build/" --exclude "venv/"

# Exclude hidden files
codebase-to-text --input "./my_project" --output "output.txt" --output_type "txt" --exclude_hidden

# Verbose mode for detailed logging
codebase-to-text --input "./my_project" --output "output.txt" --output_type "txt" --verbose
```

### Python API

```python
from codebase_to_text import CodebaseToText

# Basic usage
converter = CodebaseToText(
    input_path="path_or_github_url",
    output_path="output_path",
    output_type="txt"
)
converter.get_file()

# Advanced usage with exclusions
converter = CodebaseToText(
    input_path="./my_project",
    output_path="./output.txt",
    output_type="txt",
    exclude=["*.log", "temp/", "**/__pycache__/**"],
    exclude_hidden=True,
    verbose=True
)
converter.get_file()

# Get text content without saving to file
text_content = converter.get_text()
print(text_content)
```

## 🎯 Exclusion Patterns

The tool supports powerful exclusion patterns to filter out unwanted files and directories:

### Pattern Types

1. **Exact filename**: `README.md`, `config.yaml`
2. **Wildcard patterns**: `*.log`, `*.tmp`, `test_*`
3. **Directory patterns**: `__pycache__/`, `.git/`, `node_modules/`
4. **Recursive patterns**: `**/__pycache__/**`, `**/node_modules/**`
5. **Path-based patterns**: `src/temp/`, `docs/build/`

### Exclusion Sources

1. **CLI Arguments**: Use `--exclude` flag (can be used multiple times)
2. **`.exclude` file**: Place in your project root (see example below)
3. **Default patterns**: Common files/folders are excluded automatically

### Default Exclusions

The tool automatically excludes common development files:
- `.git/`, `__pycache__/`, `*.pyc`, `*.pyo`
- `node_modules/`, `.venv/`, `venv/`, `env/`
- `*.log`, `*.tmp`, `.DS_Store`
- `.pytest_cache/`, `build/`, `dist/`

## 📝 .exclude File Example

Create a `.exclude` file in your project root:

```
# .exclude file - Patterns for files/folders to exclude

# Version control
.git/
.gitignore

# Python
__pycache__/
*.pyc
venv/
.pytest_cache/

# Node.js
node_modules/
*.log

# IDE files
.vscode/
.idea/

# Project specific
config/secrets.yaml
data/large_files/
```

## 🔧 CLI Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--input` | Input path (local folder or GitHub URL) | `./my_project` or `https://github.com/user/repo` |
| `--output` | Output file path | `./output.txt` |
| `--output_type` | Output format (`txt` or `docx`) | `txt` |
| `--exclude` | Exclusion patterns (repeatable) | `--exclude "*.log" --exclude "temp/"` |
| `--exclude_hidden` | Exclude hidden files/folders | Flag (no value) |
| `--verbose` | Enable detailed logging | Flag (no value) |

## 💡 Examples

### Convert Local Project
```bash
# Basic conversion
codebase-to-text --input "~/projects/my_app" --output "my_app_code.txt" --output_type "txt"

# With custom exclusions
codebase-to-text --input "~/projects/my_app" --output "my_app_code.txt" --output_type "txt" --exclude "*.log,build/,dist/" --verbose
```

### Convert GitHub Repository
```bash
# Public repository
codebase-to-text --input "https://github.com/username/repo" --output "repo_analysis.docx" --output_type "docx"

# With exclusions for cleaner output
codebase-to-text --input "https://github.com/username/repo" --output "repo_clean.txt" --output_type "txt" --exclude "*.md,docs/,examples/"
```

### Python Integration
```python
# Analyze a codebase programmatically
from codebase_to_text import CodebaseToText

def analyze_codebase(project_path):
    converter = CodebaseToText(
        input_path=project_path,
        output_path="analysis.txt",
        output_type="txt",
        exclude=["*.log", "test/", "**/__pycache__/**"],
        verbose=True
    )
    
    # Get the content
    content = converter.get_text()
    
    # Process with your preferred LLM/AI tool
    # analysis_result = your_ai_tool.analyze(content)
    
    return content

# Usage
code_content = analyze_codebase("./my_project")
```

## 🎯 Use Cases

- **AI/LLM Training**: Prepare codebases for language model training
- **Code Review**: Generate comprehensive code overviews for review
- **Documentation**: Create single-file documentation from projects
- **Analysis**: Feed entire codebases to AI tools for analysis
- **Migration**: Document legacy codebases before migration
- **Learning**: Study open-source projects more effectively

## 🔄 Output Format

The generated output includes:

1. **Folder Structure**: Tree-like representation of the directory structure
2. **File Contents**: Full content of each file with metadata
3. **Clear Separators**: Distinct sections for easy navigation
