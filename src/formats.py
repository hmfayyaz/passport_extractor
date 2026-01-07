import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

def export_to_spreadsheet(data_list, output_file, format='excel'):
    """
    Exports a list of dictionaries to a spreadsheet (Excel or CSV).
    """
    if not data_list:
        logger.warning("No data to export.")
        return False

    try:
        df = pd.DataFrame(data_list)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        if format.lower() == 'excel' or output_file.endswith('.xlsx'):
            if not output_file.endswith('.xlsx'):
                output_file += '.xlsx'
            df.to_excel(output_file, index=False)
            logger.info(f"Data exported to {output_file}")
            
        elif format.lower() == 'csv' or output_file.endswith('.csv'):
            if not output_file.endswith('.csv'):
                output_file += '.csv'
            df.to_csv(output_file, index=False)
            logger.info(f"Data exported to {output_file}")
            
        else:
            logger.error(f"Unsupported format: {format}")
            return False
            
        return True

    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        return False
