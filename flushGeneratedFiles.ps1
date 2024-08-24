
# flushGeneratedFiles
# by Drew Wingfield
# Created on August 24th, 2024
# This is file for me to use for debugging. It flushes all generated files (except ones ending in .log) as well as pycache files

Remove-Item app/generatedfiles -Exclude *.log -Recurse
Remove-Item app/__pycache__ -Recurse
