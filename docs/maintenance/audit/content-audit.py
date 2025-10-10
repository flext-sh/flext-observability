#!/usr/bin/env python3
"""
Documentation Content Audit System
==================================

Comprehensive content analysis and quality assessment for flext-observability documentation.

Features:
- File discovery and categorization
- Content freshness analysis
- Word count and readability assessment
- Missing sections identification
- TODO/FIXME marker tracking
- Quality scoring and recommendations

Usage:
    python docs/maintenance/audit/content-audit.py [--comprehensive] [--output-format json|markdown]
"""

import argparse
import json
import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


@dataclass
class ContentMetrics:
    """Content quality metrics for a documentation file."""

    file_path: str
    word_count: int = 0
    line_count: int = 0
    heading_count: int = 0
    link_count: int = 0
    code_block_count: int = 0
    list_item_count: int = 0
    table_count: int = 0
    todo_count: int = 0
    fixme_count: int = 0
    last_modified: datetime = field(default_factory=datetime.now)
    freshness_score: float = 0.0
    quality_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class AuditReport:
    """Comprehensive audit report for the documentation set."""

    timestamp: datetime = field(default_factory=datetime.now)
    total_files: int = 0
    files_audited: int = 0
    total_word_count: int = 0
    total_links: int = 0
    total_issues: int = 0
    critical_issues: int = 0
    warning_issues: int = 0
    info_issues: int = 0
    freshness_threshold_days: int = 30
    fresh_files: int = 0
    stale_files: int = 0
    file_metrics: Dict[str, ContentMetrics] = field(default_factory=dict)
    category_breakdown: Dict[str, int] = field(default_factory=dict)
    overall_quality_score: float = 0.0


class DocumentationAuditor:
    """Main documentation audit system."""

    def __init__(self, docs_root: Path, config_path: Optional[Path] = None):
        self.docs_root = docs_root
        self.config = self._load_config(config_path)
        self.report = AuditReport()

    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Load audit configuration."""
        default_config = {
            "freshness_threshold_days": 30,
            "min_words_per_file": 50,
            "max_external_links": 10,
            "quality_thresholds": {
                "excellent": 90,
                "good": 75,
                "fair": 60,
                "poor": 45
            },
            "required_sections": [
                "description", "usage", "examples", "api"
            ]
        }

        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)

        return default_config

    def discover_files(self) -> List[Path]:
        """Discover all markdown files in the documentation tree."""
        files = []
        for pattern in ["*.md", "*.mdx"]:
            files.extend(self.docs_root.rglob(pattern))

        # Filter out maintenance system files
        files = [f for f in files if "maintenance" not in str(f.relative_to(self.docs_root))]

        return sorted(files)

    def analyze_file(self, file_path: Path) -> ContentMetrics:
        """Analyze a single documentation file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ContentMetrics(
                file_path=str(file_path),
                issues=[f"Failed to read file: {e}"]
            )

        metrics = ContentMetrics(file_path=str(file_path))

        # Basic content metrics
        metrics.line_count = len(content.splitlines())
        metrics.word_count = len(content.split())

        # Structural analysis
        metrics.heading_count = len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE))
        metrics.link_count = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        metrics.code_block_count = len(re.findall(r'```', content))
        metrics.list_item_count = len(re.findall(r'^[\s]*[-*+]\s+', content, re.MULTILINE))
        metrics.table_count = len(re.findall(r'\|.*\|.*\|', content))

        # TODO/FIXME tracking
        metrics.todo_count = len(re.findall(r'\bTODO\b', content, re.IGNORECASE))
        metrics.fixme_count = len(re.findall(r'\bFIXME\b', content, re.IGNORECASE))

        # File metadata
        stat = file_path.stat()
        metrics.last_modified = datetime.fromtimestamp(stat.st_mtime)

        # Quality analysis
        self._analyze_quality(metrics, content)
        self._check_freshness(metrics)
        self._identify_issues(metrics, content)

        return metrics

    def _analyze_quality(self, metrics: ContentMetrics, content: str) -> None:
        """Analyze content quality and assign scores."""
        score = 100.0

        # Word count penalty
        if metrics.word_count < self.config["min_words_per_file"]:
            score -= 20
            metrics.recommendations.append("Consider expanding content (minimum 50 words)")

        # Structure quality
        if metrics.heading_count == 0:
            score -= 15
            metrics.issues.append("Missing heading structure")

        # Link density (too many or too few)
        link_density = metrics.link_count / max(metrics.word_count, 1) * 100
        if link_density > 5:
            score -= 10
            metrics.recommendations.append("High link density may distract readers")

        # Code examples
        if metrics.code_block_count == 0 and metrics.word_count > 200:
            score -= 10
            metrics.recommendations.append("Consider adding code examples")

        # TODO/FIXME penalties
        score -= (metrics.todo_count + metrics.fixme_count) * 5

        metrics.quality_score = max(0, score)

    def _check_freshness(self, metrics: ContentMetrics) -> None:
        """Check content freshness against thresholds."""
        days_since_update = (datetime.now() - metrics.last_modified).days
        threshold = self.config["freshness_threshold_days"]

        if days_since_update <= threshold:
            metrics.freshness_score = 100.0
        elif days_since_update <= threshold * 2:
            metrics.freshness_score = 75.0
        elif days_since_update <= threshold * 3:
            metrics.freshness_score = 50.0
        else:
            metrics.freshness_score = 25.0

        if metrics.freshness_score < 75:
            metrics.recommendations.append(f"Consider updating (last modified {days_since_update} days ago)")

    def _identify_issues(self, metrics: ContentMetrics, content: str) -> None:
        """Identify specific content issues."""
        # Check for broken internal references
        internal_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for link_text, link_target in internal_links:
            if not link_target.startswith('http') and not link_target.startswith('#'):
                # Check if relative file exists
                target_path = (Path(metrics.file_path).parent / link_target).resolve()
                if not target_path.exists() and not link_target.startswith('../'):
                    metrics.issues.append(f"Broken internal link: {link_target}")

        # Check for missing alt text (though we have no images currently)
        images_without_alt = re.findall(r'!\[\]\([^)]+\)', content)
        if images_without_alt:
            metrics.issues.append("Images found without alt text")

        # Check heading hierarchy
        headings = re.findall(r'^(#{1,6})\s+', content, re.MULTILINE)
        heading_levels = [len(h) for h in headings]
        if heading_levels and heading_levels[0] != 1:
            metrics.issues.append("Document should start with H1 heading")

        # Check for excessively long lines
        long_lines = [line for line in content.splitlines() if len(line) > 120]
        if len(long_lines) > 5:
            metrics.recommendations.append("Consider breaking long lines (>120 chars)")

    def run_audit(self, comprehensive: bool = False) -> AuditReport:
        """Run comprehensive documentation audit."""
        files = self.discover_files()
        self.report.total_files = len(files)
        self.report.freshness_threshold_days = self.config["freshness_threshold_days"]

        for file_path in files:
            metrics = self.analyze_file(file_path)
            self.report.file_metrics[str(file_path)] = metrics
            self.report.files_audited += 1

            # Aggregate statistics
            self.report.total_word_count += metrics.word_count
            self.report.total_links += metrics.link_count
            self.report.total_issues += len(metrics.issues)

            # Categorize issues
            for issue in metrics.issues:
                if any(keyword in issue.lower() for keyword in ['broken', 'missing', 'failed']):
                    self.report.critical_issues += 1
                else:
                    self.report.warning_issues += 1

            # Freshness tracking
            if metrics.freshness_score >= 75:
                self.report.fresh_files += 1
            else:
                self.report.stale_files += 1

            # Category breakdown
            category = self._categorize_file(file_path)
            self.report.category_breakdown[category] += 1

        # Calculate overall quality score
        total_score = sum(m.quality_score for m in self.report.file_metrics.values())
        self.report.overall_quality_score = total_score / max(len(self.report.file_metrics), 1)

        return self.report

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize documentation file by type."""
        path_str = str(file_path.relative_to(self.docs_root))

        if 'api' in path_str:
            return 'API Reference'
        elif 'guides' in path_str:
            return 'User Guides'
        elif 'architecture' in path_str:
            return 'Architecture'
        elif 'standards' in path_str:
            return 'Standards'
        elif 'examples' in path_str:
            return 'Examples'
        elif file_path.name in ['README.md', 'CLAUDE.md']:
            return 'Root Documentation'
        else:
            return 'General'

    def generate_report(self, output_format: str = 'markdown') -> str:
        """Generate audit report in specified format."""
        if output_format == 'json':
            return self._generate_json_report()
        else:
            return self._generate_markdown_report()

    def _generate_markdown_report(self) -> str:
        """Generate markdown audit report."""
        report_lines = [
            "# Documentation Audit Report",
            "",
            f"**Generated**: {self.report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Files Audited**: {self.report.files_audited}/{self.report.total_files}",
            "",
            "## 📊 Summary Statistics",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Word Count | {self.report.total_word_count:,} |",
            f"| Total Links | {self.report.total_links} |",
            f"| Fresh Files | {self.report.fresh_files}/{self.report.files_audited} |",
            f"| Overall Quality Score | {self.report.overall_quality_score:.1f}/100 |",
            "",
            "## 🚨 Issues Summary",
            "",
            f"- **Critical Issues**: {self.report.critical_issues}",
            f"- **Warning Issues**: {self.report.warning_issues}",
            f"- **Info Items**: {self.report.info_issues}",
            "",
            "## 📁 File Categories",
            "",
            "| Category | Count |",
            "|----------|-------|",
        ]

        for category, count in sorted(self.report.category_breakdown.items()):
            report_lines.append(f"| {category} | {count} |")

        report_lines.extend([
            "",
            "## 📋 File Details",
            "",
            "| File | Quality | Freshness | Issues | Words |",
            "|------|---------|-----------|--------|-------|",
        ])

        for file_path, metrics in sorted(self.report.file_metrics.items()):
            relative_path = Path(file_path).relative_to(self.docs_root)
            quality_icon = self._get_score_icon(metrics.quality_score)
            freshness_icon = self._get_score_icon(metrics.freshness_score)
            issue_count = len(metrics.issues)

            report_lines.append(
                f"| `{relative_path}` | {quality_icon} {metrics.quality_score:.0f} | "
                f"{freshness_icon} {metrics.freshness_score:.0f} | {issue_count} | {metrics.word_count:,} |"
            )

        report_lines.extend([
            "",
            "## 🔧 Recommendations",
            "",
            "### Priority Actions",
        ])

        # Group recommendations by priority
        priority_recs = defaultdict(list)

        for file_path, metrics in self.report.file_metrics.items():
            relative_path = Path(file_path).relative_to(self.docs_root)

            for rec in metrics.recommendations:
                if "updating" in rec.lower() or "stale" in rec.lower():
                    priority_recs["high"].append(f"`{relative_path}`: {rec}")
                elif "consider" in rec.lower() or "expand" in rec.lower():
                    priority_recs["medium"].append(f"`{relative_path}`: {rec}")
                else:
                    priority_recs["low"].append(f"`{relative_path}`: {rec}")

        for priority in ["high", "medium", "low"]:
            if priority_recs[priority]:
                report_lines.append(f"#### {priority.title()} Priority")
                report_lines.extend(f"- {rec}" for rec in priority_recs[priority])
                report_lines.append("")

        return "\n".join(report_lines)

    def _generate_json_report(self) -> str:
        """Generate JSON audit report."""
        # Convert dataclasses to dicts for JSON serialization
        file_metrics = {}
        for path, metrics in self.report.file_metrics.items():
            file_metrics[path] = {
                "file_path": metrics.file_path,
                "word_count": metrics.word_count,
                "line_count": metrics.line_count,
                "heading_count": metrics.heading_count,
                "link_count": metrics.link_count,
                "code_block_count": metrics.code_block_count,
                "list_item_count": metrics.list_item_count,
                "table_count": metrics.table_count,
                "todo_count": metrics.todo_count,
                "fixme_count": metrics.fixme_count,
                "last_modified": metrics.last_modified.isoformat(),
                "freshness_score": metrics.freshness_score,
                "quality_score": metrics.quality_score,
                "issues": metrics.issues,
                "recommendations": metrics.recommendations,
            }

        report_dict = {
            "timestamp": self.report.timestamp.isoformat(),
            "total_files": self.report.total_files,
            "files_audited": self.report.files_audited,
            "total_word_count": self.report.total_word_count,
            "total_links": self.report.total_links,
            "total_issues": self.report.total_issues,
            "critical_issues": self.report.critical_issues,
            "warning_issues": self.report.warning_issues,
            "info_issues": self.report.info_issues,
            "freshness_threshold_days": self.report.freshness_threshold_days,
            "fresh_files": self.report.fresh_files,
            "stale_files": self.report.stale_files,
            "file_metrics": file_metrics,
            "category_breakdown": dict(self.report.category_breakdown),
            "overall_quality_score": self.report.overall_quality_score,
        }

        return json.dumps(report_dict, indent=2)

    def _get_score_icon(self, score: float) -> str:
        """Get icon for quality/freshness score."""
        if score >= 90:
            return "🟢"
        elif score >= 75:
            return "🟡"
        elif score >= 60:
            return "🟠"
        else:
            return "🔴"


def main():
    """Main entry point for documentation audit."""
    parser = argparse.ArgumentParser(description="Documentation Content Audit System")
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run comprehensive analysis with detailed recommendations"
    )
    parser.add_argument(
        "--output-format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format for audit report"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to custom audit configuration file"
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        help="Save report to file instead of stdout"
    )

    args = parser.parse_args()

    # Initialize auditor
    docs_root = Path(__file__).parent.parent.parent
    auditor = DocumentationAuditor(docs_root, args.config)

    # Run audit
    print("🔍 Running documentation audit...")
    report = auditor.run_audit(args.comprehensive)

    # Generate report
    print("📊 Generating audit report...")
    report_content = auditor.generate_report(args.output_format)

    # Output report
    if args.output_file:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Report saved to {args.output_file}")
    else:
        print(report_content)


if __name__ == "__main__":
    main()