#!/usr/bin/env python3
"""
Setup script for Tools Website backend dependencies
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        print(f"✓ Successfully ran: {command}")
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def main():
    print("Setting up Tools Website backend environment...")
    
    # Get current directory
    project_dir = Path(__file__).parent
    print(f"Project directory: {project_dir}")
    
    # Check if virtual environment exists
    venv_path = project_dir / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        if not run_command(f"python -m venv venv", cwd=project_dir):
            print("Failed to create virtual environment")
            return False
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/Linux/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    print(f"Using pip at: {pip_path}")
    
    # Install requirements
    requirements_file = project_dir / "requirements.txt"
    if requirements_file.exists():
        print("Installing Python dependencies...")
        if not run_command(f'"{pip_path}" install -r requirements.txt', cwd=project_dir):
            print("Failed to install requirements")
            return False
    else:
        print("requirements.txt not found, installing basic dependencies...")
        basic_deps = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "python-dotenv==1.0.0",
            "python-multipart==0.0.6",
            "pytest==7.4.3",
            "httpx==0.25.2"
        ]
        
        for dep in basic_deps:
            if not run_command(f'"{pip_path}" install {dep}', cwd=project_dir):
                print(f"Failed to install {dep}")
                return False
    
    print("\n✓ Backend setup completed successfully!")
    print("\nTo activate the virtual environment:")
    if os.name == 'nt':
        print(f"  {venv_path}\\Scripts\\activate")
    else:
        print(f"  source {venv_path}/bin/activate")
    
    print("\nTo start the backend server:")
    print("  python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
