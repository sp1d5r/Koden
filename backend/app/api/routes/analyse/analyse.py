from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.analyzer import analyze_repository
from app.core.logging import logger
from app.models.api.analysis import AnalysisResponse
from typing import Optional, Set

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def analyze_repo(
    zip_file: UploadFile = File(..., description="Zip file containing the repository to analyze"),
    ignore_patterns: Optional[Set[str]] = Form(None, description="Patterns of files to ignore during analysis")
) -> AnalysisResponse:
    """
    Analyze a repository from a zip file.
    
    Args:
        zip_file: The zip file containing the repository
        ignore_patterns: Optional set of patterns to ignore during analysis
        
    Returns:
        AnalysisResponse containing the repository analysis results
    """
    try:
        logger.info(f"Received analysis request for file: {zip_file.filename}")
        
        # Validate file
        if not zip_file.filename:
            logger.error("No file provided in request")
            raise HTTPException(status_code=400, detail="No file provided")
            
        if not zip_file.filename.endswith('.zip'):
            logger.error(f"Invalid file type: {zip_file.filename}")
            raise HTTPException(status_code=400, detail="File must be a zip file")
            
        # Log content type for debugging
        logger.debug(f"File content type: {zip_file.content_type}")
        
        # Analyze repository
        analysis = await analyze_repository(zip_file, ignore_patterns)
        
        logger.info("Analysis completed successfully")
        return AnalysisResponse(
            analysis=analysis,
            message="Analysis completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing repository: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing repository: {str(e)}"
        ) 