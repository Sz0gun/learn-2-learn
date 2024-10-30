import toml
import subprocess
import json

# Define path to pyproject.toml for both Django and FastAPI
DJANGO_TOML_PATH = "backend/django/pyproject.toml"
FASTAPI_TOML_PATH = "backend/fastapi/pyproject.toml"

#  Load dependencies from pyproject.toml
def load_dependencies(pyproject_path):

    try:
        with open(pyproject_path, "r") as file:
            pyproject_data = toml.load(file)
            dependencies = pyproject_data["tool"]["poetry"]["dependencies"]
            return dependencies
    except FileNotFoundError:
        print (f"Error: pyproject.toml not found at {pyproject_path}")
        return None
    except KeyError as e:
        print (f"Error parsing {pyproject_path}: {e}")
        return None

# Extract the currently installed packages from the environment

def get_installed_packages():
    try:
        # Run pip freeze and capture the output
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True), check=True)
        installed_packages = result.stdout.splitnlines()
        installed_dict = {}
        for pkg in installed_packages:
            if '==' in pkg:
                name, version = pkg.split('==')
                installed_dict[name.lower()] = version
        return installed_dict
    except subprocess.CalledProcessError as e:
        print(f"Error occured when trying to get installed packages: {e}")
        return {}

# Validate dependencies against the installed packages

def validate_dependencies(dependencies, installed_packages):
    mismatches = []
    for package, version in dependencies.items():
        if package.lower() in installed_packages:
            installed_version = installed_packages[package.lower()]
            if version != installed_version:
                mismatches.append({
                    "package": package,
                    "expected": version,
                    "installed": installed_version
                })
        else:
            mismatches.append({
                "package": package,
                "expected": version,
                "installed": "Not installed"
            })
    return mismatches

# Main function to execute the validation for both Django and FastAPI

def main():
    django_dependencies = load_dependencies(DJANGO_TOML_PATH)
    fastapi_dependencies = load_dependencies(FASTAPI_TOML_PATH)

    installed_packages = get_installed_packages()

    if django_dependencies:
        print("\nValidating Django dependencies:")
        mismatches = validate_dependencies(django_dependencies, installed_packages)
        if mismatches:
            for mismatch in mismatches:
                package, expected_version, installed_version = mismatch
                print(f"Mismatch for {package}: Expected version {expected_version}, Installed version {installed_version}")
        else:
            print("All Django dependencies are correctly installed.")

    if fastapi_dependencies:
        print("\nValidating FastAPI dependencies:")
        mismatches = validate_dependencies(fastapi_dependencies, installed_packages)
        if mismatches:
            for mismatch in mismatches:
                package, expected_version, installed_version = mismatch
                print(f"Mismatch for {package}: Expected version {expected_version}, Installed version {installed_version}")
        else:
            print("All FastAPI dependencies are correctly installed.")

if __name__ == "__main__":
    main()