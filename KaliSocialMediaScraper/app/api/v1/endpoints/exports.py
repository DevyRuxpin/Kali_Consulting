"""
Export API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.core.database import get_db
from app.repositories.investigation_repository import InvestigationRepository
from app.models.database import InvestigationReport as DBInvestigationReport

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/investigation/{investigation_id}/pdf")
async def export_investigation_pdf(
    investigation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Export investigation as PDF report"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Create report record
        report_data = {
            "investigation_id": investigation_id,
            "report_type": "pdf",
            "title": f"Investigation Report - {investigation.title}",
            "description": f"PDF report for investigation {investigation_id}",
            "status": "pending",
            "created_by_id": 1  # TODO: Get from authentication
        }
        
        # Add to database
        db_report = DBInvestigationReport(**report_data)
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Start background PDF generation
        background_tasks.add_task(
            generate_pdf_report,
            report_id=db_report.id,
            investigation_id=investigation_id,
            db=db
        )
        
        return {
            "report_id": db_report.id,
            "status": "pending",
            "message": "PDF report generation started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating PDF export for investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/investigation/{investigation_id}/csv")
async def export_investigation_csv(
    investigation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Export investigation as CSV report"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Create report record
        report_data = {
            "investigation_id": investigation_id,
            "report_type": "csv",
            "title": f"Investigation Data - {investigation.title}",
            "description": f"CSV export for investigation {investigation_id}",
            "status": "pending",
            "created_by_id": 1  # TODO: Get from authentication
        }
        
        # Add to database
        db_report = DBInvestigationReport(**report_data)
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Start background CSV generation
        background_tasks.add_task(
            generate_csv_report,
            report_id=db_report.id,
            investigation_id=investigation_id,
            db=db
        )
        
        return {
            "report_id": db_report.id,
            "status": "pending",
            "message": "CSV export generation started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating CSV export for investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/investigation/{investigation_id}/json")
async def export_investigation_json(
    investigation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Export investigation as JSON report"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Create report record
        report_data = {
            "investigation_id": investigation_id,
            "report_type": "json",
            "title": f"Investigation Data - {investigation.title}",
            "description": f"JSON export for investigation {investigation_id}",
            "status": "pending",
            "created_by_id": 1  # TODO: Get from authentication
        }
        
        # Add to database
        db_report = DBInvestigationReport(**report_data)
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Start background JSON generation
        background_tasks.add_task(
            generate_json_report,
            report_id=db_report.id,
            investigation_id=investigation_id,
            db=db
        )
        
        return {
            "report_id": db_report.id,
            "status": "pending",
            "message": "JSON export generation started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating JSON export for investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports", response_model=List[Dict[str, Any]])
async def list_reports(
    investigation_id: Optional[int] = None,
    report_type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all reports with optional filtering"""
    try:
        query = db.query(DBInvestigationReport)
        
        if investigation_id:
            query = query.filter(DBInvestigationReport.investigation_id == investigation_id)
        if report_type:
            query = query.filter(DBInvestigationReport.report_type == report_type)
        if status:
            query = query.filter(DBInvestigationReport.status == status)
        
        reports = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": report.id,
                "investigation_id": report.investigation_id,
                "report_type": report.report_type,
                "title": report.title,
                "description": report.description,
                "status": report.status,
                "file_path": report.file_path,
                "file_size": report.file_size,
                "created_at": report.created_at,
                "updated_at": report.updated_at
            }
            for report in reports
        ]
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/{report_id}", response_model=Dict[str, Any])
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get report by ID"""
    try:
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "id": report.id,
            "investigation_id": report.investigation_id,
            "report_type": report.report_type,
            "title": report.title,
            "description": report.description,
            "status": report.status,
            "file_path": report.file_path,
            "file_size": report.file_size,
            "created_at": report.created_at,
            "updated_at": report.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Download report file"""
    try:
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        if report.status != "completed":
            raise HTTPException(status_code=400, detail="Report not ready for download")
        
        if not report.file_path:
            raise HTTPException(status_code=404, detail="Report file not found")
        
        # TODO: Implement file download logic
        return {"message": "Download functionality to be implemented"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_pdf_report(report_id: int, investigation_id: int, db: Session):
    """Generate PDF report in background"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # TODO: Implement PDF generation logic
        # For now, just mark as completed
        if report:
            report.status = "completed"
            report.file_path = f"/reports/{report_id}.pdf"
            report.file_size = 1024  # Placeholder
            db.commit()
        
        logger.info(f"PDF report {report_id} generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating PDF report {report_id}: {e}")
        # Update status to failed
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        if report:
            report.status = "failed"
            db.commit()

async def generate_csv_report(report_id: int, investigation_id: int, db: Session):
    """Generate CSV report in background"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # TODO: Implement CSV generation logic
        # For now, just mark as completed
        if report:
            report.status = "completed"
            report.file_path = f"/reports/{report_id}.csv"
            report.file_size = 512  # Placeholder
            db.commit()
        
        logger.info(f"CSV report {report_id} generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating CSV report {report_id}: {e}")
        # Update status to failed
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        if report:
            report.status = "failed"
            db.commit()

async def generate_json_report(report_id: int, investigation_id: int, db: Session):
    """Generate JSON report in background"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # TODO: Implement JSON generation logic
        # For now, just mark as completed
        if report:
            report.status = "completed"
            report.file_path = f"/reports/{report_id}.json"
            report.file_size = 256  # Placeholder
            db.commit()
        
        logger.info(f"JSON report {report_id} generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating JSON report {report_id}: {e}")
        # Update status to failed
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        if report:
            report.status = "failed"
            db.commit() 