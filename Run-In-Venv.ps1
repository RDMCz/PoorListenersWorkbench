if ([System.IO.File]::Exists("${PSScriptRoot}\.venv\pyvenv.cfg")) {
    Write-Host "venv found"

    .venv\Scripts\activate

    .\main.py
}
else {
    Write-Host "venv not found"

    py -m venv .venv

    .venv\Scripts\activate

    pip install -r .\requirements.txt

    .\main.py
}
