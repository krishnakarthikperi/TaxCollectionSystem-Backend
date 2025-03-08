from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from auth.auth import getCurrentAdmin, getCurrentUser
from constants import USER_ROLE_COLLECOTR
import controller.taxrecord as controller
from objects.assignment import Assignment
from objects.taxrecord import TaxRecord, TaxRecordGETRequest, TaxRecordPOSTRequest
from db import SessionDep

router = APIRouter()

@router.post("/recordcollection",response_model=TaxRecordPOSTRequest)
def insertTaxRecord(
        taxData : TaxRecordPOSTRequest,
        db: SessionDep,
        user=Depends(getCurrentUser)    
):
    # Ensure user is a collector
    if USER_ROLE_COLLECOTR not in user.userRole.split(','):
        raise HTTPException(status_code=403, detail="Only collectors can record tax collection")

    # Ensure collector is assigned to this household
    assignment = db.exec(
        select(Assignment).where(
            (Assignment.username == user.username) & (Assignment.houseId == taxData.houseNumber)
        )
    ).first()

    if not assignment:
        raise HTTPException(status_code=403, detail="You are not assigned to this household")
    
    taxRecord = TaxRecordPOSTRequest(collectorId=user.id, **taxData.model_dump())
    return controller.insertTaxRecord(taxRecord=taxRecord,db=db)

@router.get("/gettaxrecords", response_model=List[TaxRecordGETRequest])
def getTaxRecords(db: SessionDep):
    return controller.getTaxRecords(db=db)

@router.get("/tax-records/{household_id}", response_model=List[TaxRecordGETRequest])
def getTaxRecordByHouse(
        houseNumber: str, 
        db: SessionDep
):
    return controller.getTaxRecordByHouse(houseNumber=houseNumber, db=db)

@router.put("/tax-records/{record_id}", response_model=TaxRecordPOSTRequest)
def updateTaxRecordById(
    recordId: int,
    updateData: TaxRecordPOSTRequest,
    db: SessionDep,
    admin=Depends(getCurrentAdmin),
):
    taxRecord = controller.getTaxRecordById(
        recordId=recordId,
        db=db
    )
    if not taxRecord:
        raise HTTPException(status_code=404, detail="Tax record not found")

    if updateData.amount is not None:
        taxRecord.amount = updateData.amount
    return controller.updateTaxRecordById(
        updateData = taxRecord,
        db=db
    )
        