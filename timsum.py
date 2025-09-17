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
import os
import configparser

CONFIG_PATH = os.path.expanduser("~/.config/timsum/timsum.conf")
THEMES_DIR = os.path.expanduser("~/.config/timsum/themes")


def load_config():
    """Load timsum.conf file (INI format)."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    return config


def load_theme(theme_name):
    """Load theme either from built-ins or JSON file."""
    # Check built-in
    if theme_name in CATPPUCCIN:
        return CATPPUCCIN[theme_name]

    # Check custom theme JSON
    theme_file = os.path.join(THEMES_DIR, f"{theme_name}.json")
    if os.path.exists(theme_file):
        try:
            with open(theme_file, "r") as f:
                theme_data = json.load(f)
                # Validate that the theme has required keys
                required_keys = ["base", "text", "accent", "highlight"]
                if all(key in theme_data for key in required_keys):
                    return theme_data
                else:
                    missing_keys = [
                        key for key in required_keys if key not in theme_data
                    ]
                    raise ValueError(
                        f"Theme '{theme_name}' is missing required keys: {missing_keys}"
                    )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in theme file '{theme_file}': {e}")

    raise ValueError(f"Theme '{theme_name}' not found in built-ins or {THEMES_DIR}")


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


def assign_tag_colors(tags, theme):
    """Assign consistent colors to tags using hashing for deterministic color assignment."""
    color_map = {}

    # Use a combination of theme colors and TAG_COLORS for variety
    available_colors = TAG_COLORS + [theme["accent"], theme["highlight"], theme["text"]]

    for tag in tags + ["(UNTAGGED)"]:
        norm = normalize_tag(tag)
        # Use hash for consistent color assignment
        h = int(hashlib.sha256(norm.encode()).hexdigest(), 16)
        color_map[norm] = available_colors[h % len(available_colors)]

    return color_map


from datetime import datetime, timezone


def parse_intervals(data):
    """Convert timewarrior intervals into per-day totals and per-tag totals."""
    per_day = defaultdict(lambda: {"hours": 0.0, "tags": defaultdict(float)})
    tag_totals = defaultdict(float)

    for entry in data:
        start = datetime.fromisoformat(entry["start"])
        if "end" in entry:
            end = datetime.fromisoformat(entry["end"])
        else:
            # match tz awareness with `start`
            if start.tzinfo is not None:
                end = datetime.now(start.tzinfo)
            else:
                end = datetime.now()

        duration = (end - start).total_seconds() / 3600
        day_key = start.date().isoformat()

        per_day[day_key]["hours"] += duration
        tags = entry.get("tags", ["(untagged)"])
        for tag in tags:
            tag = normalize_tag(tag)
            per_day[day_key]["tags"][tag] += duration
            tag_totals[tag] += duration

    return dict(sorted(per_day.items())), dict(sorted(tag_totals.items()))


def print_daily_table(per_day, theme, tag_colors, console):
    table = Table(show_header=True, header_style="bold " + theme["accent"])
    table.add_column("Date", style=theme["text"])
    table.add_column("Total Hours", style=theme["text"], justify="right")
    table.add_column("Tags", style=theme["text"])

    for day, data in per_day.items():
        tag_texts = []
        for tag, hours in data["tags"].items():
            # Use pre-computed tag colors
            color = tag_colors.get(normalize_tag(tag), theme["text"])
            tag_texts.append(f"[{color}]{tag} {hours:.1f}h[/{color}]")
        table.add_row(
            f"[{theme['text']}]{day}[/{theme['text']}]",
            f"[{theme['accent']}]{data['hours']:.1f}[/{theme['accent']}]",
            " ".join(tag_texts),
        )

    console.print(table)


def print_tag_totals(tag_totals, theme, tag_colors, console):
    table = Table(show_header=True, header_style="bold " + theme["accent"])
    table.add_column("Tag", style=theme["text"])
    table.add_column("Total Hours", style=theme["text"], justify="right")

    for tag, hours in tag_totals.items():
        # Use pre-computed tag colors
        color = tag_colors.get(normalize_tag(tag), theme["text"])
        table.add_row(
            f"[{color}]{tag}[/{color}]",
            f"[{theme['accent']}]{hours:.1f}[/{theme['accent']}]",
        )

    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Beautiful Timewarrior Summary with Colored Tags"
    )
    parser.add_argument(
        "--theme",
        help="Choose theme (built-in: mocha, macchiato, frappe, latte OR custom from ~/.config/timsum/themes/)",
    )
    parser.add_argument(
        "--range",
        help="Timewarrior range (e.g. :day, :week, :month, YYYY-MM-DD - YYYY-MM-DD)",
    )
    args = parser.parse_args()

    # Load config
    config = load_config()

    # Pick theme: CLI > config > default
    theme_name = args.theme or config.get("timsum", "theme", fallback="mocha")
    theme = load_theme(theme_name)

    # Pick range: CLI > config > default
    range_spec = args.range or config.get("timsum", "range", fallback=":week")

    console = Console()

    # Collect data
    data = get_timew_data(range_spec)
    tags = get_tags()
    tag_colors = assign_tag_colors(tags, theme)  # Fixed: added theme parameter

    per_day, tag_totals = parse_intervals(data)

    # Print outputs
    print_daily_table(per_day, theme, tag_colors, console)
    print_tag_totals(tag_totals, theme, tag_colors, console)
