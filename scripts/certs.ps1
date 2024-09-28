mkdir .certs
Set-Location .certs

& openssl genrsa -out jwt_private.pem 2048
& openssl rsa -in jwt_private.pem -outform PEM -pubout -out jwt_public.pem

Set-Location ..

Write-Host 'The keys were successfully created'