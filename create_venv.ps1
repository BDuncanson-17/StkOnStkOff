param(
    [Parameter(Mandatory=$false)]
    [Alias("-m")]
    [Switch]$Make,

    [Parameter(Mandatory=$false)]
    [Alias("-d")]
    [Switch]$Delete
)

if ($Make) {
    # Create the virtual environment
    & python -m venv .venv
    & .venv\Scripts\Activate.ps1
    exit 0
}
elseif ($Delete) {
    # Delete the virtual environment
    if (Test-Path ".venv") {
        Remove-Item -Path ".venv" -Recurse -Force
        Write-Host "Virtual environment '.venv' deleted."
    }
    else {
        Write-Host "Virtual environment '.venv' not found."
    }
    exit 0
}
else {
    Write-Host "No valid option provided. Please use either -m or -d."
    exit 1
}
