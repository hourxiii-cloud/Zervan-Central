# Zervan v47.8 GitHub upload jobs (ordered A → B → C → D)

Each ZIP is below the GitHub browser upload limit shown in the screenshot. Upload and commit these four ZIP files in order: A, then B, then C, then D. Do not rename them. Each is an opaque contiguous byte-range of the same frozen archive with its own SHA-256 metadata.

After all four commits are present in the Codespace, create a working directory and extract Job A there to obtain the assembly manifest and script. Keep all four job ZIP files in that same directory, then run:

```bash
python3 assemble_abcd.py .
```

The script validates each part, concatenates strictly A→B→C→D, checks the complete archive byte count, SHA-256, SHA-512, and ZIP CRC, and writes the exact final archive only after every check passes. Then extract the resulting clean-full-freeze ZIP to inspect the package. The assembler performs no Git commit or push.
