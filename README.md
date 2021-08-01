# pman
pman is a small cross-platform package manager written in Python.

## Installation (*nix)
Installation on *nix OSes does not require root permissions.
1. Download and extract pman to a directory with write permissions.
2. Add the directory containing pman, as well as the `packages` subdirectory, to your PATH.

## Installation (Windows)
Installation on Windows requires administrator permissions.
1. Download and extract pman to a directory with write permissions.
2. Run the command `Set-ExecutionPolicy RemoteSigned -Scope LocalMachine` in PowerShell as administrator.
3. Run the command `Test-Path $Profile` in PowerShell.
4. (if command returned `False`) Run the command `New-Item –Path $Profile –Type File –Force` in PowerShell.
5. Run the command `notepad $Profile` in PowerShell.
6. In the Notepad window that opens, add the command `Set-Alias -Name pman -Value python3 <pman-path>\pman.py` to the end, replacing `<pman-path>` with the path to your pman installation.
7. Restart PowerShell.

## Design Goals 
- Allow the same script to run on all supported OSes (Windows, GNU/Linux, etc...)
- Allow one repository to host packages for multiple OSes and CPU architectures at the same time
- System-wide (with root/administrator) or single-user (no root/administrator) package installation
- Only use libraries already in the Python standard library

## Security Design
pman relies on HTTPS to ensure traffic is not tampered with. Routing traffic through HTTP only is not supported.
Ideally pman will use GPG signatures before v1.