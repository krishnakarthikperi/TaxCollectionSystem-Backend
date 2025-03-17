from typing import List
from sqlmodel import Session, select
from objects.taxrecord import TaxRecordPOSTRequest, TaxRecord, TaxRecordPUTRequest
from db import getSession
from auth.auth import getCurrentAdmin
from fastapi import Depends

def insertTaxRecords(
        taxRecords : List[TaxRecordPOSTRequest],
        db: Session = Depends(getSession)
):
    taxRecords = [TaxRecord(**taxRecord.model_dump()) for taxRecord in taxRecords]
    db.add_all(taxRecords)
    db.flush()
    [db.refresh(taxRecord) for taxRecord in taxRecords]
    db.commit()
    return taxRecords

def getTaxRecords(db: Session = Depends(getSession)):
    return db.exec(select(TaxRecord)).all()

def getTaxRecordByHouse(
        houseNumber: str, 
        db: Session = Depends(getSession)
):
    return db.exec(select(TaxRecord).where(TaxRecord.houseId == houseNumber)).all()

def updateTaxRecordById(
    taxRecord: TaxRecord,
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