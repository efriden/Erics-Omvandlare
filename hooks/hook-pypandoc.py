# PyInstaller hook file for pypandoc
# This ensures pypandoc is properly bundled with all its dependencies

from PyInstaller.utils.hooks import collect_all

# Collect everything from pypandoc
datas, binaries, hiddenimports = collect_all('pypandoc')

# Add specific hidden imports that might be missed
hiddenimports += [
    'pypandoc.pandoc_download',
    'urllib.request',
    'urllib.parse',
    'urllib.error',
]
