# 3D Mesh Validation Script

This script performs various checks on 3D mesh files (STL format) to ensure their integrity and quality. It's useful for quality control in the medical prosthetics and surgical engineering industries.

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - trimesh
  - matplotlib
  - numpy
  - tqdm
  - etc. that are enumerated in the requirements.txt

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Setup

1. Clone or download this repository to your local machine.
2. Ensure you have a `mesh.ini` configuration file in the same directory as the script.

## Configuration

The script uses a `mesh.ini` file for configuration. Here are the available options:

- `PathToSTLFiles`: Directory containing the STL files to validate
- `ValidatedFileEndings`: List of valid file extensions (e.g., `["stl", "STL"]`)
- `MaximumFilesForVerbosity`: Maximum number of files for verbose output
- `ThreshForTriAngle`: Minimum allowed angle for triangles (in degrees)
- `ThreshForAngleDefect`: Threshold for detecting sharp vertices
- `IncludeCheckFour`: Whether to check for thin triangles (y/n)
- `IncludeCheckFive`: Whether to check for sharp vertices (y/n)
- `IncludeConsistentWinding`: Whether to check for consistent winding (y/n)

Example `mesh.ini`:

```ini
[DEFAULT]
PathToSTLFiles = /path/to/stl/files/
ValidatedFileEndings = ["stl", "STL"]
MaximumFilesForVerbosity = 10
ThreshForTriAngle = 5
ThreshForAngleDefect = 0.1
IncludeCheckFour = y
IncludeCheckFive = y
IncludeConsistentWinding = y
```

## Running the Script

To run the script, use the following command in your terminal:

```
python surfaceValidator.py
```

## Checks Performed

The script performs the following checks on each mesh:

1. Volume is defined and positive
2. Edges are manifold
3. Vertices are manifold
4. Shape is watertight (no holes)
5. Triangle angles are not too small (optional)
6. No abnormal sharp points (optional)
7. Winding is consistent (optional)

## Output

- For a small number of files (defined by `MaximumFilesForVerbosity`), the script provides verbose output for each check.
- For a large number of files, it uses a progress bar and only outputs errors.
- If issues are found, the script will raise an exception with a description of the problem and may display the problematic mesh.
- In select cases, the program will try to fix the found error (in select holes in the mesh) and show you the changes

## Customization

You can customize the script's behavior by modifying the `mesh.ini` file:

- Adjust `ThreshForTriAngle` to change the minimum allowed angle for triangles.
- Modify `ThreshForAngleDefect` to adjust the sensitivity for detecting sharp vertices.
- Set `IncludeCheckFour`, `IncludeCheckFive`, and `IncludeConsistentWinding` to 'y' or 'n' to enable or disable specific checks.

## Troubleshooting

- If you encounter a "RuntimeError: The target directory doesn't exist", make sure the `PathToSTLFiles` in your `mesh.ini` is correct and the directory exists and there are no quotations over the path.
- If you get import errors, ensure all required packages are installed.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes.