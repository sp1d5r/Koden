import zipfile
import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.logging import logger
from typing import List, Set, Dict
from app.models.domain.analysis import (
    RepositoryAnalysis,
    AnalysisInsights,
    CodeQualityMetrics,
    CouplingMetrics,
    CircularDependency
)
from .dependency_parser import analyze_dependencies

# Default ignore patterns
DEFAULT_IGNORE_PATTERNS = {
    '.venv',
    '__pycache__',
    '.git',
    '.pytest_cache',
    '.mypy_cache',
    '.coverage',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.Python',
    'env',
    'venv',
    'ENV',
    'env.bak',
    'venv.bak',
    '.DS_Store'
}

def should_ignore(path: str, ignore_patterns: Set[str]) -> bool:
    """Check if a path should be ignored based on patterns."""
    path_parts = path.split(os.sep)
    return any(
        pattern in path_parts or 
        any(part.endswith(pattern.lstrip('*')) for part in path_parts if pattern.startswith('*'))
        for pattern in ignore_patterns
    )

def calculate_quality_metrics(
    total_files: int,
    dependency_graph: Dict[str, List[str]],
    circular_deps: List[List[str]],
    orphaned_files: List[str],
    coupling_scores: Dict[str, Dict]
) -> CodeQualityMetrics:
    """Calculate overall code quality metrics."""
    total_dependencies = sum(len(deps) for deps in dependency_graph.values())
    total_coupling = sum(score['total'] for score in coupling_scores.values())
    
    return CodeQualityMetrics(
        total_files=total_files,
        total_dependencies=total_dependencies,
        circular_dependencies_count=len(circular_deps),
        orphaned_files_count=len(orphaned_files),
        average_coupling=total_coupling / total_files if total_files > 0 else 0.0
    )

async def analyze_repository(zip_file: UploadFile, ignore_patterns: Set[str] = None) -> RepositoryAnalysis:
    """
    Analyze a repository from a zip file.
    
    Args:
        zip_file: The zip file containing the repository
        ignore_patterns: Optional set of patterns to ignore during analysis
        
    Returns:
        RepositoryAnalysis containing the analysis results
    """
    if not zip_file.filename:
        logger.error("No file provided in request")
        raise HTTPException(status_code=400, detail="No file provided")

    # Use default ignore patterns if none provided
    if ignore_patterns is None:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS

    tmp_dir = Path("/tmp/koden-upload")
    try:
        logger.info(f"Processing zip file: {zip_file.filename}")
        
        # Clean up any existing temporary directory
        shutil.rmtree(tmp_dir, ignore_errors=True)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created temporary directory: {tmp_dir}")

        # Save the uploaded file
        zip_path = tmp_dir / zip_file.filename
        content = await zip_file.read()
        if not content:
            logger.error("Empty file provided")
            raise HTTPException(status_code=400, detail="Empty file provided")
            
        with open(zip_path, "wb") as f:
            f.write(content)
        logger.debug(f"Saved zip file to: {zip_path}")

        # Verify it's a valid zip file
        if not zipfile.is_zipfile(zip_path):
            logger.error(f"Invalid zip file: {zip_file.filename}")
            raise HTTPException(status_code=400, detail="Invalid zip file")

        # Extract the contents
        extract_path = tmp_dir / "unzipped"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        logger.debug(f"Extracted zip file to: {extract_path}")

        # Get file structure
        file_structure = []
        python_files = []
        for root, _, files in os.walk(extract_path):
            for name in files:
                rel_path = os.path.relpath(os.path.join(root, name), extract_path)
                if not should_ignore(rel_path, ignore_patterns):
                    file_structure.append(rel_path)
                    if rel_path.endswith('.py'):
                        python_files.append(rel_path)

        # Analyze dependencies
        logger.info("Analyzing Python dependencies...")
        analysis = analyze_dependencies(extract_path, python_files)
        logger.info(f"Found {len(analysis['dependency_graph'])} Python files with dependencies")
        
        # Convert raw analysis into Pydantic models
        coupling_scores = {
            file: CouplingMetrics(**scores)
            for file, scores in analysis['insights']['coupling_scores'].items()
        }
        
        circular_deps = [
            CircularDependency(
                files=cycle,
                severity="high" if len(cycle) > 2 else "medium",
                suggested_fixes=["Consider extracting shared functionality to a new module"]
            )
            for cycle in analysis['insights']['circular_dependencies']
        ]
        
        quality_metrics = calculate_quality_metrics(
            total_files=len(python_files),
            dependency_graph=analysis['dependency_graph'],
            circular_deps=analysis['insights']['circular_dependencies'],
            orphaned_files=analysis['insights']['orphaned_files'],
            coupling_scores=analysis['insights']['coupling_scores']
        )
        
        insights = AnalysisInsights(
            circular_dependencies=circular_deps,
            high_coupling_hotspots=coupling_scores,
            orphaned_files=analysis['insights']['orphaned_files'],
            coupling_scores=coupling_scores,
            quality_metrics=quality_metrics
        )
        
        # Log insights
        if circular_deps:
            logger.warning(f"Found {len(circular_deps)} circular dependencies")
        if insights.orphaned_files:
            logger.info(f"Found {len(insights.orphaned_files)} orphaned files")
        logger.info("Top coupling hotspots:")
        for file, scores in insights.high_coupling_hotspots.items():
            logger.info(f"  {file}: {scores.total} total edges ({scores.inbound} inbound, {scores.outbound} outbound)")

        return RepositoryAnalysis(
            files=file_structure,
            dependencies=analysis['dependency_graph'],
            insights=insights
        )

    except zipfile.BadZipFile:
        logger.error(f"Invalid zip file format: {zip_file.filename}")
        raise HTTPException(status_code=400, detail="Invalid zip file format")
    except Exception as e:
        logger.error(f"Error processing zip file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing zip file: {str(e)}")
    finally:
        # Cleanup
        shutil.rmtree(tmp_dir, ignore_errors=True)
        logger.debug("Cleaned up temporary directory") 