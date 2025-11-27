import re


def trim_md_table(markdown: str) -> str:
    """
    Simplify Markdown by removing excessive whitespace from table cells
    and normalizing table separator rows.

    Args:
        markdown: Input Markdown string with potential excessive whitespace in tables

    Returns:
        Cleaned Markdown with normalized table formatting
    """
    lines = markdown.split("\n")
    result = []

    # Pattern to detect actual table rows (must have at least 2 pipes)
    table_row_pattern = re.compile(r"^\s*\|.*\|")
    # Pattern to detect separator cells (dashes with optional colons)
    separator_pattern = re.compile(r"^:?-+:?$")

    def normalize_separator_cell(cell: str) -> str:
        """Normalize a separator cell to minimal form (3 dashes)."""
        cell = cell.strip()
        if not separator_pattern.match(cell):
            return cell

        # Check alignment
        starts_with_colon = cell.startswith(":")
        ends_with_colon = cell.endswith(":")

        if starts_with_colon and ends_with_colon:
            return ":---:"  # Center aligned
        elif starts_with_colon:
            return ":---"  # Left aligned (explicit)
        elif ends_with_colon:
            return "---:"  # Right aligned
        else:
            return "---"  # Default (left aligned)

    for line in lines:
        # Check if this is actually a table row, not just any line with |
        if table_row_pattern.match(line) and line.count("|") >= 2:
            # Process as table row
            cells = line.split("|")
            # Strip whitespace from each cell
            cells = [cell.strip() for cell in cells]
            # Filter out empty first/last elements from leading/trailing |
            cleaned_cells = [
                cell for i, cell in enumerate(cells) if i > 0 and i < len(cells) - 1
            ]
            # Normalize separator cells
            cleaned_cells = [normalize_separator_cell(cell) for cell in cleaned_cells]
            # Reconstruct with normalized spacing
            cleaned_line = "| " + " | ".join(cleaned_cells) + " |"
            result.append(cleaned_line)
        else:
            # Not a table row, preserve as-is
            result.append(line)

    return "\n".join(result)
