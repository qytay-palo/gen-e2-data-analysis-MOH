#!/usr/bin/env python3
"""
Automated Data Analysis Framework
Integrates knowledge-work-plugins/data commands for automated healthcare analytics
"""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/audit/auto_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutomatedAnalyzer:
    """Automated data analysis orchestrator using data plugin patterns"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.data_raw = self.project_root / "data" / "1_raw" / "kaggle"
        self.data_processed = self.project_root / "data" / "4_processed"
        self.reports_dir = self.project_root / "reports"
        self.results_dir = self.project_root / "results"
        
        # Create directories if needed
        self.data_processed.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        (self.results_dir / "metrics").mkdir(parents=True, exist_ok=True)
        
        # Analysis prompts from data plugin
        self.prompt_templates = self._load_prompt_templates()
        
    def _load_prompt_templates(self) -> Dict:
        """Load data plugin command templates"""
        prompts_dir = self.project_root / ".github" / "prompts" / "data-plugin" / "commands"
        templates = {}
        
        for prompt_file in prompts_dir.glob("*.md"):
            command_name = prompt_file.stem
            with open(prompt_file, 'r') as f:
                templates[command_name] = f.read()
        
        logger.info(f"Loaded {len(templates)} prompt templates")
        return templates
    
    def analyze_dataset(self, dataset_path: str, analysis_type: str = "explore") -> Dict:
        """
        Run automated analysis on a dataset
        
        Args:
            dataset_path: Path to CSV file
            analysis_type: One of 'explore', 'analyze', 'validate'
        
        Returns:
            Dict with analysis results
        """
        logger.info(f"Starting {analysis_type} analysis on {dataset_path}")
        
        # Load data
        df = pd.read_csv(dataset_path)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "dataset": str(dataset_path),
            "analysis_type": analysis_type,
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "columns": list(df.columns),
        }
        
        if analysis_type == "explore":
            results.update(self._explore_data(df))
        elif analysis_type == "analyze":
            results.update(self._analyze_patterns(df))
        elif analysis_type == "validate":
            results.update(self._validate_data(df))
        
        # Save results
        self._save_results(results, dataset_path, analysis_type)
        
        return results
    
    def _explore_data(self, df: pd.DataFrame) -> Dict:
        """Profile and explore dataset (implements /explore-data command)"""
        exploration = {
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "numeric_summary": {},
            "categorical_summary": {},
            "unique_counts": df.nunique().to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
        }
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            exploration["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols[:10]:  # Limit to first 10 to avoid huge output
            value_counts = df[col].value_counts()
            exploration["categorical_summary"][col] = {
                "unique_values": len(value_counts),
                "top_5_values": value_counts.head(5).to_dict(),
                "cardinality": len(value_counts) / len(df)
            }
        
        # Data quality flags
        quality_flags = []
        for col in df.columns:
            null_pct = df[col].isnull().sum() / len(df) * 100
            if null_pct > 20:
                quality_flags.append(f"{col}: High missing values ({null_pct:.1f}%)")
            if null_pct > 0 and null_pct < 5:
                quality_flags.append(f"{col}: Low missing values ({null_pct:.1f}%)")
        
        exploration["quality_flags"] = quality_flags
        
        logger.info(f"Exploration complete: {len(df)} rows, {len(df.columns)} columns")
        return exploration
    
    def _analyze_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze trends and patterns (implements /analyze command)"""
        analysis = {
            "temporal_analysis": {},
            "trends": [],
            "correlations": {},
            "outliers": {},
        }
        
        # Detect date columns
        date_cols = []
        for col in df.columns:
            if 'date' in col.lower() or 'year' in col.lower() or 'time' in col.lower():
                date_cols.append(col)
        
        if date_cols:
            analysis["temporal_analysis"]["date_columns"] = date_cols
            for date_col in date_cols[:3]:  # Analyze up to 3 date columns
                try:
                    if df[date_col].dtype == 'object':
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    
                    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
                        analysis["temporal_analysis"][date_col] = {
                            "min": str(df[date_col].min()),
                            "max": str(df[date_col].max()),
                            "range_days": (df[date_col].max() - df[date_col].min()).days
                        }
                except Exception as e:
                    logger.warning(f"Could not parse date column {date_col}: {e}")
        
        # Correlation analysis for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Find strong correlations (|r| > 0.7)
            strong_corrs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_corrs.append({
                            "col1": corr_matrix.columns[i],
                            "col2": corr_matrix.columns[j],
                            "correlation": float(corr_value)
                        })
            analysis["correlations"]["strong_correlations"] = strong_corrs
        
        # Outlier detection using IQR method
        for col in numeric_cols[:10]:  # Limit to first 10 numeric columns
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
            if len(outliers) > 0:
                analysis["outliers"][col] = {
                    "count": len(outliers),
                    "percentage": len(outliers) / len(df) * 100,
                    "range": [float(outliers[col].min()), float(outliers[col].max())]
                }
        
        logger.info(f"Pattern analysis complete")
        return analysis
    
    def _validate_data(self, df: pd.DataFrame) -> Dict:
        """Validate data quality (implements /validate command)"""
        validation = {
            "row_count_check": len(df) > 0,
            "duplicate_rows": int(df.duplicated().sum()),
            "duplicate_percentage": float(df.duplicated().sum() / len(df) * 100),
            "completeness": {},
            "consistency_checks": [],
            "recommendations": []
        }
        
        # Completeness check
        for col in df.columns:
            complete_pct = (1 - df[col].isnull().sum() / len(df)) * 100
            validation["completeness"][col] = float(complete_pct)
            
            if complete_pct < 80:
                validation["recommendations"].append(
                    f"⚠️ {col}: Only {complete_pct:.1f}% complete - consider imputation or removal"
                )
            elif complete_pct == 100:
                validation["recommendations"].append(
                    f"✓ {col}: 100% complete"
                )
        
        # Check for duplicate rows
        if validation["duplicate_percentage"] > 5:
            validation["consistency_checks"].append(
                f"⚠️ Found {validation['duplicate_rows']} duplicate rows ({validation['duplicate_percentage']:.1f}%)"
            )
            validation["recommendations"].append("Consider deduplication")
        else:
            validation["consistency_checks"].append(
                f"✓ Low duplicate rate ({validation['duplicate_percentage']:.1f}%)"
            )
        
        # Check for columns with single value
        for col in df.columns:
            if df[col].nunique() == 1:
                validation["consistency_checks"].append(
                    f"⚠️ {col}: Contains only one unique value - consider removing"
                )
        
        logger.info(f"Validation complete: {len(validation['recommendations'])} recommendations")
        return validation
    
    def _save_results(self, results: Dict, dataset_path: str, analysis_type: str):
        """Save analysis results to JSON and generate summary"""
        # Save full results as JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_name = Path(dataset_path).stem
        
        results_file = self.results_dir / "metrics" / f"{dataset_name}_{analysis_type}_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {results_file}")
        
        # Generate markdown summary
        summary_file = self.reports_dir / f"{dataset_name}_{analysis_type}_{timestamp}.md"
        self._generate_markdown_report(results, summary_file)
    
    def _generate_markdown_report(self, results: Dict, output_file: Path):
        """Generate markdown report from analysis results"""
        lines = [
            f"# Automated Analysis Report: {results['analysis_type'].title()}",
            f"\n**Generated:** {results['timestamp']}",
            f"\n**Dataset:** `{results['dataset']}`",
            f"\n**Shape:** {results['shape']['rows']} rows × {results['shape']['columns']} columns",
            "\n---\n"
        ]
        
        if results['analysis_type'] == 'explore':
            lines.extend(self._format_exploration_report(results))
        elif results['analysis_type'] == 'analyze':
            lines.extend(self._format_analysis_report(results))
        elif results['analysis_type'] == 'validate':
            lines.extend(self._format_validation_report(results))
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Markdown report saved to {output_file}")
    
    def _format_exploration_report(self, results: Dict) -> List[str]:
        """Format exploration results as markdown"""
        lines = [
            "\n## Data Profile\n",
            f"- **Memory Usage:** {results.get('memory_usage_mb', 0):.2f} MB",
            f"- **Columns:** {len(results['columns'])}",
            "\n### Missing Values\n"
        ]
        
        missing = results.get('missing_percentage', {})
        if any(v > 0 for v in missing.values()):
            lines.append("| Column | Missing % |")
            lines.append("|--------|-----------|")
            for col, pct in sorted(missing.items(), key=lambda x: x[1], reverse=True):
                if pct > 0:
                    lines.append(f"| {col} | {pct:.2f}% |")
        else:
            lines.append("✓ No missing values detected\n")
        
        # Quality flags
        if results.get('quality_flags'):
            lines.append("\n### Data Quality Flags\n")
            for flag in results['quality_flags']:
                lines.append(f"- {flag}")
        
        return lines
    
    def _format_analysis_report(self, results: Dict) -> List[str]:
        """Format analysis results as markdown"""
        lines = ["\n## Pattern Analysis\n"]
        
        # Temporal analysis
        if results.get('temporal_analysis'):
            lines.append("\n### Temporal Coverage\n")
            for key, value in results['temporal_analysis'].items():
                if isinstance(value, dict):
                    lines.append(f"\n**{key}:**")
                    for k, v in value.items():
                        lines.append(f"- {k}: {v}")
        
        # Correlations
        if results.get('correlations', {}).get('strong_correlations'):
            lines.append("\n### Strong Correlations (|r| > 0.7)\n")
            lines.append("| Variable 1 | Variable 2 | Correlation |")
            lines.append("|------------|------------|-------------|")
            for corr in results['correlations']['strong_correlations']:
                lines.append(f"| {corr['col1']} | {corr['col2']} | {corr['correlation']:.3f} |")
        
        # Outliers
        if results.get('outliers'):
            lines.append("\n### Outliers Detected\n")
            lines.append("| Column | Count | Percentage |")
            lines.append("|--------|-------|------------|")
            for col, info in results['outliers'].items():
                lines.append(f"| {col} | {info['count']} | {info['percentage']:.2f}% |")
        
        return lines
    
    def _format_validation_report(self, results: Dict) -> List[str]:
        """Format validation results as markdown"""
        lines = ["\n## Data Validation Results\n"]
        
        # Overall stats
        lines.append(f"- **Total Rows:** {results.get('row_count_check', 'N/A')}")
        lines.append(f"- **Duplicate Rows:** {results.get('duplicate_rows', 0)} ({results.get('duplicate_percentage', 0):.2f}%)")
        
        # Consistency checks
        if results.get('consistency_checks'):
            lines.append("\n### Consistency Checks\n")
            for check in results['consistency_checks']:
                lines.append(f"- {check}")
        
        # Recommendations
        if results.get('recommendations'):
            lines.append("\n### Recommendations\n")
            for rec in results['recommendations']:
                lines.append(f"- {rec}")
        
        return lines
    
    def batch_analyze(self, data_directory: str, analysis_types: List[str] = None) -> Dict:
        """
        Run batch analysis on all CSV files in a directory
        
        Args:
            data_directory: Path to directory containing CSV files
            analysis_types: List of analysis types to run (default: ['explore', 'validate'])
        
        Returns:
            Dict with results for each file
        """
        if analysis_types is None:
            analysis_types = ['explore', 'validate']
        
        data_dir = Path(data_directory)
        csv_files = list(data_dir.glob("**/*.csv"))
        
        logger.info(f"Found {len(csv_files)} CSV files in {data_directory}")
        
        batch_results = {
            "timestamp": datetime.now().isoformat(),
            "files_processed": [],
            "summary": {}
        }
        
        for csv_file in csv_files:
            logger.info(f"Processing {csv_file.name}")
            file_results = {}
            
            for analysis_type in analysis_types:
                try:
                    result = self.analyze_dataset(str(csv_file), analysis_type)
                    file_results[analysis_type] = "completed"
                except Exception as e:
                    logger.error(f"Error analyzing {csv_file} with {analysis_type}: {e}")
                    file_results[analysis_type] = f"failed: {str(e)}"
            
            batch_results["files_processed"].append({
                "file": str(csv_file),
                "results": file_results
            })
        
        # Save batch summary
        summary_file = self.results_dir / "metrics" / f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(batch_results, f, indent=2, default=str)
        
        logger.info(f"Batch analysis complete. Summary saved to {summary_file}")
        return batch_results


def main():
    """Main entry point for automated analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Data Analysis Framework")
    parser.add_argument('--dataset', type=str, help='Path to CSV dataset')
    parser.add_argument('--type', type=str, choices=['explore', 'analyze', 'validate'], 
                       default='explore', help='Analysis type')
    parser.add_argument('--batch', type=str, help='Directory for batch processing')
    parser.add_argument('--batch-types', nargs='+', default=['explore', 'validate'],
                       help='Analysis types for batch processing')
    
    args = parser.parse_args()
    
    analyzer = AutomatedAnalyzer()
    
    if args.batch:
        # Batch processing mode
        logger.info(f"Starting batch analysis on {args.batch}")
        results = analyzer.batch_analyze(args.batch, args.batch_types)
        print(f"\n✓ Batch analysis complete. Processed {len(results['files_processed'])} files")
    
    elif args.dataset:
        # Single dataset mode
        logger.info(f"Starting {args.type} analysis on {args.dataset}")
        results = analyzer.analyze_dataset(args.dataset, args.type)
        print(f"\n✓ Analysis complete. Results saved to results/metrics/")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
