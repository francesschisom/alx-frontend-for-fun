#!/usr/bin/python3
"""
A script that converts Markdown to HTML.
"""

import sys
import os
import re

def parse_custom_markdown(md_content):
    """
    Parses custom Markdown content, specifically handling unordered lists.

    Args:
        md_content (str): The raw Markdown content as a string.

    Returns:
        str: The parsed HTML content as a string.
    """
    lines = md_content.splitlines()
    html_output = []
    in_list = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith('- '):
            # Start of a list item
            if not in_list:
                html_output.append('<ul>')
                in_list = True
            item_text = stripped_line[2:].strip()
            html_output.append(f'<li>{item_text}</li>')
        else:
            # End of a list
            if in_list:
                html_output.append('</ul>')
                in_list = False
            html_output.append(line)

    # Close any unclosed list at the end of the document
    if in_list:
        html_output.append('</ul>')

    return "\n".join(html_output)

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    # Check that the Markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the Markdown file and convert it to HTML
    with open(input_file, encoding="utf-8") as f:
        html_lines = []
        for line in f:
            # Check for Markdown headings
            match = re.match(r"^(#+) (.*)$", line)
            if match:
                heading_level = len(match.group(1))
                heading_text = match.group(2)
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            else:
                html_lines.append(line.rstrip())

    # Write the HTML output to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

if __name__ == "__main__":
    # Check that the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    # Get the input and output file names from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Convert the Markdown file to HTML and write the output to a file
    convert_markdown_to_html(input_file, output_file)

    # Exit with a successful status code
    sys.exit(0)
