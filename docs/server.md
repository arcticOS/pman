# pman server docs
`pman` uses a standard http server to serve packages and the package index. Servers must support https.  

## package index
The package index is a simple JSON file, located at `<repo-directory>/packages.json` on the webserver. The file follows this format:  
```
{
    "package-name": {
        "path": "https://example.com/pman/package-name.zip",
        "platform": "unix",
        "version": "1.0.0-unix"
    }, "other-package-name": {
        "path": "https://example.com/pman/other-package-name.zip",
        "platform": "all",
        "version": "0.6.9-nice"
    }, ...
}
```

## package files
Package files are stored in .zip files. Packages must either have a wrapper (a simple shell/batch file will do) that changes into a directory with the package name or support loading needed files from a dedicated subdirectory. The .zip layout is as follows:

Dedicated subdirectory:
```
package.zip
    |
    |-package <- Data directory
    |   |-some-required-file.txt
    |   \-some-other-required-file.jpg
    \-package.exe <- Executable
```

Wrapper:
```
package.zip
    |
    |-package <- Data directory
    |   |-some-required-file.txt
    |   |-some-other-required-file.jpg
    |   \-package.exe <- Executable
    \-package.bat <- Wrapper
```
`package.bat` in this case would look something like:
```sh
@echo off
cd package
package.exe
```