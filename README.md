# pman
`pman` is a small, portable, cross-platform package manager written in Python.

## Note
`pman` is not ready for use yet (alpha, core features are buggy and advanced features are not implemented yet)

## Why another package manager?
As far as I know, there are no truly "cross-platform" package managers. `apt`, `pacman`, `zypper`, and the like only work well on Linux (although `apt` is also used in iOS jailbreaking) and `brew` only works on *nix OSes. `pman` is not only cross-platform, but it's also portable - you can move your installation (including repos and installed packages) across two machines very easily, and it will just work. Any packages that are cross-platform (for example, packages written in Python or Java) will even work across operating systems.

## Installation (*nix)
Installation on *nix OSes does not require root permissions.
1. Download and extract `pman` to a directory with write permissions.
2. Add the directory containing `pman`, as well as the `packages` subdirectory, to your PATH.
3. Create a new environment variable called `PMAN_PACKAGES` containing the path to the `packages` subdirectory.

## Installation (Windows)
Installation on Windows requires administrator permissions.
1. Download and extract `pman` to a directory with write permissions.
2. Run the command `Set-ExecutionPolicy RemoteSigned -Scope LocalMachine` in PowerShell as administrator.
3. Run the command `Test-Path $Profile` in PowerShell.
4. (if command returned `False`) Run the command `New-Item –Path $Profile –Type File –Force` in PowerShell.
5. Run the command `notepad $Profile` in PowerShell.
6. In the Notepad window that opens, add the command `Set-Alias -Name pman -Value python3 <pman-path>\pman.py` to the end, replacing `<pman-path>` with the path to your `pman` installation.
7. Add the `packages` subdirectory to your PATH.
8. Create a new environment variable called `PMAN_PACKAGES` containing the path to the `packages` subdirectory.
9. Restart PowerShell.

## Features
- Load repositories and package lists from disk.
- Download and import package lists from servers.
- Download and update packages from servers
- Uninstall installed packages

## Planned features
- Add repos from command line
- Option to update and then run packages (intended to update GUI of an embedded device before it finishes booting)

## Design Goals 
- Allow the same script to run on all supported OSes (Windows, GNU/Linux, etc...)
- Allow one repository to host packages for multiple OSes and CPU architectures at the same time
- System-wide (with root/administrator) or single-user (no root/administrator) package installation
- Only use libraries already in the Python standard library

## Security Design
`pman` relies on HTTPS to ensure traffic is not tampered with. Routing traffic through HTTP only is not supported.

## Security Goals
Also have `pman` verify GPG signatures on files to help prevent server-side tampering. Ideally public keys should be downloaded once, when we first see the repo in `repos.json`