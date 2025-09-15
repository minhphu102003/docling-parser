# PowerShell script to replicate Makefile functionality for docling-parser project

function Show-Help {
    Write-Host "Available targets:"
    Write-Host "  install     Install dependencies using uv"
    Write-Host "  sync        Sync dependencies using uv"
    Write-Host "  format      Format code with black and isort"
    Write-Host "  lint        Check code style with flake8"
    Write-Host "  test        Run tests"
    Write-Host "  clean       Clean up generated files"
    Write-Host "  help        Show this help message"
}

function Invoke-Install {
    Write-Host "Installing dependencies using uv..."
    uv pip install -e .
}

function Invoke-Sync {
    Write-Host "Syncing dependencies using uv..."
    uv sync
}

function Invoke-Format {
    Write-Host "Formatting code with black and isort..."
    python -m black .
    python -m isort .
}

function Invoke-Lint {
    Write-Host "Checking code style with flake8..."
    python -m flake8 .
}

function Invoke-Test {
    Write-Host "Running tests..."
    python -m pytest
}

function Invoke-Clean {
    Write-Host "Cleaning up..."
    
    # Remove __pycache__ directories
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
        Remove-Item -Recurse -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove .pytest_cache directories
    Get-ChildItem -Path . -Recurse -Directory -Name ".pytest_cache" | ForEach-Object {
        Remove-Item -Recurse -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove .pyc files
    Get-ChildItem -Path . -Recurse -Name "*.pyc" | ForEach-Object {
        Remove-Item -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove .pyo files
    Get-ChildItem -Path . -Recurse -Name "*.pyo" | ForEach-Object {
        Remove-Item -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove ~ files
    Get-ChildItem -Path . -Recurse -Name "*~" | ForEach-Object {
        Remove-Item -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove .*~ files
    Get-ChildItem -Path . -Recurse -Name ".*~" | ForEach-Object {
        Remove-Item -Force $_
        Write-Host "Removed $_"
    }
    
    # Remove coverage files and directories
    if (Test-Path ".coverage") {
        Remove-Item -Force ".coverage"
        Write-Host "Removed .coverage"
    }
    
    if (Test-Path "htmlcov") {
        Remove-Item -Recurse -Force "htmlcov"
        Write-Host "Removed htmlcov directory"
    }
    
    if (Test-Path ".mypy_cache") {
        Remove-Item -Recurse -Force ".mypy_cache"
        Write-Host "Removed .mypy_cache directory"
    }
}

# Main script logic
if ($args.Count -eq 0) {
    Show-Help
    exit 0
}

$target = $args[0].ToLower()

switch ($target) {
    "help" { Show-Help }
    "install" { Invoke-Install }
    "sync" { Invoke-Sync }
    "format" { Invoke-Format }
    "lint" { Invoke-Lint }
    "test" { Invoke-Test }
    "clean" { Invoke-Clean }
    default { 
        Write-Host "Unknown target: $target"
        Show-Help
        exit 1
    }
}