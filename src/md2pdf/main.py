import typer
import subprocess
from pathlib import Path
import importlib.resources as pkg_resources
from weasyprint import HTML, CSS
import md2pdf

app = typer.Typer()


def get_resource_path(filename: str) -> Path:
    with pkg_resources.path(md2pdf, filename) as p:
        return p


def convertToHTML(
    input_file: Path, temp_html_path: Path, template_path: Path, lua_filter_path: Path
):
    subprocess.run(
        [
            "pandoc",
            str(input_file),
            "-M",
            "theme=github-markdown-dark",  # theme metadata does nothing for now. should just default to github-markdown-dark
            "-o",
            str(temp_html_path),
            "--template",
            str(template_path),
            "--lua-filter",
            str(lua_filter_path),
        ],
        check=True,
    )


def convertHTMLtoPDF(tempFile: Path, cssFile: Path, output_filename: Path):
    HTML(filename=tempFile).write_pdf(
        filename=output_filename, stylesheets=[CSS(filename=cssFile)]
    )


@app.command()
def main(filename: Path):
    template_path = get_resource_path("template.html")
    lua_filter_path = get_resource_path("lua/callouts-filter.lua")
    temp_html_path = get_resource_path("temp.html")
    css_path = get_resource_path("github-markdown-dark.css")
    output_filename = filename.with_suffix(".pdf")

    # TODO: Implement error handling for user input
    print("⏳ Converting To HTML")
    convertToHTML(filename, temp_html_path, template_path, lua_filter_path)
    print("HTML Conversion Success ✅")

    print("⏳ Converting To PDF")
    convertHTMLtoPDF(temp_html_path, css_path, output_filename)
    print(f"PDF Conversion Success ✅. File is available at {str(output_filename)}")


if __name__ == "__main__":
    typer.run(main)
