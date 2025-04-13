import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def extract_openapi_doc(openapi_path):
    with open(openapi_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = []
    paths = data.get('paths', {})
    for route, methods in paths.items():
        for method, details in methods.items():
            summary = details.get('summary', '')
            output.append(f"### `{method.upper()} {route}`\n- {summary}\n")
    return "\n".join(output)

def extract_changelog(changelog_path, lines=30):
    with open(changelog_path, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines()[:lines])

def generate_readme(template_path, output_path, openapi_path, changelog_path):
    template = Path(template_path).read_text(encoding='utf-8')
    api_doc = extract_openapi_doc(openapi_path)
    changelog = extract_changelog(changelog_path)

    result = (
        template.replace("{{OPENAPI_DOC}}", api_doc)
                .replace("{{CHANGELOG}}", changelog)
    )
    Path(output_path).write_text(result, encoding='utf-8')

if __name__ == "__main__":
    generate_readme(
        BASE_DIR / "README.template.md",
        BASE_DIR.parent / "README.md",
        BASE_DIR / "openapi.json",
        BASE_DIR.parent / "CHANGELOG.md"
    )
