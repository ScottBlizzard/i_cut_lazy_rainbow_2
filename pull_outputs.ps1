# pull_outputs.ps1 - pull experiment outputs from server to local outputs\
# Usage:
#   ./pull_outputs.ps1              # pull from 4090 server
#   ./pull_outputs.ps1 -Server A40  # pull from A40 server

param(
    [ValidateSet("4090", "A40")]
    [string]$Server = "4090"
)

$ErrorActionPreference = "Stop"

$LocalOut = Join-Path $PSScriptRoot "outputs"
New-Item -ItemType Directory -Force $LocalOut | Out-Null

if ($Server -eq "4090") {
    $Remote = "ccj@10.10.217.244:/home/ccj/workspace_1/iclr_2/outputs/*"
    Write-Host "==> pulling 4090 outputs -> $LocalOut"
    scp $Remote $LocalOut
}
else {
    $Remote = "root@10.91.11.250:/workspace/thymic_project/paper/iclr_2/outputs/*"
    Write-Host "==> pulling A40 outputs -> $LocalOut"
    scp -P 10008 $Remote $LocalOut
}

Write-Host "==> done."

