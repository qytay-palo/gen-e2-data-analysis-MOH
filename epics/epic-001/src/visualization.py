"""
Epic 001: Visualization Module
Create visualizations and interactive dashboards
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Optional
import logging


# Standard MOH color palette
MOH_COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF6600',
    'success': '#00CC66',
    'warning': '#FFCC00',
    'danger': '#CC0000',
    'neutral': '#666666'
}


class UtilizationVisualizer:
    """Create visualizations for utilization analysis"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize visualizer
        
        Args:
            logger: Logger instance (creates new if None)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.template = self._create_template()
    
    def _create_template(self):
        """Create standard Plotly template"""
        return go.layout.Template(
            layout=go.Layout(
                font={'family': 'Arial, sans-serif', 'size': 12},
                title={'font': {'size': 18, 'color': MOH_COLORS['primary']}},
                paper_bgcolor='white',
                plot_bgcolor='#F5F5F5'
            )
        )
    
    def plot_utilization_trend(
        self, 
        df: pd.DataFrame, 
        facility_id: Optional[str] = None
    ) -> go.Figure:
        """
        Plot utilization trend over time
        
        Args:
            df: DataFrame with utilization data
            facility_id: Specific facility to plot (None for aggregate)
            
        Returns:
            Plotly figure object
        """
        if facility_id:
            plot_df = df[df['hospital'] == facility_id].sort_values('year')
            title = f"Utilization Trend: {facility_id}"
        else:
            # Aggregate across all facilities
            plot_df = df.groupby('year')['utilization_rate_pct'].mean().reset_index()
            title = "Average Utilization Trend (All Facilities)"
        
        fig = px.line(
            plot_df,
            x='year',
            y='utilization_rate_pct',
            title=title,
            labels={'utilization_rate_pct': 'Utilization Rate (%)', 'year': 'Year'},
            markers=True
        )
        
        # Add optimal range shading
        fig.add_hrect(
            y0=70, y1=85,
            fillcolor=MOH_COLORS['success'],
            opacity=0.1,
            annotation_text="Optimal Range (70-85%)",
            annotation_position="top left"
        )
        
        # Add warning zone
        fig.add_hrect(
            y0=90, y1=100,
            fillcolor=MOH_COLORS['danger'],
            opacity=0.1,
            annotation_text="Bottleneck Zone (>90%)",
            annotation_position="top right"
        )
        
        fig.update_layout(template=self.template)
        
        return fig
    
    def plot_facility_ranking(self, profiles_df: pd.DataFrame) -> go.Figure:
        """
        Plot facility ranking by utilization
        
        Args:
            profiles_df: DataFrame with facility profiles
            
        Returns:
            Plotly figure object
        """
        sorted_df = profiles_df.sort_values('utilization_rate_pct_mean', ascending=True)
        
        # Color code by utilization level
        colors = sorted_df['utilization_rate_pct_mean'].apply(
            lambda x: MOH_COLORS['danger'] if x > 90 else
                     MOH_COLORS['warning'] if x > 85 else
                     MOH_COLORS['success'] if x >= 70 else
                     MOH_COLORS['neutral']
        )
        
        fig = go.Figure(go.Bar(
            x=sorted_df['utilization_rate_pct_mean'],
            y=sorted_df['hospital'],
            orientation='h',
            marker=dict(color=colors),
            text=sorted_df['utilization_rate_pct_mean'].round(1),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Facility Utilization Ranking",
            xaxis_title="Average Utilization Rate (%)",
            yaxis_title="Facility",
            height=max(400, len(sorted_df) * 25),
            template=self.template
        )
        
        # Add reference lines
        fig.add_vline(x=85, line_dash="dash", line_color=MOH_COLORS['success'],
                     annotation_text="Optimal (85%)")
        fig.add_vline(x=90, line_dash="dash", line_color=MOH_COLORS['danger'],
                     annotation_text="Bottleneck (90%)")
        
        return fig
    
    def plot_bottleneck_severity(self, bottleneck_df: pd.DataFrame) -> go.Figure:
        """
        Visualize bottleneck severity
        
        Args:
            bottleneck_df: DataFrame with bottleneck data
            
        Returns:
            Plotly figure object
        """
        fig = px.scatter(
            bottleneck_df,
            x='utilization_rate_pct',
            y='attendances_no',
            size='severity_score',
            color='severity_score',
            hover_data=['hospital', 'year', 'beds_no'],
            title="Bottleneck Severity Analysis",
            labels={
                'utilization_rate_pct': 'Utilization Rate (%)',
                'attendances_no': 'Annual Attendances',
                'severity_score': 'Severity Score'
            },
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(template=self.template)
        
        return fig
    
    def plot_capacity_gap(self, df: pd.DataFrame) -> go.Figure:
        """
        Plot capacity gap analysis
        
        Args:
            df: DataFrame with capacity gap data
            
        Returns:
            Plotly figure object
        """
        # Calculate average gap per facility
        gap_df = df.groupby('hospital').agg({
            'capacity_gap': 'mean',
            'utilization_rate_pct': 'mean'
        }).reset_index().sort_values('capacity_gap')
        
        # Color by surplus (negative gap) vs deficit (positive gap)
        colors = gap_df['capacity_gap'].apply(
            lambda x: MOH_COLORS['success'] if x < 0 else MOH_COLORS['danger']
        )
        
        fig = go.Figure(go.Bar(
            x=gap_df['capacity_gap'],
            y=gap_df['hospital'],
            orientation='h',
            marker=dict(color=colors),
            text=gap_df['capacity_gap'].round(0),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Facility Capacity Gap Analysis",
            xaxis_title="Capacity Gap (Attendances - Capacity)",
            yaxis_title="Facility",
            height=max(400, len(gap_df) * 25),
            template=self.template
        )
        
        fig.add_vline(x=0, line_dash="dash", line_color="black",
                     annotation_text="Balance Point")
        
        return fig
    
    def plot_utilization_distribution(self, df: pd.DataFrame) -> go.Figure:
        """
        Plot distribution of utilization rates
        
        Args:
            df: DataFrame with utilization data
            
        Returns:
            Plotly figure object
        """
        fig = px.histogram(
            df,
            x='utilization_rate_pct',
            nbins=30,
            title="Distribution of Facility Utilization Rates",
            labels={'utilization_rate_pct': 'Utilization Rate (%)', 'count': 'Frequency'}
        )
        
        # Add optimal range overlay
        fig.add_vrect(
            x0=70, x1=85,
            fillcolor=MOH_COLORS['success'],
            opacity=0.2,
            annotation_text="Optimal",
            annotation_position="top"
        )
        
        fig.update_layout(template=self.template)
        
        return fig
    
    def plot_multi_facility_comparison(
        self, 
        df: pd.DataFrame, 
        facilities: List[str]
    ) -> go.Figure:
        """
        Compare multiple facilities over time
        
        Args:
            df: DataFrame with utilization data
            facilities: List of facility names to compare
            
        Returns:
            Plotly figure object
        """
        plot_df = df[df['hospital'].isin(facilities)].sort_values(['hospital', 'year'])
        
        fig = px.line(
            plot_df,
            x='year',
            y='utilization_rate_pct',
            color='hospital',
            title="Multi-Facility Utilization Comparison",
            labels={'utilization_rate_pct': 'Utilization Rate (%)', 'year': 'Year'},
            markers=True
        )
        
        # Add optimal range
        fig.add_hrect(
            y0=70, y1=85,
            fillcolor=MOH_COLORS['success'],
            opacity=0.1,
            annotation_text="Optimal Range"
        )
        
        fig.update_layout(template=self.template)
        
        return fig
    
    def create_dashboard_layout(
        self, 
        utilization_df: pd.DataFrame,
        bottleneck_df: pd.DataFrame,
        profiles_df: pd.DataFrame
    ) -> Dict[str, go.Figure]:
        """
        Create all dashboard visualizations
        
        Args:
            utilization_df: DataFrame with utilization data
            bottleneck_df: DataFrame with bottlenecks
            profiles_df: DataFrame with facility profiles
            
        Returns:
            Dictionary of figure names to figure objects
        """
        self.logger.info("Creating dashboard visualizations...")
        
        figures = {
            'utilization_trend': self.plot_utilization_trend(utilization_df),
            'facility_ranking': self.plot_facility_ranking(profiles_df),
            'bottleneck_severity': self.plot_bottleneck_severity(bottleneck_df),
            'capacity_gap': self.plot_capacity_gap(utilization_df),
            'utilization_distribution': self.plot_utilization_distribution(utilization_df)
        }
        
        # Add comparison for top bottleneck facilities
        if len(bottleneck_df) > 0:
            top_bottlenecks = bottleneck_df.nlargest(5, 'severity_score')['hospital'].tolist()
            if len(top_bottlenecks) > 0:
                figures['top_bottlenecks_comparison'] = self.plot_multi_facility_comparison(
                    utilization_df,
                    top_bottlenecks
                )
        
        self.logger.info(f"Created {len(figures)} visualizations")
        return figures
    
    def save_figures(
        self, 
        figures: Dict[str, go.Figure], 
        output_dir: str,
        formats: List[str] = ['html', 'png']
    ):
        """
        Save all figures to disk
        
        Args:
            figures: Dictionary of figures
            output_dir: Output directory path
            formats: List of output formats ('html', 'png', 'pdf', 'svg')
        """
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, fig in figures.items():
            for fmt in formats:
                file_path = output_path / f"{name}.{fmt}"
                
                if fmt == 'html':
                    fig.write_html(str(file_path))
                elif fmt in ['png', 'pdf', 'svg']:
                    fig.write_image(str(file_path))
                
                self.logger.info(f"Saved {name}.{fmt}")
