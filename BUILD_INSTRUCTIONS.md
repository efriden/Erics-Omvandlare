# Building Erics-Omvandlare as Portable Executable

This document explains how to build Erics-Omvandlare as a single, portable .exe file that includes all dependencies including pandoc.

## What You Get

The portable executable includes:
- ✅ Your Python application
- ✅ Python interpreter 
- ✅ All Python dependencies (pypandoc, tkinter, etc.)
- ✅ Pandoc executable (no separate installation needed)
- ✅ Single .exe file (~48MB)
- ✅ No installation required for end users
- ✅ Works on any Windows machine without Python

## Prerequisites

- Python 3.11+ installed on Windows
- All project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller (`pip install pyinstaller`)

## Build Process

### Automatic Build (Recommended)

Simply run the build script:

```batch
.\build_portable.bat
```

This script will:
1. Check for PyInstaller and install if needed
2. Verify pandoc.exe is available
3. Clean previous builds
4. Install/verify dependencies
5. Build the executable using PyInstaller
6. Offer to test the result

### Manual Build

If you prefer to build manually:

```batch
# Install dependencies
py -m pip install -r requirements.txt
py -m pip install pyinstaller

# Build the executable
py -m PyInstaller --clean build_portable.spec
```

The executable will be created at `dist\Erics-Omvandlare.exe`.

## Files Involved in Build

| File | Purpose |
|------|---------|
| `build_portable.spec` | PyInstaller configuration file |
| `build_portable.bat` | Automated build script |
| `tools/pandoc.exe` | Pandoc executable (bundled into .exe) |
| `src/pandoc_setup.py` | Runtime pandoc path configuration |

## Testing the Executable

### Quick Test
Double-click `dist\Erics-Omvandlare.exe` to launch the GUI.

### Comprehensive Test
Run the test script in development:
```batch
py test_portable.py
```

## Distribution

The portable executable is completely self-contained. You can:

1. **Copy the single .exe file** to any location
2. **Share via email, USB, cloud storage**, etc.
3. **No installation needed** on target machines
4. **Works on Windows 10/11** without any setup

## Technical Details

### How Pandoc Bundling Works

1. **Download**: Pandoc executable is downloaded to `tools/pandoc.exe`
2. **Bundle**: PyInstaller includes it in the .exe package
3. **Runtime**: `pandoc_setup.py` detects if running as bundled executable
4. **Path Setup**: Sets `PYPANDOC_PANDOC` environment variable to bundled pandoc

### File Structure in Bundled .exe

```
Erics-Omvandlare.exe (contains):
├── Python interpreter and libraries
├── Your application source code
├── pypandoc and other dependencies
└── pandoc.exe (automatically located at runtime)
```

## Troubleshooting

### Build Fails
- Ensure Python is installed and `py` command works
- Check that `tools/pandoc.exe` exists
- Run `py -m pip install -r requirements.txt`

### Executable Doesn't Run
- Try running from command line to see error messages
- Check Windows antivirus isn't blocking the .exe
- Verify the build completed without errors

### Pandoc Not Found in Executable
- Check that `tools/pandoc.exe` was included during build
- Verify `pandoc_setup.py` is correctly imported in your entry points
- Test with the `test_portable.py` script first

### "No module named pandoc" Error
This was fixed in the current build system by:
- Adding custom PyInstaller hooks in `hooks/hook-pypandoc.py`
- Using `sys._MEIPASS` to locate bundled pandoc in temporary directory
- Adding proper hidden imports in the spec file

### Debug Mode
If issues persist, build the debug version:
```batch
py -m PyInstaller --clean build_debug.spec
```
This creates `Erics-Omvandlare-Debug.exe` with console output for troubleshooting.

## File Size Optimization

The current build (~48MB) includes:
- Python interpreter: ~30MB
- Pandoc executable: ~208MB (compressed in .exe)
- Your code + dependencies: ~10MB

This is reasonable for a fully self-contained application. If size is critical:
1. Consider using pandoc as external dependency
2. Use PyInstaller exclusion options for unused modules
3. Enable UPX compression (already enabled in spec file)

## Security Considerations

- The .exe may trigger antivirus warnings (false positive)
- Users might need to approve execution for unknown publishers
- Consider code signing for production distribution

## Building for Different Versions

To bundle a different pandoc version:
1. Download desired pandoc release
2. Replace `tools/pandoc.exe`
3. Rebuild with `.\build_portable.bat`
