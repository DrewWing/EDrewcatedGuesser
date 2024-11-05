<#
.SYNOPSIS
    This script is temporary and for debug. 
    
.DESCRIPTION
    Flushes all generated files (except ones ending in .log) as well as pycache files.
    
    Created on August 24th, 2024

    AUTHOR: Drew Wingfield
    VERSION: 48.0
    COPYRIGHT: 
        This script is part of Drew Wingfield's EDrewcated Guesser.
        It is licensed under the license found at LICENSE.txt.
        See the documentation in the README.md file.

#>

Remove-Item app/generatedfiles -Exclude *.log -Recurse
Remove-Item app/__pycache__ -Recurse
