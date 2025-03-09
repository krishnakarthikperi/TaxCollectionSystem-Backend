from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from auth.auth import getCurrentAdmin, getCurrentUser
from constants import USER_ROLE_ADMIN, USER_ROLE_COLLECOTR
import controller.taxrecord as controller
import controller.assignment as AssignmentController
from db import getSession
from objects.assignment import Assignment
from objects.taxrecord import TaxRecord, TaxRecordGETRequest, TaxRecordPOSTRequest

router = APIRouter()

@router.post("/recordcollection",response_model=TaxRecordPOSTRequest)
def insertTaxRecord(
        taxData : TaxRecordPOSTRequest,
        user=Depends(getCurrentUser),
        db: Session = Depends(getSession)    
):
    # Ensure user is a collector
    if USER_ROLE_COLLECOTR not in user.userRole.split(','):
        raise HTTPException(status_code=403, detail="Only collectors can record tax collection")

    # Ensure collector is assigned to this household
    assignment = AssignmentController.getAssignmentsByUsernameAndHouseNumber(
        username=user.username, 
        houseNumber=taxData.houseNumber,
        db=db
    ) 
    if not assignment:
        raise HTTPException(status_code=403, detail="You are not assigned to this household")
    
    taxRecord = TaxRecordPOSTRequest(collectorId=user.id, **taxData.model_dump())
    return controller.insertTaxRecord(taxRecord=taxRecord, db=db)

@router.get("/gettaxrecords", response_model=List[TaxRecordGETRequest], dependencies=[Depends(getCurrentUser)])
def getTaxRecords(db: Session = Depends(getSession)):
    return controller.getTaxRecords(db=db)

@router.get("/tax-records/{household_id}", response_model=List[TaxRecordGETRequest], dependencies=[Depends(getCurrentUser)])
def getTaxRecordByHouse(
        houseNumber: str,
        db: Session = Depends(getSession)
):
    return controller.getTaxRecordByHouse(houseNumber=houseNumber, db=db)

@router.put("/tax-records/{record_id}", response_model=TaxRecordPOSTRequest)
def updateTaxRecordById(
    recordId: int,
    updateData: TaxRecordPOSTRequest,
    db: Session = Depends(getSession),
    user=Depends(getCurrentUser)
):
    taxRecord = controller.getTaxRecordById(
        recordId=recordId,
        db=db
    )
    if not taxRecord:
        raise HTTPException(status_code=404, detail="Tax record not found")
    if user.userRole != USER_ROLE_ADMIN and user.username != taxRecord.collectorId:
        raise HTTPException(status_code=401, detail="Unauthorized edit")

    if updateData.amount is not None:
        taxRecord.amount = updateData.amount
    return controller.updateTaxRecordById(
        updateData = taxRecord,
        db=db
    )        