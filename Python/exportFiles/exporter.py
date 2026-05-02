import json
import os
from pathlib import Path
import shutil
import importlib
import sys
import tempfile

from sqlalchemy.exc import OperationalError

python_root = Path(__file__).resolve().parent.parent

if str(python_root) not in sys.path:
    sys.path.insert(0, str(python_root))

json2pdf_converter = importlib.import_module('json2pdf_converter')
generate = json2pdf_converter.generate
UnitOfWork = importlib.import_module('db.unit_of_work').UnitOfWork


def _recipe_to_meal_dict(recipe) -> dict:
    meal = {
        'idMeal': str(recipe.id) if recipe.id is not None else '',
        'strMeal': recipe.name,
        'strCategory': recipe.category or '',
        'strArea': '',
        'strInstructions': '\n'.join(recipe.instructions or []),
        'strMealThumb': '',
        'strTags': ','.join(recipe.tags or []),
        'strSource': '',
        'strYoutube': recipe.video or '',
        'dateModified': recipe.published_time.strftime('%Y-%m-%d %H:%M:%S') if recipe.published_time else '',
    }

    for index in range(1, 21):
        meal[f'strIngredient{index}'] = ''
        meal[f'strMeasure{index}'] = ''

    for index, recipe_ingredient in enumerate(recipe._ingredients.values(), start=1):
        if index > 20:
            break

        meal[f'strIngredient{index}'] = recipe_ingredient.ingredient.name

        measure_parts = []
        if recipe_ingredient.quantity is not None:
            measure_parts.append(str(recipe_ingredient.quantity))
        if recipe_ingredient.unit:
            measure_parts.append(recipe_ingredient.unit)

        meal[f'strMeasure{index}'] = ' '.join(measure_parts)

    return meal


def search_recipe(recipe_name: str) -> dict | None:
    """Search for a recipe in Oracle and return a MealDB-shaped dict."""
    recipe_name = recipe_name.strip()
    if not recipe_name:
        return None

    recipe_name_lower = recipe_name.lower()

    try:
        with UnitOfWork() as uow:
            for recipe in uow.recipes.search_by_name(recipe_name):
                if recipe.name.lower() == recipe_name_lower:
                    return _recipe_to_meal_dict(recipe)
    except OperationalError as exc:
        raise RuntimeError(
            "Unable to reach the Oracle database. Make sure you are on the ISU VPN, "
            "DB_PW is set, and the database is reachable, then rerun the exporter."
        ) from exc

    return None


def ensure_wkhtmltopdf_available() -> None:
    package_dir = Path(json2pdf_converter.__file__).resolve().parent
    expected_bin_dir = package_dir / 'wkhtmltopdf' / 'bin'
    executable_name = 'wkhtmltopdf.exe' if os.name == 'nt' else 'wkhtmltopdf'
    image_executable_name = 'wkhtmltoimage.exe' if os.name == 'nt' else 'wkhtmltoimage'
    expected_exe = expected_bin_dir / executable_name

    if expected_exe.exists():
        return

    common_windows_paths = [
        Path(r'C:\Program Files\wkhtmltopdf\bin') / executable_name,
        Path(r'C:\Program Files (x86)\wkhtmltopdf\bin') / executable_name,
    ]

    installed_exe_path = (
        os.environ.get('WKHTMLTOPDF_BIN')
        or os.environ.get('WKHTMLTOPDF_PATH')
        or shutil.which(executable_name)
        or shutil.which('wkhtmltopdf')
        or next((str(path) for path in common_windows_paths if path.exists()), None)
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

def export_recipe(recipe_name: str) -> tuple[Path, Path]:
    ensure_wkhtmltopdf_available()

    recipe_name = recipe_name.strip()
    if not recipe_name:
        raise ValueError("Recipe name cannot be empty.")

    try:
        recipe = search_recipe(recipe_name)
    except RuntimeError:
        raise

    if recipe is None:
        raise LookupError(f"Recipe '{recipe_name}' not found in the database.")

    print(f"Found recipe: {recipe.get('strMeal', 'Unknown')}")

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
    template_directory = python_root / 'exportFiles'
    template_name = "recipeExportTemplate.html"

    safe_recipe_name = "".join(c for c in recipe.get('strMeal', 'recipe') if c.isalnum() or c in (' ', '_', '-')).rstrip()
    output_dir = str(python_root / 'exportFiles')

    print(f"Generating PDF: {safe_recipe_name}.pdf")

    temp_json_path = None

    try:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json', encoding='utf-8') as temp_file:
            json.dump(data, temp_file, ensure_ascii=False, indent=2)
            temp_json_path = Path(temp_file.name)

        generate(
            json_file_path=str(temp_json_path),
            template_directory_path=str(template_directory),
            output_html_path=output_dir,
            output_pdf_path=output_dir,
            options=options,
            template_name=template_name,
            data_variables=data_variables,
            custom_filter_functions=[]
        )
    finally:
        if temp_json_path and temp_json_path.exists():
            temp_json_path.unlink()

    output_html_file = Path(output_dir) / 'output.html'
    html_dir = Path(output_dir) / 'html'
    html_dir.mkdir(exist_ok=True)
    final_html_file = html_dir / f'{safe_recipe_name}.html'

    output_pdf_file = Path(output_dir) / 'pdf' / 'merged_output.pdf'
    pdf_dir = Path(output_dir) / 'pdf'
    pdf_dir.mkdir(exist_ok=True)
    final_pdf_file = pdf_dir / f'{safe_recipe_name}.pdf'

    if output_html_file.exists():
        if final_html_file.exists():
            final_html_file.unlink()
        output_html_file.replace(final_html_file)
        print(f"HTML created: {final_html_file}")
    else:
        print(f"Warning: HTML file not found at {output_html_file}")

    if output_pdf_file.exists():
        if final_pdf_file.exists():
            final_pdf_file.unlink()
        output_pdf_file.replace(final_pdf_file)
        print(f"PDF created: {final_pdf_file}")
    else:
        print(f"Warning: PDF file not found at {output_pdf_file}")

    print(f"\nPDF successfully created at: {final_pdf_file}")
    return final_html_file, final_pdf_file


def main() -> None:
    recipe_name = input("Enter the recipe name you want to export to PDF: ").strip()

    try:
        export_recipe(recipe_name)
    except (ValueError, LookupError, RuntimeError, FileNotFoundError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()