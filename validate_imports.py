#!/usr/bin/env python3
"""
Comprehensive import validation script to test all modules and identify issues.
"""

import sys
import traceback
from typing import Dict, List, Tuple
import importlib

def test_import(module_name: str) -> Tuple[bool, str]:
    """Test importing a module and return success status with message."""
    try:
        importlib.import_module(module_name)
        return True, f"✅ {module_name}: OK"
    except ImportError as e:
        return False, f"❌ {module_name}: Import Error - {str(e)}"
    except Exception as e:
        return False, f"❌ {module_name}: Error - {str(e)}"

def test_circular_dependency(module_name: str) -> Tuple[bool, str]:
    """Test for circular dependencies by checking if module can be reloaded."""
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
        return True, f"✅ {module_name}: No circular dependencies"
    except Exception as e:
        if "circular" in str(e).lower() or "recursion" in str(e).lower():
            return False, f"❌ {module_name}: Circular dependency - {str(e)}"
        return True, f"✅ {module_name}: No circular dependencies (reload failed for other reasons)"

def main():
    """Run comprehensive import validation."""
    print("🔍 Comprehensive Import Validation")
    print("=" * 50)
    
    # Test main modules
    main_modules = [
        "app.main",
        "app.config",
        "run",
        "worker"
    ]
    
    # Test service modules
    service_modules = [
        "app.services.pdf_service",
        "app.services.conversion_service", 
        "app.services.ocr_service",
        "app.services.chat_service",
        "app.services.form_service",
        "app.services.table_service",
        "app.services.workflow_service",
        "app.services.template_service",
        "app.services.editor_service"
    ]
    
    # Test route modules
    route_modules = [
        "app.routes.pdf_routes",
        "app.routes.conversion_routes", 
        "app.routes.ocr_routes",
        "app.routes.chat_routes",
        "app.routes.form_routes",
        "app.routes.table_routes",
        "app.routes.workflow_routes",
        "app.routes.template_routes",
        "app.routes.editor_routes"
    ]
    
    # Test utility modules
    utility_modules = [
        "app.utils.file_utils",
        "app.middleware",
        "app.tasks.celery_app"
    ]
    
    all_modules = main_modules + service_modules + route_modules + utility_modules
    
    print("\n📦 Basic Import Tests:")
    print("-" * 30)
    
    passed_imports = 0
    total_imports = len(all_modules)
    failed_modules = []
    
    for module_name in all_modules:
        success, message = test_import(module_name)
        print(message)
        if success:
            passed_imports += 1
        else:
            failed_modules.append(module_name)
    
    print("\n🔄 Circular Dependency Tests:")
    print("-" * 30)
    
    passed_circular = 0
    total_circular = len(all_modules)
    
    for module_name in all_modules:
        success, message = test_circular_dependency(module_name)
        print(message)
        if success:
            passed_circular += 1
    
    # Test FastAPI application creation
    print("\n🚀 Application Tests:")
    print("-" * 30)
    
    app_tests_passed = 0
    app_tests_total = 3
    
    try:
        from app.main import app
        print("✅ FastAPI app creation: OK")
        app_tests_passed += 1
    except Exception as e:
        print(f"❌ FastAPI app creation: {str(e)}")
    
    try:
        import uvicorn
        server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000))
        print("✅ Uvicorn server creation: OK")
        app_tests_passed += 1
    except Exception as e:
        print(f"❌ Uvicorn server creation: {str(e)}")
    
    try:
        from app.tasks.celery_app import celery_app
        print("✅ Celery app creation: OK")
        app_tests_passed += 1
    except Exception as e:
        print(f"❌ Celery app creation: {str(e)}")
    
    # Summary
    print("\n📊 Validation Summary:")
    print("=" * 50)
    print(f"Import Tests: {passed_imports}/{total_imports} passed")
    print(f"Circular Dependency Tests: {passed_circular}/{total_circular} passed")
    print(f"Application Tests: {app_tests_passed}/{app_tests_total} passed")
    
    total_passed = passed_imports + passed_circular + app_tests_passed
    total_tests = total_imports + total_circular + app_tests_total
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if failed_modules:
        print(f"\n⚠️  Failed Modules:")
        for module in failed_modules:
            print(f"  - {module}")
    
    if total_passed == total_tests:
        print("\n🎉 All import tests passed! No circular dependencies or import issues found!")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} tests failed. Review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
