# RAGAR - The Development Language (v0.1.2)

RAGAR is a lightweight, interpreted programming language designed for simplicity and flexibility. It features a custom syntax, built-in functions, and modular capabilities. The language is currently under active development.

## New Features in v0.1.2

**Libraries Added:**
- _built_in
- _built_out
- _std_in
- _std_out
- _object

**New File Extension:**  
`.rgr`

**New Keywords:**
- `include` ← / →: Specify a module to use in the next or previous class.
- `included`: Refers to another module included by the `include` statement for use in the next class.
- `define`: Define a module to be called.
- `defied`: Define a module that is being used.
- `class`, `func`: Main definitions for declaring classes and functions.
- `var`, `put`, `ask`: Built-in functions for variable declaration, output, and input handling.
- `if`, `else`, `elif`: Control flow statements.

**Additional Enhancements:**
- Introduced a versioning system.
- Added configuration log support.

## Installation

Clone the repository:
```bash
git clone https://github.com/LegendCoder505/RAGAR-Development-Language.git
cd RAGAR-Development-Language
```

Run a RAGAR script:
```bash
python3 ragar.py script.rgr
```

## Example Code

```rgr
var x = 10
var y = 20
if x < y {
    put "X is smaller!"
} else {
    put "X is larger!"
}
```

## Contributing

RAGAR is open-source and actively developed. Contributions are welcome.

- Report bugs via GitHub Issues.
- Submit pull requests for improvements.
- Participate in discussions within the project community.

## License

RAGAR is licensed under the MIT License. You are free to use and modify the language.

Stay tuned for future updates. More features and optimizations are planned.
