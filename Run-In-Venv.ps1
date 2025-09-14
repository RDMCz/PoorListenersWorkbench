if ([System.IO.File]::Exists("${PSScriptRoot}\.venv\pyvenv.cfg")) {
    Write-Host "Python virtual environment .venv found`nLaunching..." -NoNewline

    .venv\Scripts\activate

    .\main.py
}
else {
    Write-Host "Python virtual environment .venv not found`nCreating .venv..." -NoNewline

    py -m venv .venv

    .venv\Scripts\activate

    pip install -r .\requirements.txt

    .\main.py
}
