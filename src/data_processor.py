import pandas as pd
import numpy as np
from datetime import datetime
from pyxirr import xirr
from typing import Dict, List, Tuple
import csv
import re


class IBKRDataProcessor:
    """Process IBKR account statement data and calculate performance metrics."""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.raw_lines = None
        self.monthly_returns = None
        self.cash_flows = None
        self.nav_history = None
        
    def load_data(self):
        """Load and parse IBKR CSV data using csv module for proper quote handling."""
        # Handle both file paths and file-like objects (from streamlit upload)
        if isinstance(self.csv_path, str):
            with open(self.csv_path, 'r') as f:
                reader = csv.reader(f)
                self.raw_lines = list(reader)
        else:
            # File-like object from streamlit
            reader = csv.reader(self.csv_path)
            self.raw_lines = list(reader)
        return self.raw_lines
    
    def extract_monthly_returns(self):
        """Extract monthly returns from the raw data."""
        if self.raw_lines is None:
            self.load_data()
        
        # Find monthly data
        monthly_data = []
        i = 0
        while i < len(self.raw_lines):
            line = self.raw_lines[i]
            
            # Look for monthly performance data lines
            if (len(line) >= 11 and 
                line[0] == 'Historical Performance Benchmark Comparison' and 
                line[1] == 'Data' and 
                len(line[2]) == 6 and 
                line[2].isdigit() and
                line[9] == 'U3462773'):  # Account identifier
                
                month = line[2]
                # Account return is at position 10 (0-indexed)
                try:
                    account_return = line[10]
                    
                    # Handle missing data
                    if account_return == '-' or not account_return:
                        i += 1
                        continue
                    
                    return_pct = float(account_return)
                    monthly_data.append({
                        'month': month,
                        'year': int(month[:4]),
                        'year_month': f"{month[:4]}-{month[4:]}",
                        'return_pct': return_pct
                    })
                except (ValueError, TypeError, IndexError):
                    pass
            
            i += 1
        
        self.monthly_returns = pd.DataFrame(monthly_data)
        return self.monthly_returns
    
    def extract_key_statistics(self):
        """Extract key statistics from the data."""
        if self.raw_lines is None:
            self.load_data()
        
        stats = {}
        
        # Find Key Statistics Data row
        for line in self.raw_lines:
            if (len(line) >= 20 and 
                line[0] == 'Key Statistics' and 
                line[1] == 'Data'):
                
                try:
                    stats['beginning_nav'] = float(line[2]) if line[2] and line[2] != '0' else 0
                    stats['ending_nav'] = float(line[3])
                    stats['cumulative_return'] = float(line[4])
                    stats['one_month_return'] = float(line[5])
                    stats['three_month_return'] = float(line[7]) if len(line) > 7 else 0
                    stats['deposits'] = float(line[14])
                    stats['dividends'] = float(line[15]) if len(line) > 15 else 0
                    stats['interest'] = float(line[16]) if len(line) > 16 else 0
                    stats['fees'] = float(line[17]) if len(line) > 17 else 0
                    stats['mtm'] = float(line[13]) if len(line) > 13 else 0
                except (ValueError, TypeError, IndexError):
                    pass
        
        return stats
    
    def calculate_mwr(self, monthly_data: pd.DataFrame) -> Dict:
        """
        Calculate Money-Weighted Return (MWR) using XIRR method.
        This requires cash flow information which we'll calculate from returns and NAV changes.
        """
        # For MWR calculation, we need the actual cash flows and NAV values
        # Using month-end values
        
        mwr_by_month = {}
        mwr_by_year = {}
        
        # Calculate monthly MWR percentages
        for idx, row in monthly_data.iterrows():
            month_key = row['year_month']
            mwr_by_month[month_key] = row['return_pct']
        
        # Calculate yearly MWR from monthly returns
        if len(monthly_data) > 0:
            monthly_data_sorted = monthly_data.sort_values('year_month')
            
            for year in monthly_data_sorted['year'].unique():
                year_data = monthly_data_sorted[monthly_data_sorted['year'] == year]
                
                # Compound monthly returns for the year
                annual_return = 1.0
                for _, row in year_data.iterrows():
                    annual_return *= (1 + row['return_pct'] / 100)
                
                annual_return_pct = (annual_return - 1) * 100
                mwr_by_year[year] = annual_return_pct
        
        return {
            'by_month': mwr_by_month,
            'by_year': mwr_by_year
        }
    
    def calculate_nav_values(self, stats: Dict, monthly_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate estimated NAV values for each month based on returns.
        This is an approximation since we don't have exact cash flow timing.
        """
        if len(monthly_data) == 0:
            return pd.DataFrame()
        
        ending_nav = stats.get('ending_nav', 1000000)
        
        # Work backwards from ending NAV to calculate starting values
        nav_values = []
        running_nav = ending_nav
        
        # Sort by date descending to work backwards
        sorted_data = monthly_data.sort_values('year_month', ascending=False)
        
        for idx, row in sorted_data.iterrows():
            month_return_pct = row['return_pct']
            
            # Calculate previous month's NAV
            # NAV_current = NAV_previous * (1 + return%)
            # NAV_previous = NAV_current / (1 + return%)
            prev_nav = running_nav / (1 + month_return_pct / 100)
            nav_change = running_nav - prev_nav
            
            nav_values.append({
                'year_month': row['year_month'],
                'month': row['month'],
                'year': row['year'],
                'return_pct': month_return_pct,
                'beginning_nav': prev_nav,
                'ending_nav': running_nav,
                'nav_change_value': nav_change
            })
            
            running_nav = prev_nav
        
        nav_values.reverse()
        nav_df = pd.DataFrame(nav_values)
        return nav_df
    
    def get_performance_summary(self) -> Dict:
        """Get complete performance summary with MWR by month and year."""
        self.extract_monthly_returns()
        stats = self.extract_key_statistics()
        
        if self.monthly_returns is None or len(self.monthly_returns) == 0:
            return {}
        
        mwr_data = self.calculate_mwr(self.monthly_returns)
        nav_data = self.calculate_nav_values(stats, self.monthly_returns)
        
        return {
            'stats': stats,
            'monthly_returns': self.monthly_returns,
            'mwr': mwr_data,
            'nav_values': nav_data
        }
