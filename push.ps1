# push.ps1 - sync local src\ to an experiment server via scp
# Usage:
#   ./push.ps1              # push to 4090 server
#   ./push.ps1 -Server A40  # push to A40 server
# Local d:\ICLR_2\src is the master copy; each push wipes and replaces server src.
# Put experiment outputs under iclr_2/outputs (outside src) so they are NOT wiped.

param(
    [ValidateSet("4090", "A40")]
    [string]$Server = "4090"
)

$ErrorActionPreference = "Stop"

if ($Server -eq "4090") {
    $SshTarget = "ccj@10.10.217.244"
    $SshArgs = @()
    $ScpArgs = @("-r")
    $RemoteDir = "/home/ccj/workspace_1/iclr_2"
}
else {
    $SshTarget = "root@10.91.11.250"
    $SshArgs = @("-p", "10008")
    $ScpArgs = @("-P", "10008", "-r")
    $RemoteDir = "/workspace/thymic_project/paper/iclr_2"
}

$RemoteSrc = "$RemoteDir/src"
$LocalSrc  = Join-Path $PSScriptRoot "src"

if (-not (Test-Path $LocalSrc)) {
    Write-Error "Local src folder not found: $LocalSrc"
    exit 1
}

Write-Host "==> wiping and recreating remote $RemoteSrc"
& ssh @SshArgs $SshTarget "rm -rf $RemoteSrc && mkdir -p $RemoteSrc"

# cd into src and use RELATIVE names, otherwise Windows scp treats the "D:" drive
# letter as a remote host (the colon ambiguity).
Push-Location $LocalSrc
try {
    $items = @(Get-ChildItem -Force | Where-Object { $_.Name -ne '__pycache__' } | ForEach-Object { $_.Name })
    if ($items.Count -eq 0) {
        Write-Host "src is empty, nothing to push."
        exit 0
    }
    Write-Host "==> pushing $($items.Count) item(s) -> ${SshTarget}:$RemoteSrc/"
    $ScpFullArgs = $ScpArgs + $items + @("${SshTarget}:$RemoteSrc/")
    & scp @ScpFullArgs
}
finally {
    Pop-Location
}

Write-Host "==> done. latest code at ${SshTarget}:$RemoteSrc"
