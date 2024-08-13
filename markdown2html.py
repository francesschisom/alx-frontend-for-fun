#!/usr/bin/python3
"""
markdown2html.py - A script to convert Markdown files to HTML.

This script takes two command-line arguments:
1. The name of the Markdown file to be converted.
2. The name of the output HTML file.

Usage:
    python3 markdown2html.py input.md output.html
"""

import sys
import os
import markdown

def parse_custom_markdown(md_content):
    """
    Parses custom Markdown content, specifically handling ordered lists,
    unordered lists, and paragraphs.
    
    Args:
        md_content (str): The raw Markdown content as a string.
    
    Returns:
        str: The parsed HTML content as a string.
    """
    lines = md_content.splitlines()
    html_output = []
    in_list = False
    list_type = None
    paragraph_lines = []

    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line.startswith('* '):
            if paragraph_lines:
                html_output.append(f"<p>{' '.join(paragraph_lines)}</p>")
                paragraph_lines = []
            if not in_list:
                html_output.append('<ol>')
                in_list = True
                list_type = 'ordered'
            item_text = stripped_line[2:].strip()
            html_output.append(f'<li>{item_text}</li>')
        elif stripped_line.startswith('- '):
            if paragraph_lines:
                html_output.append(f"<p>{' '.join(paragraph_lines)}</p>")
                paragraph_lines = []
            if not in_list:
                html_output.append('<ul>')
                in_list = True
                list_type = 'unordered'
            item_text = stripped_line[2:].strip()
            html_output.append(f'<li>{item_text}</li>')
        elif stripped_line == "":
            if paragraph_lines:
                html_output.append(f"<p>{' '.join(paragraph_lines)}</p>")
                paragraph_lines = []
            if in_list:
                if list_type == 'ordered':
                    html_output.append('</ol>')
                elif list_type == 'unordered':
                    html_output.append('</ul>')
                in_list = False
                list_type = None
        else:
            if in_list:
                if list_type == 'ordered':
                    html_output.append('</ol>')
                elif list_type == 'unordered':
                    html_output.append('</ul>')
                in_list = False
                list_type = None
            paragraph_lines.append(stripped_line)

    # Close any open paragraphs at the end of the document
    if paragraph_lines:
        html_output.append(f"<p>{' '.join(paragraph_lines)}</p>")
    
    # Close any unclosed lists at the end of the document
    if in_list:
        if list_type == 'ordered':
            html_output.append('</ol>')
        elif list_type == 'unordered':
            html_output.append('</ul>')
    
    return "\n".join(html_output)

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes the result to the output file.

    Args:
        input_file (str): The path to the input Markdown file.
        output_file (str): The path to the output HTML file.
    """
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Custom parsing for ordered lists, unordered lists, and paragraphs
        md_content = parse_custom_markdown(md_content)

        # Convert the parsed content to HTML
        html_content = markdown.markdown(md_content)

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        print(f"Successfully converted {input_file} to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to handle command-line arguments and call the conversion function.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 markdown2html.py <input_file.md> <output_file.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)

if __name__ == "__main__":
    main()

