from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum

class DependencyType(str, Enum):
    """Types of dependencies that can exist between files."""
    IMPORT = "import"
    FROM_IMPORT = "from_import"
    RELATIVE_IMPORT = "relative_import"
    TYPE_HINT = "type_hint"  # For future: type hints
    INHERITANCE = "inheritance"  # For future: class inheritance
    COMPOSITION = "composition"  # For future: class composition

class DependencyEdge(BaseModel):
    """Represents a single dependency edge between files."""
    source: str
    target: str
    type: DependencyType
    line_number: Optional[int] = None
    imported_names: Optional[List[str]] = None
    metadata: Dict = Field(default_factory=dict)  # For future extensibility

class CouplingMetrics(BaseModel):
    """Metrics about a file's coupling with other files."""
    outbound: int = Field(description="Number of files this file imports")
    inbound: int = Field(description="Number of files that import this file")
    total: int = Field(description="Total number of dependencies")
    depth: Optional[int] = Field(None, description="Maximum depth of dependency chain")
    fan_in: Optional[int] = Field(None, description="Number of incoming dependencies")
    fan_out: Optional[int] = Field(None, description="Number of outgoing dependencies")
    metadata: Dict = Field(default_factory=dict)  # For future metrics

class FileAnalysis(BaseModel):
    """Analysis results for a single file."""
    path: str
    dependencies: List[DependencyEdge] = Field(default_factory=list)
    coupling: CouplingMetrics
    is_orphaned: bool = False
    is_part_of_cycle: bool = False
    metadata: Dict = Field(default_factory=dict)  # For future file-level metrics

class CircularDependency(BaseModel):
    """Represents a circular dependency chain."""
    files: List[str]
    severity: str = Field(description="Severity level of the circular dependency")
    suggested_fixes: Optional[List[str]] = None
    metadata: Dict = Field(default_factory=dict)  # For future analysis

class CodeQualityMetrics(BaseModel):
    """Overall code quality metrics."""
    total_files: int
    total_dependencies: int
    circular_dependencies_count: int
    orphaned_files_count: int
    average_coupling: float
    metadata: Dict = Field(default_factory=dict)  # For future metrics

class AnalysisInsights(BaseModel):
    """Insights derived from the dependency analysis."""
    circular_dependencies: List[CircularDependency] = Field(default_factory=list)
    high_coupling_hotspots: Dict[str, CouplingMetrics] = Field(default_factory=dict)
    orphaned_files: List[str] = Field(default_factory=list)
    coupling_scores: Dict[str, CouplingMetrics] = Field(default_factory=dict)
    quality_metrics: CodeQualityMetrics
    metadata: Dict = Field(default_factory=dict)  # For future insights

class RepositoryAnalysis(BaseModel):
    """Complete analysis of a repository."""
    files: List[str]
    dependencies: Dict[str, List[str]]
    insights: AnalysisInsights
    metadata: Dict = Field(default_factory=dict)  # For future repository-level metrics

    class Config:
        schema_extra = {
            "example": {
                "files": ["file1.py", "file2.py"],
                "dependencies": {
                    "file1.py": ["file2.py"]
                },
                "insights": {
                    "circular_dependencies": [],
                    "high_coupling_hotspots": {
                        "file1.py": {
                            "outbound": 1,
                            "inbound": 0,
                            "total": 1
                        }
                    },
                    "orphaned_files": [],
                    "coupling_scores": {
                        "file1.py": {
                            "outbound": 1,
                            "inbound": 0,
                            "total": 1
                        }
                    },
                    "quality_metrics": {
                        "total_files": 2,
                        "total_dependencies": 1,
                        "circular_dependencies_count": 0,
                        "orphaned_files_count": 0,
                        "average_coupling": 0.5
                    }
                }
            }
        } 