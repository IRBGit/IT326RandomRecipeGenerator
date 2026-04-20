from json2pdf_converter import generate
import json2pdf_converter
import json
import os
from pathlib import Path
import shutil

project_root = Path(__file__).resolve().parent.parent


def search_recipe(recipe_name: str) -> dict | None:
    """Search for a recipe across all JSON recipe files.
    
    Args:
        recipe_name: The name of the recipe to search for (case-insensitive)
    
    Returns:
        A dict containing the recipe if found, None otherwise
    """
    recipes_dir = project_root / 'JSON_Recipes'
    recipe_name_lower = recipe_name.lower()
    
    # Iterate through all JSON files in the recipes directory
    for json_file in recipes_dir.glob('*_recipes.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('meals'):
                    for meal in data['meals']:
                        if meal.get('strMeal', '').lower() == recipe_name_lower:
                            return meal
        except (json.JSONDecodeError, FileNotFoundError):
            continue
    
    return None


def ensure_wkhtmltopdf_available() -> None:
    package_dir = Path(json2pdf_converter.__file__).resolve().parent
    expected_bin_dir = package_dir / 'wkhtmltopdf' / 'bin'
    executable_name = 'wkhtmltopdf.exe' if os.name == 'nt' else 'wkhtmltopdf'
    image_executable_name = 'wkhtmltoimage.exe' if os.name == 'nt' else 'wkhtmltoimage'
    expected_exe = expected_bin_dir / executable_name

    if expected_exe.exists():
        return

    installed_exe_path = (
        os.environ.get('WKHTMLTOPDF_BIN')
        or os.environ.get('WKHTMLTOPDF_PATH')
        or shutil.which(executable_name)
        or shutil.which('wkhtmltopdf')
    )
    if not installed_exe_path:
        raise FileNotFoundError(
            f'{executable_name} is not installed or not available on PATH. '
            'Install wkhtmltopdf, or set WKHTMLTOPDF_BIN/WKHTMLTOPDF_PATH, and rerun exporter.'
        )

    installed_bin_dir = Path(installed_exe_path).resolve().parent

    expected_bin_dir.mkdir(parents=True, exist_ok=True)
    binary_names = [executable_name, image_executable_name]
    if os.name == 'nt':
        binary_names.append('wkhtmltox.dll')

    for binary_name in binary_names:
        src = installed_bin_dir / binary_name
        if src.exists():
            shutil.copy2(src, expected_bin_dir / binary_name)


ensure_wkhtmltopdf_available()

# Get recipe name from user
recipe_name = input("Enter the recipe name you want to export to PDF: ").strip()

if not recipe_name:
    print("Error: Recipe name cannot be empty.")
    exit(1)

# Search for the recipe
recipe = search_recipe(recipe_name)

if recipe is None:
    print(f"Error: Recipe '{recipe_name}' not found in the database.")
    exit(1)

print(f"Found recipe: {recipe.get('strMeal', 'Unknown')}")

# Create a data structure with just this recipe
data = {"meals": [recipe]}

options = {
    'encoding': 'UTF-8',
    'margin-top': '0px',
    'margin-right': '30px',
    'margin-bottom': '30px',
    'margin-left': '30px',
    'footer-right': "Page [page] of [topage]",
    'footer-font-size': "9",
    'orientation': 'Portrait',
    'page-size': 'A4',
}

data_variables = {
    "data": data
}
template_directory = project_root / 'exportFiles'
template_name = "recipeExportTemplate.html"

# Create a safe filename from the recipe name
safe_recipe_name = "".join(c for c in recipe.get('strMeal', 'recipe') if c.isalnum() or c in (' ', '_', '-')).rstrip()

# Directories for output (library expects directories, not full paths)
output_dir = str(project_root / 'exportFiles')

print(f"Generating PDF: {safe_recipe_name}.pdf")

# Note: json_file_path is passed to generate() but we're using data_variables instead
dummy_json_path = project_root / 'JSON_Recipes' / 'a_recipes.json'

generate(
    json_file_path=str(dummy_json_path),
    template_directory_path=str(template_directory),
    output_html_path=output_dir,
    output_pdf_path=output_dir,
    options=options,
    template_name=template_name,
    data_variables=data_variables,
    custom_filter_functions=[]
)

# Rename the generated files to use the recipe name
# HTML file is created in the root output directory, move it to html/
output_html_file = Path(output_dir) / 'output.html'
html_dir = Path(output_dir) / 'html'
html_dir.mkdir(exist_ok=True)
final_html_file = html_dir / f'{safe_recipe_name}.html'

# PDF file is created in the pdf subdirectory
output_pdf_file = Path(output_dir) / 'pdf' / 'merged_output.pdf'
pdf_dir = Path(output_dir) / 'pdf'
pdf_dir.mkdir(exist_ok=True)
final_pdf_file = pdf_dir / f'{safe_recipe_name}.pdf'

# Move HTML file
if output_html_file.exists():
    if final_html_file.exists():
        final_html_file.unlink()
    output_html_file.replace(final_html_file)
    print(f"HTML created: {final_html_file}")
else:
    print(f"Warning: HTML file not found at {output_html_file}")

# Move PDF file
if output_pdf_file.exists():
    if final_pdf_file.exists():
        final_pdf_file.unlink()
    output_pdf_file.replace(final_pdf_file)
    print(f"PDF created: {final_pdf_file}")
else:
    print(f"Warning: PDF file not found at {output_pdf_file}")

print(f"\nPDF successfully created at: {final_pdf_file}")