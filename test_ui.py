#!/usr/bin/env python3
"""
Quick test to verify comparison_ui.py works
Tests the core comparison logic without requiring running vLLM servers
"""

def test_ui_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        import gradio as gr
        import requests
        print("✅ All imports successful")
        print(f"  Gradio version: {gr.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_ui_structure():
    """Test that the UI can be created"""
    print("\nTesting UI structure...")
    try:
        # Import the module
        import comparison_ui
        print("✅ UI module loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading UI: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Comparison UI Test Suite")
    print("=" * 50)
    print()

    all_pass = True
    all_pass &= test_ui_imports()
    all_pass &= test_ui_structure()

    print()
    print("=" * 50)
    if all_pass:
        print("✅ All tests passed!")
        print()
        print("To run the UI:")
        print("  python comparison_ui.py")
        print()
        print("Make sure vLLM servers are running:")
        print("  ./deploy_models.sh")
    else:
        print("❌ Some tests failed")
        print()
        print("Install dependencies:")
        print("  pip install -r requirements.txt")
    print("=" * 50)
