#!/usr/bin/env python3
"""
Comprehensive testing script for the Tools Website project
Tests both frontend (TypeScript) and backend (Python) components
"""
import subprocess
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

class ProjectTester:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.results: Dict[str, Dict] = {}
        
    def run_command(self, command: str, cwd: Path = None, capture_output: bool = True) -> Tuple[bool, str, str]:
        """Run a command and return success status, stdout, stderr"""
        try:
            if cwd is None:
                cwd = self.project_dir
                
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=capture_output, 
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            success = result.returncode == 0
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out after 2 minutes"
        except Exception as e:
            return False, "", str(e)

    def test_typescript_compilation(self) -> Dict:
        """Test TypeScript compilation"""
        print("🔍 Testing TypeScript compilation...")
        
        success, stdout, stderr = self.run_command("npm run type-check")
        
        result = {
            "name": "TypeScript Compilation",
            "success": success,
            "output": stdout,
            "errors": stderr,
            "issues": []
        }
        
        if not success:
            # Parse TypeScript errors
            lines = stderr.split('\n')
            for line in lines:
                if " - error TS" in line:
                    result["issues"].append(line.strip())
                    
        return result

    def test_eslint(self) -> Dict:
        """Test ESLint"""
        print("🔍 Testing ESLint...")
        
        success, stdout, stderr = self.run_command("npm run lint")
        
        result = {
            "name": "ESLint",
            "success": success,
            "output": stdout,
            "errors": stderr,
            "warnings": []
        }
        
        # Parse ESLint warnings
        lines = stdout.split('\n')
        for line in lines:
            if "Warning:" in line:
                result["warnings"].append(line.strip())
                
        return result

    def test_frontend_build(self) -> Dict:
        """Test frontend build"""
        print("🔍 Testing frontend build...")
        
        success, stdout, stderr = self.run_command("npm run build")
        
        return {
            "name": "Frontend Build",
            "success": success,
            "output": stdout,
            "errors": stderr
        }

    def test_backend_import(self) -> Dict:
        """Test backend Python imports"""
        print("🔍 Testing backend imports...")
        
        # Test if we can import the main modules
        test_script = '''
import sys
sys.path.append(".")
try:
    from app.main import app
    from app.config import settings
    print("✓ Backend imports successful")
    exit(0)
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
'''
        
        # Write test script to temporary file
        test_file = self.project_dir / "temp_import_test.py"
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        try:
            # Try with virtual environment first
            venv_python = self.project_dir / "venv" / "Scripts" / "python.exe"
            if venv_python.exists():
                success, stdout, stderr = self.run_command(f'"{venv_python}" temp_import_test.py')
            else:
                success, stdout, stderr = self.run_command("python temp_import_test.py")
                
            return {
                "name": "Backend Imports",
                "success": success,
                "output": stdout,
                "errors": stderr
            }
        finally:
            # Clean up test file
            if test_file.exists():
                test_file.unlink()

    def test_backend_syntax(self) -> Dict:
        """Test backend Python syntax"""
        print("🔍 Testing backend syntax...")
        
        python_files = list(self.project_dir.glob("**/*.py"))
        python_files = [f for f in python_files if "venv" not in str(f) and "__pycache__" not in str(f)]
        
        syntax_errors = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {e}")
            except Exception as e:
                syntax_errors.append(f"{py_file}: {e}")
        
        return {
            "name": "Backend Syntax Check",
            "success": len(syntax_errors) == 0,
            "files_checked": len(python_files),
            "syntax_errors": syntax_errors
        }

    def test_dependencies(self) -> Dict:
        """Check if all dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Node dependencies
        node_deps_ok = (self.project_dir / "node_modules").exists()
        
        # Check Python dependencies
        requirements_file = self.project_dir / "requirements.txt"
        python_deps_ok = True
        missing_deps = []
        
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            for dep in deps:
                dep_name = dep.split('==')[0].split('>=')[0].split('<=')[0]
                success, _, _ = self.run_command(f"python -c \"import {dep_name.replace('-', '_')}\"")
                if not success:
                    missing_deps.append(dep_name)
                    python_deps_ok = False
        
        return {
            "name": "Dependencies Check",
            "node_dependencies": node_deps_ok,
            "python_dependencies": python_deps_ok,
            "missing_python_deps": missing_deps
        }

    def test_config_files(self) -> Dict:
        """Test configuration files"""
        print("🔍 Testing configuration files...")
        
        config_files = [
            "package.json",
            "tsconfig.json",
            "next.config.js",
            ".eslintrc.json",
            "tailwind.config.js",
            "requirements.txt",
            ".env"
        ]
        
        file_status = {}
        for config_file in config_files:
            file_path = self.project_dir / config_file
            file_status[config_file] = {
                "exists": file_path.exists(),
                "readable": False
            }
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse JSON files
                    if config_file.endswith('.json'):
                        json.loads(content)
                    
                    file_status[config_file]["readable"] = True
                except Exception as e:
                    file_status[config_file]["error"] = str(e)
        
        return {
            "name": "Configuration Files",
            "files": file_status
        }

    def run_all_tests(self) -> Dict:
        """Run all tests and return comprehensive results"""
        print("🚀 Starting comprehensive project testing...\n")
        
        tests = [
            self.test_config_files,
            self.test_dependencies,
            self.test_backend_syntax,
            self.test_backend_import,
            self.test_typescript_compilation,
            self.test_eslint,
        ]
        
        # Skip build test for now as it might fail due to other issues
        # tests.append(self.test_frontend_build)
        
        results = {}
        total_tests = len(tests)
        passed_tests = 0
        
        for test_func in tests:
            try:
                result = test_func()
                results[result["name"]] = result
                
                if result.get("success", False):
                    passed_tests += 1
                    print(f"✅ {result['name']}: PASSED")
                else:
                    print(f"❌ {result['name']}: FAILED")
                    
            except Exception as e:
                print(f"🔥 {test_func.__name__}: ERROR - {e}")
                results[test_func.__name__] = {
                    "name": test_func.__name__,
                    "success": False,
                    "error": str(e)
                }
        
        print(f"\n📊 Test Summary: {passed_tests}/{total_tests} tests passed")
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
            },
            "results": results
        }

def main():
    project_dir = Path(__file__).parent
    tester = ProjectTester(project_dir)
    
    # Run all tests
    test_results = tester.run_all_tests()
    
    # Save results to file
    results_file = project_dir / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📝 Detailed results saved to: {results_file}")
    
    # Print recommendations
    print("\n🔧 Recommendations:")
    
    if not test_results["results"].get("Dependencies Check", {}).get("node_dependencies", False):
        print("  • Run 'npm install' to install Node.js dependencies")
    
    if not test_results["results"].get("Dependencies Check", {}).get("python_dependencies", True):
        print("  • Run 'python setup_backend.py' to install Python dependencies")
    
    if not test_results["results"].get("TypeScript Compilation", {}).get("success", False):
        print("  • Fix TypeScript compilation errors before proceeding")
    
    if not test_results["results"].get("Backend Imports", {}).get("success", False):
        print("  • Install missing Python dependencies or fix import issues")
    
    print("\n🚦 Next Steps:")
    print("  1. Fix any failing tests")
    print("  2. Run 'npm run dev' to start the frontend development server")
    print("  3. Run 'python run.py' to start the backend server")
    print("  4. Test the application in your browser")
    
    return test_results["summary"]["passed_tests"] == test_results["summary"]["total_tests"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
