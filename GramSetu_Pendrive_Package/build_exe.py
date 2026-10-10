import os
import sys
import subprocess

def build_executable():
    print("=" * 60)
    print("🌾 GramSetu AI - Standalone Executable (.exe) Builder")
    print("=" * 60)
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is found.")
    except ImportError:
        print("⚡ Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define files and folders to bundle
    data_files = [
        ("index.html", "."),
        ("app.js", "."),
        ("styles.css", "."),
        ("knowledge_data.js", "."),
        ("gramsetu.db", "."),
        ("manifest.json", "."),
        ("sw.js", "."),
        ("icon-192.png", "."),
        ("icon-512.png", "."),
        ("docs.html", "."),
        ("docs_en.html", "."),
        ("qa100.html", "."),
        ("presentation_summary.html", "."),
        ("print_project_plan.html", "."),
        ("PROJECT_PLAN.md", "."),
        ("core", "core"),
        ("ai", "ai"),
        ("tools", "tools"),
        ("rag", "rag"),
    ]

    add_data_args = []
    sep = ";" if os.name == 'nt' else ":"
    for src, dst in data_files:
        if os.path.exists(src):
            add_data_args.extend(["--add-data", f"{src}{sep}{dst}"])

    icon_arg = []
    if os.path.exists("icon-512.png"):
        icon_arg = ["--icon", "icon-512.png"]

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=GramSetuAI",
        "--onefile",
        "--noconfirm",
        "--clean",
        *icon_arg,
        *add_data_args,
        "server.py"
    ]

    print("⚡ Building standalone executable...")
    subprocess.check_call(pyinstaller_cmd)
    
    print("\n" + "=" * 60)
    print("✅ Build Successful!")
    if os.name == 'nt':
        print("🎉 Your Windows executable is located at: dist\\GramSetuAI.exe")
    else:
        print("🎉 Your executable is located at: dist/GramSetuAI")
    print("=" * 60)

if __name__ == "__main__":
    build_executable()
