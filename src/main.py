from config import config  # Import the config instance instead of the module
import functions 
import os
import pandas as pd 
from logger import setup_logger

logger = setup_logger(__name__)

def create_dummy_file():
    logger.info("Starting to create dummy RPT file")    
    ### Create Dummy file
    output_file = os.path.join(config.output_dir, "dummy_report.rpt")
    structure = functions.create_dummy_rpt_file(output_file)
    
    # Print the structure for reference
    logger.info("\nDummy RPT File Structure:")
    logger.info("------------------------")
    logger.info("Tables and Fields:")
    for table_name, fields in structure["tables"].items():
        logger.info(f"  {table_name}")
        for field in fields:
            logger.info(f"    - {field}")
    
    logger.info("\nReport Sections:")
    for section in structure["sections"]:
        logger.info(f"  - {section}")

    logger.info("Dummy RPT file created successfully")  

# Main function
if __name__ == "__main__":
    logger.info("Starting Crystal Report Extractor")
    
    #create_dummy_file()

    input_file = os.path.join(config.input_dir, "dummy_report.rpt")
    rpt_df = functions.basic_rpt_parser(input_file)

    # Save the DataFrame to a CSV file
    csv_path = os.path.join(config.output_dir, "dummy_report.csv")
    rpt_df.to_csv(csv_path, index=False)
    # save the DataFrame to Excel
    excel_path = os.path.join(config.output_dir, "dummy_report.xlsx")
    rpt_df.to_excel(excel_path, index=False)            

    logger.info("Crystal Report Extractor completed")
    
