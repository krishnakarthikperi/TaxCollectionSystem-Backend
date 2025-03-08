from objects.taxrecord import TaxRecordPOSTRequest, TaxRecord, TaxRecordGETRequest
from objects.assignment import Assignment
from db import SessionDep
from auth.auth import getCurrentUser, getCurrentAdmin
from fastapi import Depends, HTTPException

def insertTaxRecord(
        taxRecord : TaxRecordPOSTRequest,
        db: SessionDep
):
    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord

def getTaxRecords(db: SessionDep):
    return db.exec(select(TaxRecord)).all()

def getTaxRecordByHouse(
        houseNumber: str, 
        db: SessionDep
):
    return db.exec(select(TaxRecord).where(TaxRecord.houseId == houseNumber)).all()

# @router.put("/tax-records/{record_id}", response_model=TaxRecordPOSTRequest)
def updateTaxRecordById(
    taxRecord: TaxRecordPOSTRequest,
    db: SessionDep,
    admin=Depends(getCurrentAdmin),
):
    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord

def getTaxRecordById(
        recordId: int,
        db: SessionDep
):
    return db.get(TaxRecord, recordId)