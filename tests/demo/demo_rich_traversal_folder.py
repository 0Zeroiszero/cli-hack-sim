from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

tree_text = """ROOT
├── SYSTEM
│   ├── CONFIG
│   └── SECURITY
└── DATABASE
    └── LOGS"""

table = Table(
    show_header=True,
    header_style="bold cyan",
    border_style="white",
    box=box.SIMPLE,
    expand=True,
)

table.add_column("Traversal Lainnya", style="bold green", no_wrap=True)
table.add_column("Hasil", style="white")

table.add_row("Inorder", "CONFIG → SYSTEM → SECURITY → ROOT → LOGS → DATABASE")

table.add_row("Postorder", "CONFIG → SECURITY → SYSTEM → LOGS → DATABASE → ROOT")

if __name__ == "__main__":
    console.print(Panel(tree_text, title="Preorder Tree", border_style="green"))
    console.print(table)
