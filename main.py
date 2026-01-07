import argparse
import os
import sys
from tqdm import tqdm
from src.extractor import PassportExtractor
from src.formats import export_to_spreadsheet
from src.validators import validate_passport_data
from src.utils import setup_logger
from config.settings import ALLOWED_EXTENSIONS

# Setup Logger
logger = setup_logger()

def is_valid_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def main():
    parser = argparse.ArgumentParser(description="Passport OCR Tool - Extract data from passport images/PDFs.")
    parser.add_argument('--input', '-i', required=True, help="Path to input file or directory")
    parser.add_argument('--output', '-o', default='passport_data', help="Output filename (without extension)")
    parser.add_argument('--format', '-f', choices=['excel', 'csv'], default='excel', help="Output format (excel or csv)")
    parser.add_argument('--gpu', action='store_true', help="Use GPU for OCR")
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(os.path.join('data', 'output', args.output)) # Default to data/output if relative
    
    # Adjust output path if user provided a specific path
    if os.path.dirname(args.output):
        output_path = os.path.abspath(args.output)

    if not os.path.exists(input_path):
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)

    files_to_process = []
    if os.path.isfile(input_path):
        if is_valid_file(input_path):
            files_to_process.append(input_path)
        else:
            logger.error(f"Unsupported file format: {input_path}")
            sys.exit(1)
    else:
        for root, _, files in os.walk(input_path):
            for file in files:
                if is_valid_file(file):
                    files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        logger.warning("No valid files found to process.")
        sys.exit(0)

    logger.info(f"Found {len(files_to_process)} files to process.")

    # Initialize Extractor
    extractor = PassportExtractor(use_gpu=args.gpu)
    
    extracted_results = []
    
    # Process files
    for file_path in tqdm(files_to_process, desc="Processing files"):
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                results = extractor.process_pdf(file_path)
                extracted_results.extend(results)
            else:
                result = extractor.get_data(file_path)
                if result:
                    extracted_results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")

    # Validate and Summarize
    valid_count = 0
    for res in extracted_results:
        errors = validate_passport_data(res)
        if not errors:
            valid_count += 1
        else:
            res['validation_errors'] = "; ".join(errors)
            # logger.warning(f"Validation issues for {res.get('source_file')}: {errors}")

    logger.info(f"Processing complete. Extracted {len(extracted_results)} records ({valid_count} valid).")

    # Export
    if extracted_results:
        success = export_to_spreadsheet(extracted_results, output_path, format=args.format)
        if success:
            logger.info(f"Successfully saved data to {output_path}.{args.format if not output_path.endswith(args.format) else ''}")
    else:
        logger.warning("No data extracted.")

if __name__ == "__main__":
    main()
