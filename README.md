## How to run the SBOM script:
- Run main.py in CMD and add the path at the end.

Example: "python3 main.py /home/alice/code/repos/" or "python3 main.py /users/bob/code/repos"

With or without "/" at the end, it will still work.

- This script only needs main.py and nothing else.

## Assumptions:
- The SBOM files is created and saved in the root directory "The directory path that was written in when launching the script". Although it is not hard to change it to SBOM for every repository with the way the coding is structured.
- The devDependencies is also added into the SBOM
