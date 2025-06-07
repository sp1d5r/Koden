from typing import List, Optional, Set
from pydantic import BaseModel, Field
from fastapi import UploadFile
from ..domain.analysis import RepositoryAnalysis

class AnalysisRequest(BaseModel):
    """Request model for repository analysis."""
    ignore_patterns: Optional[Set[str]] = Field(
        default=None,
        description="Patterns of files to ignore during analysis"
    )

class AnalysisResponse(BaseModel):
    """Response model for repository analysis."""
    analysis: RepositoryAnalysis
    message: str = Field(
        default="Analysis completed successfully",
        description="Status message for the analysis"
    )

    class Config:
        schema_extra = {
            "example": {
                "analysis": {
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
                },
                "message": "Analysis completed successfully"
            }
        } 