# -------------------------------
# PowerShell script to install OpenSSL and create a self-signed cert
# -------------------------------

# Variables
$installDir = "C:\Program Files\OpenSSL-Win64"


$certDir = ".\certs"
$certFile = "$certDir\server.crt"
$keyFile = "$certDir\server.key"

# Create cert directory if not exists
if (!(Test-Path $certDir)) {
    New-Item -Path $certDir -ItemType Directory | Out-Null
}

# Download OpenSSL Light installer
# Write-Host "Downloading OpenSSL..."
# Invoke-WebRequest -Uri "https://slproweb.com/download/Win64OpenSSL_Light-3_1_2.msi" -OutFile $opensslInstaller

# Install OpenSSL silently
# Write-Host "Installing OpenSSL to $installDir..."
# Start-Process msiexec.exe -Wait -ArgumentList "/i `"$opensslInstaller`" /qn INSTALLDIR=`"$installDir`" ADDLOCAL=ALL"

# Add OpenSSL to PATH if not already
if (-not ($env:PATH -like "*$installDir\bin*")) {
    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$installDir\bin", [EnvironmentVariableTarget]::Machine)
    Write-Host "Added OpenSSL to system PATH. You may need to restart PowerShell."
}

# Generate self-signed certificate
Write-Host "Generating self-signed certificate in $certDir..."
& "$installDir\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout $keyFile -out $certFile -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Org/OU=Unit/CN=localhost"

Write-Host "Done!"
Write-Host "Certificate: $certFile"
Write-Host "Private Key: $keyFile"
