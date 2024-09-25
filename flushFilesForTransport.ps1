
# flushFilesForTransport
# by Drew Wingfield
# Copied from flushGeneratedFiles.ps1 on September 24th, 2024
# by Drew Wingfield

# This script is to be used when transporting the project. It removes the virtual environment,
# cache files, and other unnecessary or large files/folders we can regenerate later.

Write-Output "Removing files..."

Remove-Item app/generatedfiles -Exclude *.log -Recurse
Remove-Item app/__pycache__ -Recurse
Remove-Item app/tests/__pycache__ -Recurse

Remove-Item .venv -Recurse

Write-Output "Done removing files."
