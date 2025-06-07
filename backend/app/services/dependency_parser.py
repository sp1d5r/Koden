import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from app.core.logging import logger
from app.models.domain.analysis import ComplexityMetrics

class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor for calculating code complexity metrics."""
    def __init__(self):
        self.loc = 0
        self.function_count = 0
        self.class_count = 0
        self.max_nesting_depth = 0
        self.current_nesting = 0
        self.cyclomatic_complexity = 0
        self.comment_lines = 0
        self.code_lines = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.cyclomatic_complexity += 1  # Base complexity for function
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        
        # Visit all nodes in the function
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler)):
                self.cyclomatic_complexity += 1
        
        self.current_nesting -= 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.class_count += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.current_nesting -= 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

def calculate_complexity(content: str) -> ComplexityMetrics:
    """Calculate complexity metrics for a Python file."""
    try:
        tree = ast.parse(content)
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        
        # Calculate LOC and comment ratio
        lines = content.splitlines()
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        return ComplexityMetrics(
            loc=len(lines),
            function_count=visitor.function_count,
            class_count=visitor.class_count,
            max_nesting_depth=visitor.max_nesting_depth,
            cyclomatic_complexity=visitor.cyclomatic_complexity / max(visitor.function_count, 1),
            comment_ratio=comment_lines / max(code_lines, 1)
        )
    except Exception as e:
        logger.error(f"Error calculating complexity: {str(e)}", exc_info=True)
        return ComplexityMetrics(
            loc=0,
            function_count=0,
            class_count=0,
            max_nesting_depth=0,
            cyclomatic_complexity=0.0,
            comment_ratio=0.0
        )

def calculate_risk_score(complexity: ComplexityMetrics, coupling: Dict) -> float:
    """Calculate a risk score based on complexity and coupling metrics."""
    # Normalize metrics to 0-1 range
    complexity_score = (
        (complexity.cyclomatic_complexity / 10) +  # Normalize to 0-1, assuming 10 is high
        (complexity.max_nesting_depth / 5) +       # Normalize to 0-1, assuming 5 is high
        (complexity.function_count / 20)           # Normalize to 0-1, assuming 20 is high
    ) / 3

    coupling_score = (
        (coupling['total'] / 10) +                # Normalize to 0-1, assuming 10 is high
        (coupling['depth'] / 5)                   # Normalize to 0-1, assuming 5 is high
    ) / 2

    # Combine scores with weights
    return (complexity_score * 0.6 + coupling_score * 0.4) * 100  # Scale to 0-100

def analyze_dependencies(base_path: Path, python_files: List[str]) -> Dict:
    """
    Parse Python files and analyze dependencies to find architectural insights.
    
    Args:
        base_path: Base path where the files are located
        python_files: List of Python file paths relative to base_path
        
    Returns:
        Dictionary containing dependency graph and derived signals
    """
    dependency_graph = {}
    inbound_edges = defaultdict(set)
    complexity_metrics = {}
    
    # First pass: build the dependency graph and calculate complexity
    for file_path in python_files:
        try:
            full_path = base_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate complexity metrics
            complexity_metrics[file_path] = calculate_complexity(content)
            
            # Parse the file
            tree = ast.parse(content)
            
            # Find all imports
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
            
            # Convert imports to file paths
            dependencies = []
            for imp in imports:
                # Try to find the corresponding Python file
                for py_file in python_files:
                    if py_file.endswith(f"{imp.replace('.', '/')}.py"):
                        dependencies.append(py_file)
                        inbound_edges[py_file].add(file_path)
                    elif py_file.endswith(f"{imp.replace('.', '/')}/__init__.py"):
                        dependencies.append(py_file)
                        inbound_edges[py_file].add(file_path)
            
            if dependencies:
                dependency_graph[file_path] = sorted(dependencies)
                
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}", exc_info=True)
            continue

    # Find circular dependencies
    circular_deps = find_circular_dependencies(dependency_graph)
    
    # Calculate coupling metrics for each file
    coupling_scores = {}
    risk_scores = {}
    for file_path in python_files:
        outbound = len(dependency_graph.get(file_path, []))
        inbound = len(inbound_edges[file_path])
        depth = calculate_dependency_depth(dependency_graph, file_path)
        
        coupling = {
            "outbound": outbound,
            "inbound": inbound,
            "total": outbound + inbound,
            "depth": depth,
            "fan_in": inbound,
            "fan_out": outbound
        }
        coupling_scores[file_path] = coupling
        
        # Calculate risk score if we have complexity metrics
        if file_path in complexity_metrics:
            risk_scores[file_path] = calculate_risk_score(
                complexity_metrics[file_path],
                coupling
            )
    
    # Find high risk files (complexity + coupling)
    high_risk_files = {
        file: {
            "complexity": complexity_metrics[file],
            "coupling": coupling_scores[file],
            "risk_score": risk_scores[file]
        }
        for file, score in risk_scores.items()
        if score > 70  # Threshold for high risk
    }
    
    # Find orphaned files
    orphaned_files = []
    for file_path in python_files:
        if (file_path not in dependency_graph and 
            not inbound_edges[file_path] and 
            file_path.endswith('.py')):
            orphaned_files.append(file_path)
    
    # Sort coupling scores to find hotspots
    high_coupling = sorted(
        coupling_scores.items(),
        key=lambda x: x[1]["total"],
        reverse=True
    )[:5]  # Top 5 most coupled files
    
    # Sort complexity scores to find complex files
    high_complexity = sorted(
        complexity_metrics.items(),
        key=lambda x: x[1].cyclomatic_complexity,
        reverse=True
    )[:5]  # Top 5 most complex files
    
    return {
        "dependency_graph": dependency_graph,
        "insights": {
            "circular_dependencies": circular_deps,
            "high_coupling_hotspots": {
                file: scores for file, scores in high_coupling
            },
            "high_complexity_files": {
                file: metrics for file, metrics in high_complexity
            },
            "high_risk_files": high_risk_files,
            "orphaned_files": orphaned_files,
            "coupling_scores": coupling_scores
        }
    }

def calculate_dependency_depth(graph: Dict[str, List[str]], start_file: str) -> int:
    """Calculate the maximum depth of dependencies for a file."""
    def dfs(node: str, visited: Set[str], current_depth: int) -> int:
        if node in visited:
            return current_depth
        visited.add(node)
        max_depth = current_depth
        for neighbor in graph.get(node, []):
            depth = dfs(neighbor, visited, current_depth + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    
    return dfs(start_file, set(), 0)

def find_circular_dependencies(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Find circular dependencies in the graph using DFS."""
    def dfs(node: str, visited: Set[str], path: List[str], circles: List[List[str]]):
        if node in path:
            circle_start = path.index(node)
            circles.append(path[circle_start:] + [node])
            return
        if node in visited:
            return
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            dfs(neighbor, visited, path, circles)
        
        path.pop()
    
    circles = []
    visited = set()
    for node in graph:
        if node not in visited:
            dfs(node, visited, [], circles)
    return circles 