from sqlmodel import Session, select
from objects.taxrecord import TaxRecordPOSTRequest, TaxRecord, TaxRecordGETRequest
from objects.assignment import Assignment
from db import SessionDep, getSession
from auth.auth import getCurrentAdmin
from fastapi import Depends, HTTPException

def insertTaxRecord(
        taxRecord : TaxRecordPOSTRequest,
        db: Session = Depends(getSession)
):
    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord

def getTaxRecords(db: Session = Depends(getSession)):
    return db.exec(select(TaxRecord)).all()

def getTaxRecordByHouse(
        houseNumber: str, 
        db: Session = Depends(getSession)
):
    return db.exec(select(TaxRecord).where(TaxRecord.houseId == houseNumber)).all()

# @router.put("/tax-records/{record_id}", response_model=TaxRecordPOSTRequest)
def updateTaxRecordById(
    taxRecord: TaxRecordPOSTRequest,
    db: Session = Depends(getSession),
    admin=Depends(getCurrentAdmin),
):
    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord

def getTaxRecordById(
        recordId: int,
        db: Session = Depends(getSession)
):
    return db.get(TaxRecord, recordId)