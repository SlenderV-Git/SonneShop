if (-not (Test-Path -Path ".certs")) {
    New-Item -ItemType Directory -Path ".certs"
    Write-Host "The .certs directory has been created."
} else {
    Write-Host "The .certs directory already exists."
}
Set-Location .certs

& openssl genpkey -algorithm RSA -out signature_private.pem -pkeyopt rsa_keygen_bits:2048

Set-Location ..

Write-Host 'The signature keys were successfully created'
