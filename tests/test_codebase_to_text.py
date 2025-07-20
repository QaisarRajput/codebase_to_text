import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from codebase_to_text.codebase_to_text import CodebaseToText


class TestCodebaseToText(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temporary folder structure"""
        self.test_folder_path = tempfile.mkdtemp(prefix="test_codebase_")
        
        # Create test folder structure
        self._create_test_structure()
        
        # Output paths for testing
        self.output_txt = os.path.join(self.test_folder_path, "output.txt")
        self.output_docx = os.path.join(self.test_folder_path, "output.docx")

    def _create_test_structure(self):
        """Create a complex test folder structure"""
        base = self.test_folder_path
        
        # Create main files
        with open(os.path.join(base, "main.py"), "w") as f:
            f.write("print('Hello World')")
        
        with open(os.path.join(base, "README.md"), "w") as f:
            f.write("# Test Project\nThis is a test.")
        
        with open(os.path.join(base, "requirements.txt"), "w") as f:
            f.write("requests>=2.25.0\npandas>=1.3.0")
        
        # Create subdirectories
        os.makedirs(os.path.join(base, "src"), exist_ok=True)
        os.makedirs(os.path.join(base, "tests"), exist_ok=True)
        os.makedirs(os.path.join(base, "__pycache__"), exist_ok=True)
        os.makedirs(os.path.join(base, ".git"), exist_ok=True)
        os.makedirs(os.path.join(base, "venv", "lib"), exist_ok=True)
        os.makedirs(os.path.join(base, "logs"), exist_ok=True)
        
        # Create files in subdirectories
        with open(os.path.join(base, "src", "app.py"), "w") as f:
            f.write("def main():\n    pass")
        
        with open(os.path.join(base, "src", "utils.py"), "w") as f:
            f.write("def helper():\n    return True")
        
        with open(os.path.join(base, "tests", "test_app.py"), "w") as f:
            f.write("import unittest\n\nclass TestApp(unittest.TestCase):\n    pass")
        
        # Create files that should be excluded by default
        with open(os.path.join(base, "__pycache__", "app.cpython-39.pyc"), "w") as f:
            f.write("binary content")
        
        with open(os.path.join(base, ".git", "config"), "w") as f:
            f.write("[core]\nrepositoryformatversion = 0")
        
        with open(os.path.join(base, "venv", "lib", "python3.9"), "w") as f:
            f.write("virtual env file")
        
        with open(os.path.join(base, "logs", "app.log"), "w") as f:
            f.write("2023-01-01 10:00:00 INFO Application started")
        
        with open(os.path.join(base, "temp.tmp"), "w") as f:
            f.write("temporary content")
        
        # Create hidden files
        with open(os.path.join(base, ".gitignore"), "w") as f:
            f.write("*.pyc\n__pycache__/\n.env")
        
        with open(os.path.join(base, ".env"), "w") as f:
            f.write("SECRET_KEY=test123")

    def test_basic_functionality(self):
        """Test basic text generation without exclusions"""
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=[]
        )
        
        text = code_to_text.get_text()
        self.assertIn("Folder Structure", text)
        self.assertIn("File Contents", text)
        self.assertIn("main.py", text)
        self.assertIn("Hello World", text)

    def test_exclude_hidden_files(self):
        """Test exclusion of hidden files"""
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=True,
            exclude=[]
        )
        text = code_to_text.get_text()
        self.assertNotIn(".gitignore", text)
        self.assertNotIn(".env", text)
        self.assertIn("main.py", text)  # Regular files should still be included

    def test_exclude_patterns(self):
        """Test pattern-based exclusions"""
        exclude_patterns = ["*.log", "*.tmp", "__pycache__/**", ".git/**"]
        
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=exclude_patterns
        )
        
        text = code_to_text.get_text()
        
        # Split the text to get only the folder structure section
        folder_structure_section = text.split("File Contents")[0]
        
        # Should exclude log and tmp files from folder structure
        self.assertNotIn("app.log", folder_structure_section)
        self.assertNotIn("temp.tmp", folder_structure_section)
        self.assertNotIn("__pycache__/", folder_structure_section)
        self.assertNotIn(".git/", folder_structure_section)
        
        # Should include normal files in folder structure
        self.assertIn("main.py", folder_structure_section)
        self.assertIn("src/", folder_structure_section)

    def test_exclude_specific_files(self):
        """Test exclusion of specific files"""
        exclude_patterns = ["README.md", "requirements.txt"]
        
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=exclude_patterns
        )
        
        text = code_to_text.get_text()
          # Should exclude specified files
        self.assertNotIn("README.md", text)
        self.assertNotIn("requirements.txt", text)
        
        # Should include other files
        self.assertIn("main.py", text)

    def test_exclude_directories(self):
        """Test exclusion of entire directories"""
        exclude_patterns = ["venv/", "logs/"]
        
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=exclude_patterns
        )
        
        text = code_to_text.get_text()
        
        # Split the text to get only the folder structure section
        folder_structure_section = text.split("File Contents")[0]
        
        # Should exclude specified directories from folder structure
        self.assertNotIn("venv/", folder_structure_section)
        self.assertNotIn("logs/", folder_structure_section)
        
        # Should include other directories
        self.assertIn("src/", folder_structure_section)
        self.assertIn("tests/", folder_structure_section)

    def test_exclude_file_creation(self):
        """Test loading exclusion patterns from .exclude file"""
        exclude_file_path = os.path.join(self.test_folder_path, ".exclude")
        
        # Create .exclude file
        with open(exclude_file_path, "w") as f:
            f.write("# This is a comment\n")
            f.write("*.log\n")
            f.write("temp.tmp\n")
            f.write("venv/\n")
            f.write("\n")  # Empty line
        
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=[]
        )
        
        text = code_to_text.get_text()
        
        # Split the text to get only the folder structure section
        folder_structure_section = text.split("File Contents")[0]
        
        # Should exclude files listed in .exclude file from folder structure
        self.assertNotIn("app.log", folder_structure_section)
        self.assertNotIn("temp.tmp", folder_structure_section)
        self.assertNotIn("venv/", folder_structure_section)

    def test_combined_exclusions(self):
        """Test combination of CLI args and .exclude file"""
        exclude_file_path = os.path.join(self.test_folder_path, ".exclude")
        
        # Create .exclude file
        with open(exclude_file_path, "w") as f:
            f.write("*.log\n")
            f.write("venv/\n")
        
        # Also provide CLI exclusions
        cli_excludes = ["*.tmp", "__pycache__/"]
        
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=cli_excludes
        )
        
        text = code_to_text.get_text()
        
        # Split the text to get only the folder structure section
        folder_structure_section = text.split("File Contents")[0]
        
        # Should exclude files from both sources from folder structure
        self.assertNotIn("app.log", folder_structure_section)  # From .exclude file
        self.assertNotIn("venv/", folder_structure_section)    # From .exclude file
        self.assertNotIn("temp.tmp", folder_structure_section) # From CLI
        self.assertNotIn("__pycache__/", folder_structure_section) # From CLI

    def test_output_file_generation_txt(self):
        """Test TXT file output generation"""
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            exclude=["*.log", "*.tmp"]
        )
        
        code_to_text.get_file()
        
        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_txt))
        
        # Check content
        with open(self.output_txt, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Folder Structure", content)
            self.assertIn("main.py", content)

    def test_output_file_generation_docx(self):
        """Test DOCX file output generation"""
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_docx,
            output_type="docx",
            verbose=False,
            exclude_hidden=False,
            exclude=["*.log", "*.tmp"]
        )
        
        code_to_text.get_file()
        
        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_docx))

    def test_verbose_mode(self):
        """Test verbose output mode"""
        import io
        import sys
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            code_to_text = CodebaseToText(
                input_path=self.test_folder_path,
                output_path=self.output_txt,
                output_type="txt",
                verbose=True,
                exclude_hidden=False,
                exclude=["*.log"]
            )
            
            code_to_text.get_file()
            
            # Get the output
            output = captured_output.getvalue()
            
            # Should contain verbose messages
            self.assertIn("Active exclusion patterns", output)
            self.assertIn("Processing:", output)
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_invalid_output_type(self):
        """Test error handling for invalid output type"""
        with self.assertRaises(ValueError):
            code_to_text = CodebaseToText(
                input_path=self.test_folder_path,
                output_path="output.xyz",
                output_type="xyz",
                verbose=False,
                exclude_hidden=False,
                exclude=[]
            )
            code_to_text.get_file()    
            
    def test_exclusion_count_tracking(self):
        """Test that exclusion counting works correctly"""
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path=self.output_txt,
            output_type="txt",
            verbose=True,  # Need verbose mode for this test to work properly
            exclude_hidden=False,
            exclude=["*.log", "*.tmp", "__pycache__/**"]
        )
        
        # Generate text to trigger exclusion counting
        code_to_text.get_text()
        
        # Should have excluded some files
        self.assertGreater(code_to_text.excluded_files_count, 0)

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_folder_path):
            shutil.rmtree(self.test_folder_path)


class TestPatternMatching(unittest.TestCase):
    """Test exclusion pattern matching specifically"""
    
    def setUp(self):
        self.test_folder_path = tempfile.mkdtemp(prefix="test_patterns_")
        self.code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path="dummy.txt",
            output_type="txt",
            exclude=[]
        )

    def test_wildcard_patterns(self):
        """Test wildcard pattern matching"""
        self.code_to_text.exclude_patterns = {"*.py", "*.log"}
        
        # Should match
        self.assertTrue(self.code_to_text._should_exclude("test.py", self.test_folder_path))
        self.assertTrue(self.code_to_text._should_exclude("app.log", self.test_folder_path))
        
        # Should not match
        self.assertFalse(self.code_to_text._should_exclude("test.txt", self.test_folder_path))
        self.assertFalse(self.code_to_text._should_exclude("README.md", self.test_folder_path))

    def test_directory_patterns(self):
        """Test directory pattern matching"""
        self.code_to_text.exclude_patterns = {"__pycache__/", "node_modules/"}
        
        # Create test directories
        pycache_dir = os.path.join(self.test_folder_path, "__pycache__")
        os.makedirs(pycache_dir, exist_ok=True)
        
        # Should match directories
        self.assertTrue(self.code_to_text._should_exclude(pycache_dir, self.test_folder_path))

    def test_recursive_patterns(self):
        """Test recursive wildcard patterns"""
        self.code_to_text.exclude_patterns = {"**/__pycache__/**", "**/node_modules/**"}
        
        # Create nested test structure
        nested_pycache = os.path.join(self.test_folder_path, "src", "utils", "__pycache__", "file.pyc")
        os.makedirs(os.path.dirname(nested_pycache), exist_ok=True)
        
        # Should match nested paths
        self.assertTrue(self.code_to_text._should_exclude(nested_pycache, self.test_folder_path))

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_folder_path):
            shutil.rmtree(self.test_folder_path)


if __name__ == "__main__":
    # Run specific test class or all tests
    unittest.main(verbosity=2)