from rich.console import Console
from rich.prompt import Prompt
from rich.rule import Rule
from rich.text import Text
from rich.status import Status
from rich.table import Table
from rich.panel import Panel

from supportos.orchestrator import run_supportos

console = Console()

current_spinner = None


def banner():
    console.clear()

    console.print(
        Text(
            "SupportOS v1.0",
            style="bold white"
        )
    )

    console.print(
        "[grey58]Google ADK[/] • "
        "[grey58]Gemini[/] • "
        "[grey58]Qdrant[/] • "
        "[grey58]Context7[/] • "
        "[grey58]Lyzr[/]"
    )

    console.print(Rule(style="grey35"))


def handle_event(event):

    global current_spinner

    stage = event["stage"]
    status = event["status"]

    # ---------------- SEARCH ---------------- #

    if stage == "search":

        if status == "start":

            current_spinner = console.status(
                "[cyan]Searching vector memory...",
                spinner="dots"
            )
            current_spinner.start()

        else:

            if current_spinner:
                current_spinner.stop()

            console.print(
                f"[cyan]SEARCH[/]  Retrieved "
                f"{event['chunks']} chunks "
                f"({event['elapsed']:.2f}s)"
            )

            for src in event["sources"]:
                console.print(
                    f"         {src}",
                    style="grey62"
                )

    # ---------------- REASON ---------------- #

    elif stage == "reason":

        if status == "start":

            current_spinner = console.status(
                "[magenta]Generating grounded response...",
                spinner="dots"
            )
            current_spinner.start()

        else:

            if current_spinner:
                current_spinner.stop()

            console.print(
                f"[magenta]REASON[/]  "
                f"Completed ({event['elapsed']:.2f}s)"
            )

    # ---------------- VERIFY ---------------- #

    elif stage == "verify":

        if status == "start":

            current_spinner = console.status(
                "[green]Running verification...",
                spinner="dots"
            )
            current_spinner.start()

        else:

            if current_spinner:
                current_spinner.stop()

            console.print(
                f"[green]VERIFY[/]  "
                f"Grounded={event['grounded']} | "
                f"Risk={event['risk']} | "
                f"Action={event['action']} "
                f"({event['elapsed']:.2f}s)"
            )

            if event["escalate"]:

                console.print()

                console.print(
                    f"[bold red]ESCALATION[/] : {event['reason']}"
                )


banner()

while True:

    query = Prompt.ask(
        "\n[bold cyan]supportos[/]"
    )

    if query.lower() in ["exit", "quit"]:

        break

    console.print()

    result = run_supportos(
        query,
        callback=handle_event
    )

    console.print(Rule(style="grey35"))

    console.print(
        Panel(
            result["answer"],
            title="Answer",
            border_style="cyan",
            expand=False
        )
    )

    verification = result["verification"]

    table = Table(show_header=False)

    table.add_row(
        "Grounded",
        "YES" if verification["grounded"] else "NO"
    )

    table.add_row(
        "Risk",
        verification["risk"]
    )

    table.add_row(
        "Action",
        verification["action"]
    )

    console.print(table)

    if verification["escalate"]:

        console.print()

        console.print(
            "[bold red]Human escalation required.[/]"
        )

        console.print(
            verification["reason"]
        )

    console.print()

    console.print("[bold]Sources[/]")

    for src in result["sources"]:
        console.print(f"• {src}")

    console.print(Rule(style="grey35"))