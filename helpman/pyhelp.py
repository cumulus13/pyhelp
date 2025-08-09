#!/usr/bin/env python3
"""
Enhanced Python Help Tool with Rich Library - Beautiful terminal output
Author: Hadi Cahyadi (cumulus13@gmail.com)
License: MIT
"""

import os
import sys
import time
import importlib
import subprocess
from pathlib import Path
from typing import Optional, List, Any, Union
import threading
import io
from contextlib import redirect_stdout
import argparse
import inspect
import re
# import shutil
from licface import CustomRichHelpFormatter
# from textwrap import wrap
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
    from rich.table import Table
    from rich.columns import Columns
    from rich.text import Text
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.align import Align
    from rich.layout import Layout
    from rich.live import Live
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich import box
    from rich.traceback import install
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback to basic console if Rich is not available
    class Console:
        def print(self, *args, **kwargs):
            print(*args)

class EnhancedPyHelp:
    """Enhanced Python Help Tool with Rich library support"""
    
    def __init__(self):
        self.version = "2.1.0"
        self.author = "Enhanced PyHelp with Rich"
        self.python_paths = []
        self.cache = {}
        
        # Initialize Rich console
        self.console = Console()
        
        # Install rich traceback handler for better error display
        if RICH_AVAILABLE:
            install()
        
        # Check if Rich is available
        if not RICH_AVAILABLE:
            self.console.print("⚠️  Rich library not found. Install with: pip install rich")
            self.console.print("Falling back to basic output...\n")
    
    def get_version(self):
        """
        Get the version.
        Version is taken from the __version__.py file if it exists.
        The content of __version__.py should be:
        version = "0.33"
        """
        try:
            version_file = Path(__file__).parent / "__version__.py"
            if version_file.is_file():
                with open(version_file, "r") as f:
                    for line in f:
                        if line.strip().startswith("version"):
                            parts = line.split("=")
                            if len(parts) == 2:
                                return parts[1].strip().strip('"').strip("'")
        except Exception as e:
            if os.getenv('TRACEBACK') and os.getenv('TRACEBACK') in ['1', 'true', 'True']:
                self.console.log(Syntax(traceback.format_exc(), 'pytb'))
            else:
                self.console.log(f"[white on red]{e}[/]")

        return self.version

    def get_width(self) -> int:
        """Get terminal width for code display"""
        try:
            columns = os.get_terminal_size()[0]
            return min(columns - 4, 120)  # Leave some margin and cap at 120
        except:
            return 100  # Default width
    
    def print_header(self) -> None:
        """Print beautiful application header using Rich"""
        if not RICH_AVAILABLE:
            print("Enhanced Python Help Tool v" + self.get_version())
            print("=" * 60)
            return
            
        # Create a beautiful header panel
        header_text = Text()
        header_text.append("🐍 Enhanced Python Help Tool ", style="bold cyan")
        header_text.append(f"v{self.version}", style="bold yellow")
        header_text.append(" 🚀", style="bold cyan")
        
        description = Text()
        description.append("Beautiful terminal help for Python modules", style="italic bright_blue")
        
        header_panel = Panel(
            Align.center(header_text + "\n" + description),
            style="bold blue",
            box=box.DOUBLE_EDGE,
            padding=(1, 2)
        )
        
        self.console.print(header_panel)
        self.console.print()
    
    def show_usage(self) -> None:
        """Show usage information with Rich formatting"""
        if not RICH_AVAILABLE:
            filename = Path(sys.argv[0]).name
            print(f"Usage: {filename} [module/module.function/module.class]")
            print(f"Example: {filename} os.path")
            return
            
        filename = Path(sys.argv[0]).name
        
        # Create usage table
        usage_table = Table(show_header=False, box=box.SIMPLE)
        usage_table.add_column("Command", style="bold green")
        usage_table.add_column("Description", style="bright_blue")
        
        usage_table.add_row(f"{filename} os.path", "Show help for os.path module")
        usage_table.add_row(f"{filename} json.loads", "Show help for json.loads function")
        usage_table.add_row(f"{filename} collections.Counter", "Show help for Counter class")
        usage_table.add_row(f"{filename} requests", "Show help for requests module")
        
        usage_panel = Panel(
            usage_table,
            title="📚 Usage Examples",
            title_align="left",
            style="bright_yellow"
        )
        
        self.console.print(usage_panel)
    
    def find_python_executables(self) -> List[str]:
        """Find all Python executables with Rich progress bar"""
        if self.python_paths:
            return self.python_paths
            
        if not RICH_AVAILABLE:
            self.console.print("Searching for Python interpreters...")
            # Basic search without progress bar
            executables = []
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            search_names = ['python', 'python3', 'python.exe', 'python3.exe']
            
            for directory in path_dirs:
                if not directory or not os.path.isdir(directory):
                    continue
                for name in search_names:
                    exe_path = os.path.join(directory, name)
                    if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
                        if exe_path not in executables:
                            executables.append(exe_path)
            
            if not executables:
                executables.append(sys.executable)
            
            self.python_paths = executables
            return executables
        
        executables = []
        search_names = ['python', 'python3', 'python.exe', 'python3.exe']
        
        # Get PATH directories
        path_dirs = [d for d in os.environ.get('PATH', '').split(os.pathsep) if d and os.path.isdir(d)]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console
        ) as progress:
            
            search_task = progress.add_task("🔍 Scanning PATH directories...", total=len(path_dirs))
            
            for directory in path_dirs:
                for name in search_names:
                    exe_path = os.path.join(directory, name)
                    if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
                        if exe_path not in executables:
                            executables.append(exe_path)
                progress.update(search_task, advance=1)
        
        # Check common locations
        common_paths = [
            '/usr/bin', '/usr/local/bin',
            'C:\\Python*', 'C:\\Program Files\\Python*',
        ]
        
        for path_pattern in common_paths:
            for path in Path().glob(path_pattern):
                if path.is_dir():
                    for name in search_names:
                        exe_path = path / name
                        if exe_path.is_file() and str(exe_path) not in executables:
                            executables.append(str(exe_path))
        
        # Use current Python if no others found
        if not executables:
            executables.append(sys.executable)
            
        self.python_paths = executables
        
        # Show results in a nice panel
        result_text = Text()
        result_text.append("✅ Found ", style="bold green")
        result_text.append(f"{len(executables)}", style="bold yellow")
        result_text.append(" Python interpreter(s)", style="bold green")
        
        self.console.print(Panel(result_text, style="green"))
        
        return executables
    
    def test_python_executable(self, python_path: str) -> tuple[bool, str]:
        """Test if Python executable is working and return version info"""
        try:
            result = subprocess.run([python_path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, version
            return False, result.stderr.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            return False, str(e)
    
    def get_working_python(self) -> Optional[str]:
        """Get the first working Python executable with Rich display"""
        executables = self.find_python_executables()
        
        if not RICH_AVAILABLE:
            for python_path in executables:
                working, version = self.test_python_executable(python_path)
                if working:
                    self.console.print(f"Using: {python_path} ({version})")
                    return python_path
            return None
        
        # Create a table to show Python interpreters
        python_table = Table(title="🐍 Available Python Interpreters", box=box.ROUNDED)
        python_table.add_column("Path", style="bright_cyan")
        python_table.add_column("Version", style="bright_green")
        python_table.add_column("Status", style="bold")
        
        working_python = None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🧪 Testing Python interpreters...", total=len(executables))
            
            for python_path in executables:
                working, version_or_error = self.test_python_executable(python_path)
                
                if working:
                    python_table.add_row(
                        python_path,
                        version_or_error,
                        "✅ Working"
                    )
                    if working_python is None:
                        working_python = python_path
                else:
                    python_table.add_row(
                        python_path,
                        version_or_error,
                        "❌ Failed"
                    )
                progress.update(task, advance=1)
        
        self.console.print(python_table)
        
        if working_python:
            selected_text = Text()
            selected_text.append("🎯 Selected: ", style="bold yellow")
            selected_text.append(working_python, style="bold cyan")
            self.console.print(Panel(selected_text, style="yellow"))
        
        return working_python
    
    def get_source(self, source: Any) -> bool:
        """Get and display source code with Rich syntax highlighting"""
        if not RICH_AVAILABLE:
            try:
                source_code = inspect.getsource(source)
                print("Source Code:")
                print("-" * 50)
                print(source_code)
                print("-" * 50)
                return True
            except Exception as e:
                print(f"Error getting source: {e}")
                return False
        
        try:
            # Get source code
            source_code = inspect.getsource(source)
            
            # Display with Rich syntax highlighting
            syntax = Syntax(
                source_code, 
                "python", 
                theme='fruity', 
                line_numbers=True, 
                tab_size=2, 
                code_width=self.get_width(), 
                word_wrap=True
            )
            
            # Create a panel for the source code
            source_panel = Panel(
                syntax,
                title=f"📄 Source Code - {getattr(source, '__name__', 'Unknown')}",
                title_align="left",
                style="bright_green",
                box=box.ROUNDED
            )
            
            self.console.print(source_panel)
            
            # Show terminal width info
            width_info = Text()
            width_info.append("📏 Terminal Width: ", style="bold")
            width_info.append(f"{self.get_width()}", style="bold yellow")
            width_info.append(" characters", style="bold")
            
            self.console.print(Panel(width_info, style="dim"))
            
            return True
            
        except Exception as e:
            if sys.version_info.major == 2:
                # Fallback for Python 2
                return self.get_source_python2(source)
            else:
                error_text = Text()
                error_text.append("❌ Error getting source: ", style="bold red")
                error_text.append(str(e), style="red")
                self.console.print(Panel(error_text, style="red"))
                return False
    
    def get_source_python2(self, source: Any) -> bool:
        """Fallback method for Python 2"""
        try:
            module_name = getattr(source, '__module__', getattr(source, '__name__', 'unknown'))
            width = self.get_width()
            
            # Try with module
            cmd = f"""python3 -c "import {module_name};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({module_name}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={width}))" """
            
            result = os.system(cmd)
            if result == 0:
                return True
            
            # Try with object name
            obj_name = getattr(source, '__name__', 'unknown')
            cmd = f"""python3 -c "import {obj_name};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({obj_name}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={width}))" """
            
            result = os.system(cmd)
            return result == 0
            
        except Exception as e:
            self.console.print(f"❌ Error in Python 2 fallback: {e}")
            return False
        """Safely import a module and return (module, error)"""
        try:
            if '.' in module_name:
                # Handle submodules
                parts = module_name.split('.')
                module = importlib.import_module(parts[0])
                obj = module
                for part in parts[1:]:
                    obj = getattr(obj, part)
                return obj, None
            else:
                module = importlib.import_module(module_name)
                return module, None
        except Exception as e:
            return None, str(e)
    
    def format_help_with_rich(self, obj: Any) -> None:
        """Format and display help output using Rich"""
        if not RICH_AVAILABLE:
            help(obj)
            return
            
        # Capture help output
        help_output = io.StringIO()
        with redirect_stdout(help_output):
            help(obj)
        
        # help_text = "\n".join(wrap(help_output.getvalue(), os.get_terminal_size()[0] - 2))
        help_text = help_output.getvalue()
        
        # Create syntax highlighted help
        help_panel = Panel(
            Syntax(help_text, "restructuredtext", theme='fruity', word_wrap = True, code_width = os.get_terminal_size()[0] - 5),
            title="📖 Help Documentation",
            title_align="left",
            style="bright_blue",
            box=box.ROUNDED,
        )
        
        self.console.print(help_panel)
    
    def show_attributes_with_rich(self, obj: Any, show_all: bool = False) -> None:
        """Show object attributes in a beautiful Rich table"""
        if not RICH_AVAILABLE:
            print("Attributes:", dir(obj))
            return
            
        attributes = dir(obj)
        public_attrs = [attr for attr in attributes if not attr.startswith('_')]
        private_attrs = [attr for attr in attributes if attr.startswith('_')]
        
        # Create attributes table
        attr_table = Table(title="🔧 Attributes & Methods", box=box.ROUNDED)
        attr_table.add_column("Name", style="bright_cyan")
        attr_table.add_column("Type", style="bright_yellow")
        attr_table.add_column("Visibility", style="bright_green")
        
        # Add public attributes
        for attr in (public_attrs if show_all else public_attrs[:20]):  # Limit to first 20 for readability
            try:
                attr_obj = getattr(obj, attr)
                attr_type = type(attr_obj).__name__
                attr_table.add_row(attr, attr_type, "Public")
            except:
                attr_table.add_row(attr, "Unknown", "Public")
        
        # Add some private attributes
        for attr in (private_attrs if show_all else private_attrs[:10]):  # Limit to first 10
            try:
                attr_obj = getattr(obj, attr)
                attr_type = type(attr_obj).__name__
                attr_table.add_row(attr, attr_type, "Private")
            except:
                attr_table.add_row(attr, "Unknown", "Private")
        
        self.console.print(attr_table)
        
        # Show summary
        summary_text = Text()
        summary_text.append(f"📊 Total: ", style="bold")
        summary_text.append(f"{len(public_attrs)}", style="bold green")
        summary_text.append(" public, ", style="bold")
        summary_text.append(f"{len(private_attrs)}", style="bold yellow")
        summary_text.append(" private attributes", style="bold")
        
        if len(public_attrs) > 20 and not show_all:
            summary_text.append(f" (showing first 20 public)", style="dim")
        # else:
        #     summary_text.append(f" (showing first {len(public_attrs)} public)", style="dim")
        if len(private_attrs) > 10 and not show_all:
            summary_text.append(f" (showing first 10 private)", style="dim")

        summary_text.append(f" use '-a' to show all", style="dim")
        # else:
        #     summary_text.append(f" (showing first {len(private_attrs)} private)", style="dim")
        
        self.console.print(Panel(summary_text, style="bright_magenta"))
    
    def import_module_safely(self, module_name: str) -> tuple[Any, Optional[str]]:
        """Safely import a module and return (module, error)"""
        try:
            if '.' in module_name:
                # Handle submodules
                parts = module_name.split('.')
                module = importlib.import_module(parts[0])
                obj = module
                for part in parts[1:]:
                    obj = getattr(obj, part)
                return obj, None
            else:
                module = importlib.import_module(module_name)
                return module, None
        except Exception as e:
            return None, str(e)

    def show_module_help(self, module_name: str, show_source: bool = False, show_all: bool = False) -> bool:
        """Show help for a specific module with Rich formatting"""
        if not RICH_AVAILABLE:
            # Fallback to basic help
            try:
                obj, error = self.import_module_safely(module_name)
                if obj:
                    if show_source:
                        self.get_source(obj)
                    else:
                        help(obj)
                        print("\nAttributes:", dir(obj))
                    return True
                else:
                    print(f"Error: {error}")
                    return False
            except Exception as e:
                print(f"Error: {e}")
                return False
        
        # Show loading spinner
        with self.console.status(f"[bold green]Loading module: {module_name}...") as status:
            obj, error = self.import_module_safely(module_name)
        
        if obj is not None:
            # Success message
            success_text = Text()
            success_text.append("✅ Module loaded successfully: ", style="bold green")
            success_text.append(module_name, style="bold cyan")
            self.console.print(Panel(success_text, style="green"))
            
            if show_source:
                # Show source code instead of help
                return self.get_source(obj)
            else:
                # Show help documentation
                self.format_help_with_rich(obj)
                
                # Show attributes
                self.show_attributes_with_rich(obj, show_all)
            
            return True
        else:
            # Show error and try subprocess method
            error_text = Text()
            error_text.append("⚠️  Direct import failed: ", style="bold yellow")
            error_text.append(error, style="red")
            self.console.print(Panel(error_text, style="yellow"))
            
            if show_source:
                self.console.print("❌ Cannot show source code for failed imports")
                return False
            else:
                self.console.print("🔄 Trying external Python interpreter...")
                return self.show_module_help_subprocess(module_name)
    
    def show_module_help_subprocess(self, module_name: str) -> bool:
        """Show help using subprocess with Rich progress"""
        python_path = self.get_working_python()
        
        if not python_path:
            if RICH_AVAILABLE:
                self.console.print(Panel("❌ No working Python interpreter found!", style="bold red"))
            else:
                self.console.print("❌ No working Python interpreter found!")
            return False
        
        # Prepare the command
        if '.' in module_name:
            parts = module_name.split('.')
            cmd = f"import {parts[0]}; help({module_name}); print('\\n' + '='*50 + '\\nATTRIBUTES:\\n' + '='*50); print(dir({module_name}))"
        else:
            builtins = ['dict', 'list', 'str', 'int', 'float', 'bool', 'tuple', 'set']
            if module_name in builtins:
                cmd = f"help({module_name}); print('\\n' + '='*50 + '\\nATTRIBUTES:\\n' + '='*50); print(dir({module_name}))"
            else:
                cmd = f"import {module_name}; help({module_name}); print('\\n' + '='*50 + '\\nATTRIBUTES:\\n' + '='*50); print(dir({module_name}))"
        
        try:
            if RICH_AVAILABLE:
                with self.console.status("[bold blue]Executing help command...") as status:
                    result = subprocess.run([python_path, '-c', cmd], 
                                          capture_output=True, text=True, timeout=30)
            else:
                self.console.print("Executing help command...")
                result = subprocess.run([python_path, '-c', cmd], 
                                      capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                if RICH_AVAILABLE:
                    # Show output in a nice panel
                    output_panel = Panel(
                        result.stdout,
                        title="📋 Help Output",
                        title_align="left",
                        style="bright_green"
                    )
                    self.console.print(output_panel)
                else:
                    self.console.print("Help Output:")
                    self.console.print(result.stdout)
                return True
            else:
                if RICH_AVAILABLE:
                    error_panel = Panel(
                        result.stderr,
                        title="❌ Error",
                        title_align="left",
                        style="bold red"
                    )
                    self.console.print(error_panel)
                else:
                    self.console.print("Error:", result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            if RICH_AVAILABLE:
                self.console.print(Panel("⏱️ Help command timed out!", style="bold red"))
            else:
                self.console.print("⏱️ Help command timed out!")
            return False
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(Panel(f"💥 Unexpected error: {str(e)}", style="bold red"))
            else:
                self.console.print(f"💥 Unexpected error: {str(e)}")
            return False
    
    def create_argument_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser"""
        parser = argparse.ArgumentParser(
            prog='pyhelp/helpman',
            description='🐍 Enhanced Python Help Tool with Rich formatting',
            formatter_class=CustomRichHelpFormatter,
            epilog="""
Examples:
  pyhelp os.path                    # Show help for os.path module
  pyhelp json.loads                 # Show help for json.loads function
  pyhelp -s requests.get            # Show source code for requests.get
  pyhelp --source collections.Counter  # Show source code for Counter class
            """
        )
        
        parser.add_argument(
            'module',
            nargs='*',
            help='Module, function, or class to get help for (e.g., os.path, json.loads)'
        )
        
        parser.add_argument(
            '-s', '--source',
            action='store_true',
            help='Show source code instead of help documentation'
        )

        parser.add_argument(
            '-a', '--show-all',
            action='store_true',
            help='Show all the attributes'
        )

        parser.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='Interactive mode'
        )
        
        parser.add_argument(
            '-v', '--version',
            action='version',
            version=f'pyhelp v{self.get_version()}'
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> None:
        """Main application entry point with argparse"""
        parser = self.create_argument_parser()
        
        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)
        # Parse arguments
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit:
            return
        
        self.print_header()
        module_name = " ".join(parsed_args.module)

        if "c " in module_name.lower().strip() or " c" in module_name.lower().strip():
            module_name = list(filter(None, list(filter(lambda k: k.strip() != 'c', re.split(" c|c | C|C ", module_name, re.I)))))
            module_name = module_name[0] if module_name else None
            os.system('cls') if 'win' in sys.platform.lower() else os.system('clear')

        while 1:
            show_source = parsed_args.source
            # Show module info
            if RICH_AVAILABLE:
                action = "source code" if show_source else "help"
                module_info = Text()
                module_info.append("🎯 Target: ", style="bold")
                module_info.append(module_name, style="bold cyan")
                module_info.append(f" ({action})", style="bold yellow")
                self.console.print(Panel(module_info, style="blue"))
            else:
                action = "source code" if show_source else "help"
                self.console.print(f"🎯 Target: {module_name} ({action})")
            
            start_time = time.time()
            success = self.show_module_help(module_name, show_source, parsed_args.show_all)
            end_time = time.time()
            
            # Show completion status
            if RICH_AVAILABLE:
                if success:
                    completion_text = Text()
                    completion_text.append("🎉 Operation completed in ", style="bold green")
                    completion_text.append(f"{end_time - start_time:.2f}s", style="bold yellow")
                    self.console.print(Panel(completion_text, style="green"))
                else:
                    failure_text = Text()
                    failure_text.append("❌ Failed to complete operation", style="bold red")
                    failure_text.append("\n💡 Please check the module name and try again", style="yellow")
                    self.console.print(Panel(failure_text, style="red"))
            else:
                if success:
                    self.console.print(f"🎉 Operation completed in {end_time - start_time:.2f}s")
                else:
                    self.console.print("❌ Failed to complete operation")

            if parsed_args.interactive:
                self.console.print("[bold #00FFFF]q/quit/x/exit = exit/quit[/]") if RICH_AVAILABLE else print("q/quit/x/exit = exit/quit")
                
                q = input(": ")
                if q:
                    if q.lower().strip() in ['exit', 'quit', 'x', 'q']:
                        sys.exit(0)
                    elif "c " in q.lower().strip() or " c" in q.lower().strip():
                        q = list(filter(None, list(filter(lambda k: k.strip() != 'c', re.split(" c|c | C|C ", q, re.I)))))
                        q = q[0] if q else None
                        os.system('cls') if 'win' in sys.platform.lower() else os.system('clear')
                if q:
                    module_name = q
            else:
                break

def main():
    """Main function with Rich error handling"""
    try:
        app = EnhancedPyHelp()
        app.run()
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console = Console()
            console.print(Panel("⚠️ Operation cancelled by user", style="bold yellow"))
        else:
            print("⚠️ Operation cancelled by user")
    except Exception as e:
        if RICH_AVAILABLE:
            console = Console()
            console.print(Panel(f"💥 Unexpected error: {str(e)}", style="bold red"))
        else:
            print(f"💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()