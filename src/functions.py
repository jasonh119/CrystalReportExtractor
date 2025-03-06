import pandas as pd
from logger import setup_logger
import struct
import random
import os
from config import config

logger = setup_logger(__name__)

#add functions here
def create_dummy_rpt_file(output_path):
    """
    Create a dummy file that mimics some aspects of an RPT file structure.
    This is NOT a valid Crystal Reports file but can be used for testing parsers.
    
    Args:
        output_path (str): Path where the dummy RPT file will be saved
    """
    # Start with a header that looks somewhat like Crystal Reports
    header = b"CR\x00\x0A\x00\x00\x00"
    
    # Add some metadata sections
    metadata = b"METADATA\x00" + struct.pack("<I", random.randint(1000, 9999))
    
    # Create dummy table definitions
    tables = []
    table_names = ["Customers", "Orders", "Products", "Employees"]
    
    for table_name in table_names:
        # Table header
        table_header = f"TABLE:{table_name}\x00".encode()
        
        # Fields for this table
        fields = []
        if table_name == "Customers":
            field_names = ["CustomerID", "Name", "Address", "City", "Country", "Phone"]
        elif table_name == "Orders":
            field_names = ["OrderID", "CustomerID", "OrderDate", "ShipDate", "Total"]
        elif table_name == "Products":
            field_names = ["ProductID", "Name", "Category", "UnitPrice", "UnitsInStock"]
        else:  # Employees
            field_names = ["EmployeeID", "FirstName", "LastName", "Title", "HireDate"]
        
        for field_name in field_names:
            # Field definition with name and type
            field_type = random.choice([1, 2, 3, 4, 5])  # Random type codes
            field_def = f"FIELD:{field_name}:TYPE{field_type}\x00".encode()
            fields.append(field_def)
        
        # Combine all fields for this table
        fields_data = b"".join(fields)
        
        # Create table structure with header and fields
        table_size = len(table_header) + len(fields_data) + 4
        table_data = table_header + struct.pack("<I", table_size) + fields_data
        tables.append(table_data)
    
    # Combine all tables
    tables_data = b"".join(tables)
    
    # Add some report sections
    sections = []
    section_names = ["ReportHeader", "PageHeader", "Details", "PageFooter", "ReportFooter"]
    
    for section_name in section_names:
        section_header = f"SECTION:{section_name}\x00".encode()
        section_size = random.randint(100, 500)
        section_data = section_header + struct.pack("<I", section_size) + os.urandom(section_size - len(section_header) - 4)
        sections.append(section_data)
    
    # Combine all sections
    sections_data = b"".join(sections)
    
    # Add some formulas
    formulas_data = b"FORMULAS\x00" + struct.pack("<I", 256) + os.urandom(256)
    
    # Combine everything into the final file
    file_data = header + metadata + tables_data + sections_data + formulas_data
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(file_data)
    
    print(f"Dummy RPT file created at: {output_path}")
    print(f"File size: {len(file_data)} bytes")
    print(f"Contains {len(table_names)} tables with fields")
    
    # Return structure information for reference
    return {
        "tables": {name: field_names for name, field_names in zip(table_names, 
                  [["CustomerID", "Name", "Address", "City", "Country", "Phone"],
                   ["OrderID", "CustomerID", "OrderDate", "ShipDate", "Total"],
                   ["ProductID", "Name", "Category", "UnitPrice", "UnitsInStock"],
                   ["EmployeeID", "FirstName", "LastName", "Title", "HireDate"]])},
        "sections": section_names
    }

def basic_rpt_parser(rpt_path):
    try:
        logger.info(f"Starting to parse RPT file: {rpt_path}")
        with open(rpt_path, 'rb') as f:
            data = f.read()
        
        logger.info(f"File size: {len(data)} bytes")
        
        # Look for text strings that might represent table/field names
        import re
        
        # Extract all printable ASCII strings of reasonable length
        string_pattern = re.compile(b'[\x20-\x7E]{3,50}')
        strings = string_pattern.findall(data)
        
        # Filter for potential table/field names
        potential_fields = []
        for s in strings:
            decoded = s.decode('ascii', errors='ignore')
            # Apply heuristics to identify potential field names
            if '.' in decoded and not ' ' in decoded:
                potential_fields.append(decoded)
        
        logger.info("\nPotential table/field references:")
        for field in sorted(set(potential_fields)):
            logger.info(f"  - {field}")
        
        # Create a DataFrame from the extracted fields
        field_data = []
        for field in sorted(set(potential_fields)):
            parts = field.split('.')
            if len(parts) >= 2:
                table_name = parts[0]
                field_name = '.'.join(parts[1:])  # Handle multiple dots
                field_data.append({
                    'table': table_name,
                    'field': field_name,
                    'full_reference': field
                })
            else:
                field_data.append({
                    'table': 'Unknown',
                    'field': field,
                    'full_reference': field
                })
        
        # Create the DataFrame
        df = pd.DataFrame(field_data)
        
        # If DataFrame is empty, return an empty DataFrame with the correct columns
        if df.empty:
            return pd.DataFrame(columns=['table', 'field', 'full_reference'])
            
        return df
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return pd.DataFrame(columns=['table', 'field', 'full_reference'])  # Return empty DataFrame on error