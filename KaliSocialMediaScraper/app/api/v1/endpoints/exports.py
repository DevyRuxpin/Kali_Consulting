"""
Export API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import os
import json
import csv
from io import StringIO
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import tempfile

from app.core.database import get_db
from app.repositories.investigation_repository import InvestigationRepository
from app.models.database import InvestigationReport as DBInvestigationReport, Investigation, SocialMediaData, DomainData, NetworkData
from app.models.schemas import InvestigationStatus

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
            db_report.id,
            investigation_id,
            db
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
            int(db_report.id),
            investigation_id,
            db
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
            db_report.id,
            investigation_id,
            db
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

@router.post("/report")
async def generate_report(
    data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a report based on the provided data"""
    try:
        investigation_id = data.get("investigation_id")
        report_type = data.get("report_type", "pdf")
        
        if not investigation_id:
            raise HTTPException(status_code=400, detail="investigation_id is required")
        
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Create report record
        report_data = {
            "investigation_id": investigation_id,
            "report_type": report_type,
            "title": f"Investigation Report - {investigation.title}",
            "description": f"{report_type.upper()} report for investigation {investigation_id}",
            "status": "pending",
            "created_by_id": 1  # TODO: Get from authentication
        }
        
        # Add to database
        db_report = DBInvestigationReport(**report_data)
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Start background report generation
        if report_type == "pdf":
            background_tasks.add_task(generate_pdf_report, report_id=db_report.id, investigation_id=investigation_id, db=db)
        elif report_type == "csv":
            background_tasks.add_task(generate_csv_report, report_id=db_report.id, investigation_id=investigation_id, db=db)
        elif report_type == "json":
            background_tasks.add_task(generate_json_report, report_id=db_report.id, investigation_id=investigation_id, db=db)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported report type: {report_type}")
        
        return {
            "report_id": db_report.id,
            "status": "pending",
            "message": f"{report_type.upper()} report generation started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating report: {e}")
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
                "completed_at": report.completed_at
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
            "completed_at": report.completed_at
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

@router.get("/reports/{report_id}/content")
async def get_report_content(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get report content for viewing"""
    try:
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        if report.status != "completed":
            raise HTTPException(status_code=400, detail="Report not ready for viewing")
        
        file_path = report.file_path
        if not file_path:
            raise HTTPException(status_code=404, detail="Report file not found")
        
        # Read file content based on report type
        try:
            if report.report_type == "pdf":
                # For PDF, return metadata since we can't easily display PDF content
                return {
                    "content_type": "pdf",
                    "file_path": file_path,
                    "file_size": report.file_size,
                    "message": "PDF content cannot be displayed directly. Please download the file."
                }
            elif report.report_type == "html":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "content_type": "html",
                    "content": content,
                    "file_size": report.file_size
                }
            elif report.report_type == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "content_type": "json",
                    "content": content,
                    "file_size": report.file_size
                }
            elif report.report_type == "csv":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "content_type": "csv",
                    "content": content,
                    "file_size": report.file_size
                }
            else:
                raise HTTPException(status_code=400, detail="Unsupported report type")
                
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Report file not found on disk")
        except Exception as e:
            logger.error(f"Error reading report file {report.file_path}: {e}")
            raise HTTPException(status_code=500, detail="Error reading report file")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report content {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_pdf_report(report_id: int, investigation_id: int, db: Session):
    """Generate comprehensive PDF report with real investigation data"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # Get investigation data
        investigation = db.query(Investigation).filter(
            Investigation.id == investigation_id
        ).first()
        
        if not investigation:
            raise Exception("Investigation not found")
        
        # Get related data
        social_media_data = db.query(SocialMediaData).filter(
            SocialMediaData.investigation_id == investigation_id
        ).all()
        
        domain_data = db.query(DomainData).filter(
            DomainData.investigation_id == investigation_id
        ).first()
        
        network_data = db.query(NetworkData).filter(
            NetworkData.investigation_id == investigation_id
        ).first()
        
        # Create PDF report
        report_file = f"/tmp/report_{report_id}.pdf"
        doc = SimpleDocTemplate(report_file, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12
        )
        normal_style = styles['Normal']
        
        # Title
        story.append(Paragraph("OSINT Investigation Report", title_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(f"""
        This report presents the findings of an OSINT investigation targeting {investigation.target_value} 
        ({investigation.target_type}). The investigation was initiated on {investigation.created_at.strftime('%Y-%m-%d %H:%M:%S')} 
        and completed with a status of {investigation.status}.
        """, normal_style))
        story.append(Spacer(1, 12))
        
        # Investigation Details
        story.append(Paragraph("Investigation Details", heading_style))
        investigation_table_data = [
            ['Field', 'Value'],
            ['Target Type', investigation.target_type],
            ['Target Value', investigation.target_value],
            ['Status', investigation.status],
            ['Priority', investigation.priority],
            ['Analysis Depth', investigation.analysis_depth],
            ['Progress', f"{investigation.progress}%"],
            ['Created', investigation.created_at.strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        if investigation.completed_at:
            investigation_table_data.append(['Completed', investigation.completed_at.strftime('%Y-%m-%d %H:%M:%S')])
        
        investigation_table = Table(investigation_table_data)
        investigation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(investigation_table)
        story.append(Spacer(1, 20))
        
        # Social Media Findings
        if social_media_data:
            story.append(Paragraph("Social Media Analysis", heading_style))
            story.append(Paragraph(f"Found {len(social_media_data)} social media profiles across different platforms.", normal_style))
            
            for profile in social_media_data:
                story.append(Paragraph(f"Platform: {profile.platform.name}", normal_style))
                story.append(Paragraph(f"Username: {profile.username}", normal_style))
                story.append(Paragraph(f"Display Name: {profile.display_name or 'N/A'}", normal_style))
                story.append(Paragraph(f"Followers: {profile.followers_count}", normal_style))
                story.append(Paragraph(f"Threat Score: {profile.threat_score:.2f}", normal_style))
                story.append(Spacer(1, 6))
        
        # Domain Intelligence
        if domain_data:
            story.append(Paragraph("Domain Intelligence", heading_style))
            story.append(Paragraph(f"Domain: {domain_data.domain}", normal_style))
            story.append(Paragraph(f"IP Addresses: {', '.join(domain_data.ip_addresses) if domain_data.ip_addresses else 'N/A'}", normal_style))
            story.append(Paragraph(f"Subdomains Found: {len(domain_data.subdomains) if domain_data.subdomains else 0}", normal_style))
            story.append(Paragraph(f"Threat Score: {domain_data.threat_score:.2f}", normal_style))
            story.append(Spacer(1, 12))
        
        # Network Analysis
        if network_data:
            story.append(Paragraph("Network Analysis", heading_style))
            story.append(Paragraph(f"Nodes Analyzed: {len(network_data.nodes) if network_data.nodes else 0}", normal_style))
            story.append(Paragraph(f"Connections Found: {len(network_data.edges) if network_data.edges else 0}", normal_style))
            story.append(Paragraph(f"Communities Detected: {len(network_data.communities) if network_data.communities else 0}", normal_style))
            story.append(Spacer(1, 12))
        
        # Recommendations
        story.append(Paragraph("Recommendations", heading_style))
        recommendations = [
            "Continue monitoring the target for new activity",
            "Expand investigation to related entities if necessary",
            "Document all findings for future reference",
            "Consider automated monitoring for ongoing surveillance"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", normal_style))
        
        # Build PDF
        doc.build(story)
        
        # Update report status
        if report:
            report.status = "completed"
            report.file_path = report_file
            report.file_size = os.path.getsize(report_file)
            report.completed_at = datetime.utcnow()
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
    """Generate comprehensive CSV report with real investigation data"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # Get investigation data
        investigation = db.query(Investigation).filter(
            Investigation.id == investigation_id
        ).first()
        
        if not investigation:
            raise Exception("Investigation not found")
        
        # Get related data
        social_media_data = db.query(SocialMediaData).filter(
            SocialMediaData.investigation_id == investigation_id
        ).all()
        
        domain_data = db.query(DomainData).filter(
            DomainData.investigation_id == investigation_id
        ).first()
        
        # Create CSV report
        report_file = f"/tmp/report_{report_id}.csv"
        
        with open(report_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Investigation Overview
            writer.writerow(['OSINT Investigation Report'])
            writer.writerow([])
            writer.writerow(['Investigation Details'])
            writer.writerow(['Field', 'Value'])
            writer.writerow(['Target Type', investigation.target_type])
            writer.writerow(['Target Value', investigation.target_value])
            writer.writerow(['Status', investigation.status])
            writer.writerow(['Priority', investigation.priority])
            writer.writerow(['Analysis Depth', investigation.analysis_depth])
            writer.writerow(['Progress', f"{investigation.progress}%"])
            writer.writerow(['Created', investigation.created_at.strftime('%Y-%m-%d %H:%M:%S')])
            if investigation.completed_at:
                writer.writerow(['Completed', investigation.completed_at.strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Social Media Data
            if social_media_data:
                writer.writerow(['Social Media Analysis'])
                writer.writerow(['Platform', 'Username', 'Display Name', 'Followers', 'Following', 'Threat Score', 'Sentiment Score'])
                for profile in social_media_data:
                    writer.writerow([
                        profile.platform.name,
                        profile.username,
                        profile.display_name or 'N/A',
                        profile.followers_count,
                        profile.following_count,
                        f"{profile.threat_score:.2f}",
                        f"{profile.sentiment_score:.2f}"
                    ])
                writer.writerow([])
            
            # Domain Data
            if domain_data:
                writer.writerow(['Domain Intelligence'])
                writer.writerow(['Domain', domain_data.domain])
                writer.writerow(['IP Addresses', ', '.join(domain_data.ip_addresses) if domain_data.ip_addresses else 'N/A'])
                writer.writerow(['Subdomains', ', '.join(domain_data.subdomains) if domain_data.subdomains else 'N/A'])
                writer.writerow(['Threat Score', f"{domain_data.threat_score:.2f}"])
                writer.writerow(['Technologies', ', '.join(domain_data.technologies) if domain_data.technologies else 'N/A'])
                writer.writerow([])
        
        # Update report status
        if report:
            report.status = "completed"
            report.file_path = report_file
            report.file_size = os.path.getsize(report_file)
            report.completed_at = datetime.utcnow()
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
    """Generate comprehensive JSON report with real investigation data"""
    try:
        # Update status to processing
        report = db.query(DBInvestigationReport).filter(
            DBInvestigationReport.id == report_id
        ).first()
        
        if report:
            report.status = "processing"
            db.commit()
        
        # Get investigation data
        investigation = db.query(Investigation).filter(
            Investigation.id == investigation_id
        ).first()
        
        if not investigation:
            raise Exception("Investigation not found")
        
        # Get related data
        social_media_data = db.query(SocialMediaData).filter(
            SocialMediaData.investigation_id == investigation_id
        ).all()
        
        domain_data = db.query(DomainData).filter(
            DomainData.investigation_id == investigation_id
        ).first()
        
        network_data = db.query(NetworkData).filter(
            NetworkData.investigation_id == investigation_id
        ).first()
        
        # Create comprehensive JSON report
        report_data = {
            "report_id": report_id,
            "investigation_id": investigation_id,
            "generated_at": datetime.utcnow().isoformat(),
            "investigation": {
                "id": investigation.id,
                "title": investigation.title,
                "description": investigation.description,
                "target_type": investigation.target_type,
                "target_value": investigation.target_value,
                "status": investigation.status,
                "priority": investigation.priority,
                "analysis_depth": investigation.analysis_depth,
                "progress": investigation.progress,
                "created_at": investigation.created_at.isoformat(),
                "completed_at": investigation.completed_at.isoformat() if investigation.completed_at else None,
                "analysis_options": investigation.analysis_options
            },
            "social_media_analysis": {
                "total_profiles": len(social_media_data),
                "profiles": [
                    {
                        "platform": profile.platform.name,
                        "username": profile.username,
                        "display_name": profile.display_name,
                        "bio": profile.bio,
                        "followers_count": profile.followers_count,
                        "following_count": profile.following_count,
                        "posts_count": profile.posts_count,
                        "profile_url": profile.profile_url,
                        "is_verified": profile.is_verified,
                        "is_private": profile.is_private,
                        "threat_score": profile.threat_score,
                        "threat_indicators": profile.threat_indicators,
                        "sentiment_score": profile.sentiment_score,
                        "collected_at": profile.collected_at.isoformat()
                    }
                    for profile in social_media_data
                ]
            },
            "domain_intelligence": {
                "domain": domain_data.domain if domain_data else None,
                "ip_addresses": domain_data.ip_addresses if domain_data else [],
                "subdomains": domain_data.subdomains if domain_data else [],
                "dns_records": domain_data.dns_records if domain_data else {},
                "whois_data": domain_data.whois_data if domain_data else {},
                "ssl_certificate": domain_data.ssl_certificate if domain_data else {},
                "technologies": domain_data.technologies if domain_data else [],
                "threat_indicators": domain_data.threat_indicators if domain_data else [],
                "threat_score": domain_data.threat_score if domain_data else 0.0,
                "collected_at": domain_data.collected_at.isoformat() if domain_data else None
            },
            "network_analysis": {
                "nodes": network_data.nodes if network_data else [],
                "edges": network_data.edges if network_data else [],
                "communities": network_data.communities if network_data else [],
                "centrality_scores": network_data.centrality_scores if network_data else {},
                "threat_hotspots": network_data.threat_hotspots if network_data else [],
                "created_at": network_data.created_at.isoformat() if network_data else None
            },
            "summary": {
                "total_findings": len(social_media_data) + (1 if domain_data else 0) + (1 if network_data else 0),
                "average_threat_score": sum([p.threat_score for p in social_media_data]) / len(social_media_data) if social_media_data else 0.0,
                "high_risk_profiles": len([p for p in social_media_data if p.threat_score > 0.7]),
                "recommendations": [
                    "Continue monitoring the target for new activity",
                    "Expand investigation to related entities if necessary",
                    "Document all findings for future reference",
                    "Consider automated monitoring for ongoing surveillance"
                ]
            }
        }
        
        # Write JSON report
        report_file = f"/tmp/report_{report_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Update report status
        if report:
            report.status = "completed"
            report.file_path = report_file
            report.file_size = os.path.getsize(report_file)
            report.completed_at = datetime.utcnow()
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