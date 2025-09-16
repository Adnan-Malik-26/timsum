#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime
from collections import defaultdict
import argparse
import hashlib
from rich.console import Console
from rich.table import Table
from rich.style import Style

# Catppuccin palettes (for table styling)
CATPPUCCIN = {
    "mocha": {
        "base": "#1e1e2e",
        "text": "#cdd6f4",
        "accent": "#89b4fa",
        "highlight": "#f38ba8",
    },
    "macchiato": {
        "base": "#24273a",
        "text": "#cad3f5",
        "accent": "#8aadf4",
        "highlight": "#ed8796",
    },
    "frappe": {
        "base": "#303446",
        "text": "#c6d0f5",
        "accent": "#8caaee",
        "highlight": "#e78284",
    },
    "latte": {
        "base": "#eff1f5",
        "text": "#4c4f69",
        "accent": "#1e66f5",
        "highlight": "#d20f39",
    },
}

# Pool of tag colors (cycled if more tags exist)
TAG_COLORS = [
    "#f38ba8",
    "#a6e3a1",
    "#fab387",
    "#89b4fa",
    "#f9e2af",
    "#cba6f7",
    "#94e2d5",
    "#eba0ac",
    "#74c7ec",
    "#f5c2e7",
]


def normalize_tag(tag: str) -> str:
    """Normalize tags for consistent lookup."""
    if tag.lower() == "(untagged)" or tag.strip() == "":
        return "(UNTAGGED)"
    return tag.upper()


def get_timew_data(range_spec=":week"):
    """Run `timew export` and return parsed JSON."""
    result = subprocess.run(
        ["timew", "export", range_spec], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def get_tags():
    """Run `timew tags` and return a list of normalized tag names."""
    result = subprocess.run(
        ["timew", "tags"], capture_output=True, text=True, check=True
    )
    lines = result.stdout.strip().splitlines()[1:]  # skip header row
    tags = []
    for line in lines:
        if line.strip():
            # Extract tag name before the count (separated by multiple spaces)
            # Split on multiple spaces and take everything before the last part (which is the count)
            parts = line.split()
            if len(parts) >= 2:
                # Join all parts except the last one (count)
                tag = " ".join(parts[:-1])
            else:
                tag = parts[0] if parts else ""
            tags.append(normalize_tag(tag))
    return tags


def assign_tag_colors(tags):
    """Assign a persistent unique color to each tag using hashing."""
    color_map = {}
    for tag in tags + ["(UNTAGGED)"]:
        norm = normalize_tag(tag)
        h = int(hashlib.sha256(norm.encode()).hexdigest(), 16)
        color_map[norm] = TAG_COLORS[h % len(TAG_COLORS)]
    return color_map


def parse_intervals(data):
    """Convert timewarrior intervals into per-day totals and per-tag totals."""
    per_day = defaultdict(lambda: {"hours": 0.0, "tags": defaultdict(float)})
    tag_totals = defaultdict(float)

    for entry in data:
        start = datetime.fromisoformat(entry["start"])
        end = datetime.fromisoformat(entry.get("end", datetime.now().isoformat()))
        duration = (end - start).total_seconds() / 3600
        day_key = start.date().isoformat()

        per_day[day_key]["hours"] += duration
        tags = entry.get("tags", ["(untagged)"])
        for tag in tags:
            tag = normalize_tag(tag)
            per_day[day_key]["tags"][tag] += duration
            tag_totals[tag] += duration

    return dict(sorted(per_day.items())), dict(sorted(tag_totals.items()))


def print_daily_table(per_day, theme_name, tag_colors, console):
    theme = CATPPUCCIN[theme_name]

    table = Table(
        title="⏳ Daily Time Summary with Colored Tags",
        title_style=Style(color=theme["highlight"], bold=True),
        header_style=Style(color=theme["accent"], bold=True),
        border_style=theme["accent"],
    )

    table.add_column("📅 Date", justify="center", style=theme["text"])
    table.add_column("⌛ Hours", justify="center", style=theme["text"])
    table.add_column("🏷️ Tags (hours)", justify="left", style=theme["text"])

    total_hours = 0
    for day, info in per_day.items():
        tag_entries = []
        for tag, hours in info["tags"].items():
            color = tag_colors.get(tag, theme["text"])
            tag_entries.append(f"[{color}]{tag}[/{color}] [{hours:.2f}h]")
        tags_str = ", ".join(tag_entries)

        table.add_row(day, f"{info['hours']:.2f}", tags_str)
        total_hours += info["hours"]

    console.print(table)
    console.print(
        f"[bold {theme['highlight']}]✨ Total: {total_hours:.2f} h ✨[/bold {theme['highlight']}]"
    )


def print_tag_totals(tag_totals, theme_name, tag_colors, console):
    theme = CATPPUCCIN[theme_name]

    total_hours = sum(tag_totals.values())

    table = Table(
        title="🏷️ Total Hours by Tag",
        title_style=Style(color=theme["highlight"], bold=True),
        header_style=Style(color=theme["accent"], bold=True),
        border_style=theme["accent"],
    )

    table.add_column("Tag", justify="center", style=theme["text"])
    table.add_column("Hours", justify="center", style=theme["text"])
    table.add_column("% of Total", justify="center", style=theme["text"])

    for tag, hours in sorted(tag_totals.items(), key=lambda x: x[1], reverse=True):
        if hours <= 0.0:  # hide empty tags
            continue
        color = tag_colors.get(tag, theme["text"])
        percent = (hours / total_hours * 100) if total_hours > 0 else 0
        table.add_row(f"[{color}]{tag}[/{color}]", f"{hours:.2f}", f"{percent:.1f}%")

    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Beautiful Timewarrior Summary with Colored Tags"
    )
    parser.add_argument(
        "--theme",
        choices=CATPPUCCIN.keys(),
        default="mocha",
        help="Choose Catppuccin theme (mocha, macchiato, frappe, latte)",
    )
    parser.add_argument(
        "--range",
        default=":week",
        help="Timewarrior range (default: :week, e.g. :day, :month, YYYY-MM-DD - YYYY-MM-DD)",
    )
    args = parser.parse_args()

    console = Console()

    # Collect data
    data = get_timew_data(args.range)
    tags = get_tags()
    tag_colors = assign_tag_colors(tags)

    per_day, tag_totals = parse_intervals(data)

    # Print outputs
    print_daily_table(per_day, args.theme, tag_colors, console)
    print_tag_totals(tag_totals, args.theme, tag_colors, console)
