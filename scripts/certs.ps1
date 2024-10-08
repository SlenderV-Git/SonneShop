if (-not (Test-Path -Path ".certs")) {
    New-Item -ItemType Directory -Path ".certs"
    Write-Host "The .certs directory has been created."
} else {
    Write-Host "The .certs directory already exists."
}
Set-Location .certs

& openssl genrsa -out jwt_private.pem 2048
& openssl rsa -in jwt_private.pem -outform PEM -pubout -out jwt_public.pem

Set-Location ..

Write-Host 'The jwt keys were successfully created'