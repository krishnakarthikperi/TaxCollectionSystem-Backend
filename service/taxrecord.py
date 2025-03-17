from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.taxrecord as controller
import controller.assignment as AssignmentController
from db import getSession
from objects.taxrecord import TaxRecordGETRequest, TaxRecordPOSTRequest, TaxRecordPOSTResponse, TaxRecordPUTRequest, TaxRecordPUTResponse
import service.constants as constants

router = APIRouter()

@router.post("/recordcollections",response_model=List[TaxRecordPOSTResponse])
def insertTaxRecords(
        taxData : List[TaxRecordPOSTRequest],
        user=Depends(getCurrentUser),
        db: Session = Depends(getSession)    
):
    # Ensure user is a collector
    if constants.USER_ROLE_COLLECTOR not in user.userRole.split(','):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, 
            detail = constants.ONLY_COLLECTORS_RECORD_TAX_COLLECTION
        )

    # Ensure collector is assigned to this household
    assignments = AssignmentController.getAssignmentsByUsernameAndHouseNumbers(
        username=user.username, 
        houseNumbers=[taxDatum.houseId for taxDatum in taxData],
        db=db
    ) 

    if constants.USER_ROLE_ADMIN not in user.userRole.split(','):
        for taxDatum in taxData:
            if taxDatum.houseId not in [assignment.houseId for assignment in assignments]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail = constants.INCORRECT_HOUSE_MAPPING
                )    
    return controller.insertTaxRecords(taxRecords=taxData, db=db)

@router.get("/gettaxrecords", response_model=List[TaxRecordGETRequest], dependencies=[Depends(getCurrentUser)])
def getTaxRecords(db: Session = Depends(getSession)):
    return controller.getTaxRecords(db=db)

@router.get("/tax-records/{houseNumber}", response_model=List[TaxRecordGETRequest], dependencies=[Depends(getCurrentUser)])
def getTaxRecordByHouse(
        houseNumber: str,
        db: Session = Depends(getSession)
):
    return controller.getTaxRecordByHouse(houseNumber=houseNumber, db=db)

@router.put("/tax-record/{recordId}", response_model=TaxRecordPUTResponse)
def updateTaxRecordById(
    recordId: int,
    updateData: TaxRecordPUTRequest,
    db: Session = Depends(getSession),
    user=Depends(getCurrentUser)
):
    taxRecord = controller.getTaxRecordById(
        recordId=recordId,
        db=db
    )
    if not taxRecord:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = constants.RECORD_NOT_FOUND
        )
    if constants.USER_ROLE_ADMIN not in user.userRole.split(',') and user.username != taxRecord.collectorId:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=constants.INSUFFICIENT_PERMISSIONS
        )
    if updateData.amount is not None:
        taxRecord.amount = updateData.amount
    return controller.updateTaxRecordById(
        taxRecord=taxRecord,
        db=db
    )        