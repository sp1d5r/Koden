from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum

class DependencyType(str, Enum):
    """Types of dependencies that can exist between files."""
    IMPORT = "import"
    FROM_IMPORT = "from_import"
    RELATIVE_IMPORT = "relative_import"
    TYPE_HINT = "type_hint"
    INHERITANCE = "inheritance"
    COMPOSITION = "composition"

class ComplexityMetrics(BaseModel):
    """Metrics about code complexity."""
    loc: int = Field(description="Lines of code")
    function_count: int = Field(description="Number of functions/methods")
    class_count: int = Field(description="Number of classes")
    max_nesting_depth: int = Field(description="Maximum nesting depth")
    cyclomatic_complexity: float = Field(description="Average cyclomatic complexity")
    comment_ratio: float = Field(description="Ratio of comments to code")
    metadata: Dict = Field(default_factory=dict)

class DependencyEdge(BaseModel):
    """Represents a single dependency edge between files."""
    source: str
    target: str
    type: DependencyType
    line_number: Optional[int] = None
    imported_names: Optional[List[str]] = None
    metadata: Dict = Field(default_factory=dict)

class CouplingMetrics(BaseModel):
    """Metrics about a file's coupling with other files."""
    outbound: int = Field(description="Number of files this file imports")
    inbound: int = Field(description="Number of files that import this file")
    total: int = Field(description="Total number of dependencies")
    depth: Optional[int] = Field(None, description="Maximum depth of dependency chain")
    fan_in: Optional[int] = Field(None, description="Number of incoming dependencies")
    fan_out: Optional[int] = Field(None, description="Number of outgoing dependencies")
    metadata: Dict = Field(default_factory=dict)

class FileAnalysis(BaseModel):
    """Analysis results for a single file."""
    path: str
    dependencies: List[DependencyEdge] = Field(default_factory=list)
    coupling: CouplingMetrics
    complexity: Optional[ComplexityMetrics] = None
    is_orphaned: bool = False
    is_part_of_cycle: bool = False
    risk_score: Optional[float] = Field(None, description="Combined risk score based on complexity and coupling")
    metadata: Dict = Field(default_factory=dict)

class CircularDependency(BaseModel):
    """Represents a circular dependency chain."""
    files: List[str]
    severity: str = Field(description="Severity level of the circular dependency")
    suggested_fixes: Optional[List[str]] = None
    metadata: Dict = Field(default_factory=dict)

class CodeQualityMetrics(BaseModel):
    """Overall code quality metrics."""
    total_files: int
    total_dependencies: int
    circular_dependencies_count: int
    orphaned_files_count: int
    average_coupling: float
    average_complexity: Optional[ComplexityMetrics] = None
    high_risk_files: List[str] = Field(default_factory=list, description="Files with high complexity and coupling")
    metadata: Dict = Field(default_factory=dict)

class AnalysisInsights(BaseModel):
    """Insights derived from the dependency analysis."""
    circular_dependencies: List[CircularDependency] = Field(default_factory=list)
    high_coupling_hotspots: Dict[str, CouplingMetrics] = Field(default_factory=dict)
    high_complexity_files: Dict[str, ComplexityMetrics] = Field(default_factory=dict)
    high_risk_files: Dict[str, FileAnalysis] = Field(default_factory=dict)
    orphaned_files: List[str] = Field(default_factory=list)
    coupling_scores: Dict[str, CouplingMetrics] = Field(default_factory=dict)
    quality_metrics: CodeQualityMetrics
    metadata: Dict = Field(default_factory=dict)

class RepositoryAnalysis(BaseModel):
    """Complete analysis of a repository."""
    files: List[str]
    dependencies: Dict[str, List[str]]
    insights: AnalysisInsights
    metadata: Dict = Field(default_factory=dict) 