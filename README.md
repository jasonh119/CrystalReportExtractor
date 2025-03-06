# Crystal Report Extractor

A Python utility for extracting and analyzing Crystal Report (.rpt) files without requiring Crystal Reports to be installed.

## Overview

Crystal Report Extractor allows you to:
- Parse Crystal Report (.rpt) files
- Extract table and field references
- Export the extracted data to CSV and Excel formats
- Create dummy .rpt files for testing purposes

## Project Structure

```
CrystalReportExtractor/
├── config.yaml         # Configuration settings
├── src/
│   ├── main.py         # Main application entry point
│   ├── functions.py    # Core functionality
│   ├── config.py       # Configuration handling
│   └── logger.py       # Logging setup
├── input/              # Directory for input .rpt files
├── output/             # Directory for output files (CSV, Excel)
└── logs/               # Application logs
```

## Features

- **RPT File Parsing**: Extract table and field references from Crystal Report files
- **Data Extraction**: Convert report data into structured formats (DataFrame)
- **Export Capabilities**: Save extracted data as CSV and Excel files
- **Dummy File Generation**: Create test .rpt files with sample data structure
- **Configurable**: Easy to configure via YAML configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CrystalReportExtractor.git
cd CrystalReportExtractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the required directories exist:
```bash
mkdir -p input output logs
```

## Usage

### Basic Usage

```bash
python src/main.py
```

### Creating a Dummy RPT File

```python
from src.functions import create_dummy_rpt_file

output_file = "path/to/output/dummy_report.rpt"
structure = create_dummy_rpt_file(output_file)
```

### Parsing an RPT File

```python
from src.functions import basic_rpt_parser

input_file = "path/to/input/report.rpt"
rpt_df = basic_rpt_parser(input_file)

# Save to CSV and Excel
rpt_df.to_csv("output.csv", index=False)
rpt_df.to_excel("output.xlsx", index=False)
```

## Configuration

Edit the `config.yaml` file to customize:
- Input and output directories
- Logging settings
- Application name and version

## Requirements

- Python 3.6+
- pandas (for data manipulation)
- openpyxl (for Excel export)
- pyyaml (for configuration)
- python-dotenv (for environment variables)
- pywin32 (for Windows-specific functionality)
- colorlog (for colored log output)
- pathlib (for path manipulation)

All dependencies are listed in the `requirements.txt` file and can be installed with:
```bash
pip install -r requirements.txt
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
