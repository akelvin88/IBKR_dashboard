import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.data_processor import IBKRDataProcessor
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="IBKR Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .positive {
        color: #0CCE6B;
    }
    .negative {
        color: #FF2B2B;
    }
    h1 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_processor(csv_path):
    """Load and cache the data processor."""
    processor = IBKRDataProcessor(csv_path)
    return processor

def format_number(value, is_percentage=False, decimals=2):
    """Format numbers for display."""
    if pd.isna(value):
        return "N/A"
    if is_percentage:
        color = "positive" if value >= 0 else "negative"
        return f'<span class="{color}">{value:.{decimals}f}%</span>'
    else:
        color = "positive" if value >= 0 else "negative"
        return f'<span class="{color}">${value:,.{decimals}f}</span>'

def main():
    st.title("📊 IBKR Performance Dashboard")
    st.markdown("Since Inception Performance Analysis - MWR Basis")
    
    # Sidebar configuration
    st.sidebar.header("📁 Data Input")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload IBKR CSV File", type=['csv'])
    
    csv_path = None
    
    # Use uploaded file or look for default files
    if uploaded_file is not None:
        # Save uploaded file temporarily
        csv_path = uploaded_file
    else:
        # Look for files in data folder
        data_files = []
        if os.path.exists('data'):
            data_files = [f for f in os.listdir('data') if f.endswith('.csv')]
        
        if data_files:
            selected_file = st.sidebar.selectbox("Or Select Local File", data_files)
            csv_path = os.path.join('data', selected_file)
        else:
            st.info("👈 Upload your IBKR CSV file using the file uploader in the sidebar")
            return
    
    if csv_path is None:
        return
    
    # Load data
    try:
        processor = load_processor(csv_path)
        performance_data = processor.get_performance_summary()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    if not performance_data:
        st.error("Could not parse performance data from the CSV file.")
        return
    
    stats = performance_data['stats']
    monthly_returns = performance_data['monthly_returns']
    mwr = performance_data['mwr']
    nav_data = performance_data['nav_values']
    
    # Top Metrics
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ending_nav = stats.get('ending_nav', 0)
        st.metric("Current NAV", f"${ending_nav:,.2f}")
    
    with col2:
        cumulative_return = stats.get('cumulative_return', 0)
        st.metric("Cumulative Return", f"{cumulative_return:.2f}%", 
                 delta=f"{cumulative_return:.2f}%", delta_color="normal")
    
    with col3:
        deposits = stats.get('deposits', 0)
        st.metric("Total Deposits", f"${deposits:,.2f}")
    
    with col4:
        fees = abs(stats.get('fees', 0))
        st.metric("Total Fees", f"${fees:,.2f}")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Monthly Performance", "Yearly Performance", "NAV Progression", "Data Table"])
    
    # Tab 1: Monthly Performance
    with tab1:
        st.subheader("Monthly Returns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly Returns Chart
            if not monthly_returns.empty:
                fig = go.Figure()
                
                colors = ['#0CCE6B' if x >= 0 else '#FF2B2B' for x in monthly_returns['return_pct']]
                
                fig.add_trace(go.Bar(
                    x=monthly_returns['year_month'],
                    y=monthly_returns['return_pct'],
                    marker=dict(color=colors),
                    name='Return %',
                    hovertemplate='%{x}<br>Return: %{y:.2f}%<extra></extra>'
                ))
                
                fig.update_layout(
                    title="Monthly Returns (%)",
                    xaxis_title="Month",
                    yaxis_title="Return (%)",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly Returns Value Chart
            if not nav_data.empty:
                fig = go.Figure()
                
                colors = ['#0CCE6B' if x >= 0 else '#FF2B2B' for x in nav_data['nav_change_value']]
                
                fig.add_trace(go.Bar(
                    x=nav_data['year_month'],
                    y=nav_data['nav_change_value'],
                    marker=dict(color=colors),
                    name='NAV Change',
                    hovertemplate='%{x}<br>Change: $%{y:,.2f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title="Monthly NAV Change ($)",
                    xaxis_title="Month",
                    yaxis_title="NAV Change ($)",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Monthly Returns Table
        st.subheader("Monthly Returns Table")
        monthly_display = monthly_returns.copy()
        monthly_display['return_pct'] = monthly_display['return_pct'].apply(lambda x: f"{x:.2f}%")
        
        if not nav_data.empty:
            nav_display = nav_data[['year_month', 'beginning_nav', 'ending_nav', 'nav_change_value']].copy()
            nav_display['beginning_nav'] = nav_display['beginning_nav'].apply(lambda x: f"${x:,.2f}")
            nav_display['ending_nav'] = nav_display['ending_nav'].apply(lambda x: f"${x:,.2f}")
            nav_display['nav_change_value'] = nav_display['nav_change_value'].apply(lambda x: f"${x:,.2f}")
            
            display_df = monthly_display.merge(nav_display, on='year_month')
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Tab 2: Yearly Performance
    with tab2:
        st.subheader("Yearly Returns")
        
        if mwr['by_year']:
            yearly_data = pd.DataFrame([
                {'Year': year, 'Return %': return_pct}
                for year, return_pct in mwr['by_year'].items()
            ]).sort_values('Year')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Yearly Returns Chart
                colors = ['#0CCE6B' if x >= 0 else '#FF2B2B' for x in yearly_data['Return %']]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=yearly_data['Year'].astype(str),
                    y=yearly_data['Return %'],
                    marker=dict(color=colors),
                    hovertemplate='%{x}<br>Return: %{y:.2f}%<extra></extra>'
                ))
                
                fig.update_layout(
                    title="Yearly Returns (%)",
                    xaxis_title="Year",
                    yaxis_title="Return (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Calculate cumulative wealth from yearly returns
                yearly_data_sorted = yearly_data.sort_values('Year')
                cumulative_value = [100]  # Base 100
                
                for _, row in yearly_data_sorted.iterrows():
                    new_value = cumulative_value[-1] * (1 + row['Return %'] / 100)
                    cumulative_value.append(new_value)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=yearly_data_sorted['Year'].astype(str),
                    y=cumulative_value[1:],
                    mode='lines+markers',
                    fill='tozeroy',
                    name='Cumulative Growth (Base 100)',
                    hovertemplate='%{x}<br>Value: %{y:,.2f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title="Cumulative Wealth (Base 100)",
                    xaxis_title="Year",
                    yaxis_title="Value",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Yearly Table
            st.subheader("Yearly Returns Table")
            yearly_display = yearly_data.copy()
            yearly_display['Return %'] = yearly_display['Return %'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(yearly_display, use_container_width=True, hide_index=True)
    
    # Tab 3: NAV Progression
    with tab3:
        st.subheader("NAV Progression Over Time")
        
        if not nav_data.empty:
            # Calculate cumulative deposits (approximated distribution across months)
            total_deposits = stats.get('deposits', 0)
            num_months = len(nav_data)
            
            # Distribute deposits across months (assuming even distribution after first deposit)
            monthly_deposit = total_deposits / max(1, num_months)
            cumulative_deposits = []
            running_total = 0
            
            for idx in range(num_months):
                running_total += monthly_deposit
                cumulative_deposits.append(running_total)
            
            fig = go.Figure()
            
            # NAV trace (primary y-axis)
            fig.add_trace(go.Scatter(
                x=nav_data['year_month'],
                y=nav_data['ending_nav'],
                mode='lines+markers',
                name='Account NAV',
                line=dict(color='#1f77b4', width=3),
                hovertemplate='%{x}<br>NAV: $%{y:,.2f}<extra></extra>'
            ))
            
            # Cumulative Deposits trace (secondary y-axis)
            fig.add_trace(go.Scatter(
                x=nav_data['year_month'],
                y=cumulative_deposits,
                mode='lines',
                name='Cumulative Deposits',
                line=dict(color='#FF9999', width=2, dash='dash'),
                yaxis='y2',
                hovertemplate='%{x}<br>Cumulative Deposits: $%{y:,.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Account NAV vs Cumulative Deposits Over Time",
                xaxis_title="Month",
                yaxis=dict(title="NAV ($)", titlefont=dict(color='#1f77b4'), tickfont=dict(color='#1f77b4')),
                yaxis2=dict(title="Cumulative Deposits ($)", titlefont=dict(color='#FF9999'), tickfont=dict(color='#FF9999'), overlaying='y', side='right'),
                hovermode='x unified',
                height=500,
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # NAV Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                min_nav = nav_data['ending_nav'].min()
                st.metric("Lowest NAV", f"${min_nav:,.2f}")
            
            with col2:
                max_nav = nav_data['ending_nav'].max()
                st.metric("Highest NAV", f"${max_nav:,.2f}")
            
            with col3:
                current_nav = nav_data['ending_nav'].iloc[-1]
                recovery_pct = ((current_nav / min_nav) - 1) * 100
                st.metric("Recovery from Low", f"{recovery_pct:.2f}%")
            
            with col4:
                avg_monthly_change = nav_data['nav_change_value'].mean()
                st.metric("Avg Monthly Change", f"${avg_monthly_change:,.2f}")
    
    # Tab 4: Data Table
    with tab4:
        st.subheader("Detailed Performance Data")
        
        if not nav_data.empty:
            detail_df = nav_data.copy()
            detail_df['return_pct'] = detail_df['return_pct'].apply(lambda x: f"{x:.2f}%")
            detail_df['beginning_nav'] = detail_df['beginning_nav'].apply(lambda x: f"${x:,.2f}")
            detail_df['ending_nav'] = detail_df['ending_nav'].apply(lambda x: f"${x:,.2f}")
            detail_df['nav_change_value'] = detail_df['nav_change_value'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(detail_df, use_container_width=True, hide_index=True)
            
            # Export option
            if st.button("📥 Export as CSV"):
                nav_data.to_csv('ibkr_performance_export.csv', index=False)
                st.success("Data exported to 'ibkr_performance_export.csv'")

if __name__ == "__main__":
    main()
