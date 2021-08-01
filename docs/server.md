# pman server docs
`pman` uses a standard http server to serve packages and the package index. Servers must support https.  

## package index
The package index is a simple JSON file, located at `<repo-directory>/packages.json` on the webserver. The file follows this format:  
```
{
    "package-name": {
        "path": "https://example.com/pman/package-name.zip",
        "platform": "linux",
        "version": "1.0.0",
        "depends": ["other-package-name"]
    }, "other-package-name": {
        "path": "https://example.com/pman/other-package-name.zip",
        "platform": "all",
        "version": "0.6.9",
        "depends": []
    }, ...
}
```
Version numbers must only consist of integers and decimal places.
## package files
Package files are stored in .zip files. Packages must have the executable file in the root of the packages folder, and must be able to find their own files in the directory pointed to by `PMAN_PACKAGES`. 