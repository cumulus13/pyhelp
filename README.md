# 🚀 pyhelp (Helpman)

Enhanced Python Help Tool with Rich Library - Beautiful terminal output


`pyhelp` or `helpman` is a Python command-line tool that lets you quickly view the documentation (docstring) of Python functions, classes, or objects directly from your terminal. It helps you inspect documentation without opening source files or browsing online docs.

[![Example Usage](https://github.com/cumulus13/pyhelp/raw/refs/heads/master/helpman_example_usage.gif)](https://github.com/cumulus13/pyhelp/raw/refs/heads/master/helpman_example_usage.gif)

## ✨ Features

- Displays docstrings for Python functions, classes, and objects.
- Supports searching in standard Python modules and installed third-party packages.
- Provides clean, readable output right in the terminal.

## 📦 Installation

```bash
   git clone https://github.com/cumulus13/pyhelp.git
   cd pyhelp
   pip install .

   # or

   pip install helpman
```
---

## Usage

After installation, use `pyhelp` in your terminal with the following syntax:

```bash
pyhelp <object_name>
```

Replace `<object_name>` with the name of the Python function, class, or object you want to view the documentation for.


```bash
Usage: pyhelp/helpman [-h] [-s] [-a] [-i] [-v] [module ...]

🐍 Enhanced Python Help Tool with Rich formatting

Positional Arguments:
  module             Module, function, or class to get help for (e.g., os.path, json.loads)

Options:
  -h, --help         show this help message and exit
  -s, --source       Show source code instead of help documentation
  -a, --show-all     Show all the attributes
  -i, --interactive  Interactive mode
  -v, --version      show program's version number and exit

Examples:

  pyhelp os.path                    # Show help for os.path module
  pyhelp json.loads                 # Show help for json.loads function
  pyhelp -s requests.get            # Show source code for requests.get
  pyhelp --source collections.Counter  # Show source code for Counter class

```

You can clear the terminal while inputting a query by prefixing or suffixing with "c", e.g. "c query" or "query c".

### Examples

- View docstring for the `print` function:

  ```bash
  pyhelp print
  ```

- View docstring for the `list` class:

  ```bash
  pyhelp list
  ```

- View docstring for `numpy.array` function (if `numpy` is installed):

  ```bash
  pyhelp numpy.array
  ```

If the requested object is not found directly, `pyhelp` will attempt to locate it in standard Python modules and installed third-party packages.

## Contribution

Contributions to improve `pyhelp` are welcome! Please fork the repository, create a new branch (`git checkout -b new-feature`), make your changes, and submit a pull request. Make sure to add tests and update documentation as needed.

## License

`pyhelp` is licensed under the [MIT License](LICENSE).

---

If you have any questions or need help, feel free to open an issue on the [GitHub repository](https://github.com/cumulus13/pyhelp/issues).


## author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)

[medium.com](https://www.medium.com/@cumulus13)