import os
import pandas as pd
import pdfplumber
import tabula
import camelot
from typing import List, Dict, Any, Optional, Tuple
from app.config import settings

def extract_tables_pdfplumber(pdf_path: str) -> List[pd.DataFrame]:
    """
    Extract tables from a PDF using pdfplumber.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of pandas DataFrames containing extracted tables
    """
    tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                for i, table in enumerate(page_tables):
                    if table and len(table) > 0:
                        # Convert to DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                        # Add metadata
                        df.attrs['source'] = 'pdfplumber'
                        df.attrs['page'] = page_num + 1
                        df.attrs['table_index'] = i
                        tables.append(df)
    except Exception as e:
        print(f"Error extracting tables with pdfplumber: {str(e)}")
    
    return tables

def extract_tables_tabula(pdf_path: str) -> List[pd.DataFrame]:
    """
    Extract tables from a PDF using tabula-py.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of pandas DataFrames containing extracted tables
    """
    tables = []
    
    try:
        # Extract all tables from the PDF
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        for i, df in enumerate(dfs):
            if not df.empty:
                # Add metadata
                df.attrs['source'] = 'tabula'
                df.attrs['table_index'] = i
                tables.append(df)
    except Exception as e:
        print(f"Error extracting tables with tabula: {str(e)}")
    
    return tables

def extract_tables_camelot(pdf_path: str) -> List[pd.DataFrame]:
    """
    Extract tables from a PDF using camelot.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of pandas DataFrames containing extracted tables
    """
    tables = []
    
    try:
        # Extract tables using camelot
        table_list = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        
        for i, table in enumerate(table_list):
            df = table.df
            if not df.empty:
                # Add metadata
                df.attrs['source'] = 'camelot'
                df.attrs['page'] = table.page
                df.attrs['table_index'] = i
                df.attrs['accuracy'] = table.accuracy
                tables.append(df)
    except Exception as e:
        print(f"Error extracting tables with camelot: {str(e)}")
    
    return tables

def extract_tables(pdf_path: str, methods: List[str] = None) -> Dict[str, List[pd.DataFrame]]:
    """
    Extract tables from a PDF using multiple methods for better results.
    
    Args:
        pdf_path: Path to the PDF file
        methods: List of extraction methods to use (pdfplumber, tabula, camelot)
        
    Returns:
        Dictionary with method names as keys and lists of DataFrames as values
    """
    if methods is None:
        methods = ['pdfplumber', 'tabula', 'camelot']
    
    results = {}
    
    if 'pdfplumber' in methods:
        results['pdfplumber'] = extract_tables_pdfplumber(pdf_path)
    
    if 'tabula' in methods:
        results['tabula'] = extract_tables_tabula(pdf_path)
    
    if 'camelot' in methods:
        results['camelot'] = extract_tables_camelot(pdf_path)
    
    return results

def clean_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a table by removing empty rows/columns and fixing headers.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Drop rows where all elements are NaN
    cleaned_df = cleaned_df.dropna(how='all')
    
    # Drop columns where all elements are NaN
    cleaned_df = cleaned_df.dropna(axis=1, how='all')
    
    # If the first row contains header-like values, use it as header
    if cleaned_df.shape[0] > 0:
        # Check if first row has different data type than the rest
        first_row = cleaned_df.iloc[0]
        if all(isinstance(x, str) for x in first_row if pd.notna(x)):
            # Use first row as header
            cleaned_df.columns = first_row
            cleaned_df = cleaned_df.iloc[1:].reset_index(drop=True)
    
    # Replace NaN with empty string for better display
    cleaned_df = cleaned_df.fillna('')
    
    return cleaned_df

def save_tables_to_excel(tables: List[pd.DataFrame], output_path: str) -> bool:
    """
    Save extracted tables to an Excel file with multiple sheets.
    
    Args:
        tables: List of DataFrames to save
        output_path: Path to save the Excel file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, df in enumerate(tables):
                # Get metadata if available
                source = df.attrs.get('source', 'unknown')
                page = df.attrs.get('page', i+1)
                table_index = df.attrs.get('table_index', i)
                
                # Create sheet name
                sheet_name = f"{source}_p{page}_t{table_index}"
                
                # Excel sheet names must be <= 31 characters
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                
                # Save to Excel sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return True
    except Exception as e:
        print(f"Error saving tables to Excel: {str(e)}")
        return False

def get_table_preview(df: pd.DataFrame, max_rows: int = 10) -> Dict[str, Any]:
    """
    Get a preview of a table for display in the UI.
    
    Args:
        df: DataFrame to preview
        max_rows: Maximum number of rows to include in preview
        
    Returns:
        Dictionary with table preview information
    """
    # Get metadata
    metadata = {
        'source': df.attrs.get('source', 'unknown'),
        'page': df.attrs.get('page', 0),
        'table_index': df.attrs.get('table_index', 0),
        'accuracy': df.attrs.get('accuracy', None),
        'rows': df.shape[0],
        'columns': df.shape[1]
    }
    
    # Get column names
    columns = df.columns.tolist()
    
    # Get preview rows (limited to max_rows)
    preview_rows = df.head(max_rows).values.tolist()
    
    return {
        'metadata': metadata,
        'columns': columns,
        'preview_rows': preview_rows,
        'total_rows': df.shape[0]
    }

def merge_tables(tables: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge multiple tables into a single DataFrame.
    
    Args:
        tables: List of DataFrames to merge
        
    Returns:
        Merged DataFrame
    """
    if not tables:
        return pd.DataFrame()
    
    if len(tables) == 1:
        return tables[0]
    
    # Concatenate tables vertically
    merged_df = pd.concat(tables, ignore_index=True)
    
    return merged_df