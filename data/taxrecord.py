from objects.taxrecord import TaxRecordPOST, TaxRecord, TaxRecordGET
from objects.assignment import Assignment
from db import SessionDep
from auth.auth import getCurrentUser, getCurrentAdmin
from fastapi import Depends, HTTPException

#@router.post("/collect-tax", response_model=TaxCollectionRead)
def insertTaxRecord(
        taxData : TaxRecordPOST,
        db: SessionDep,
        user=Depends(getCurrentUser),
):
    # # Ensure user is a collector
    # if user.role != "collector":
    #     raise HTTPException(status_code=403, detail="Only collectors can record tax collection")

    # # Ensure collector is assigned to this household
    # assignment = session.exec(
    #     select(CollectorAssignment).where(
    #         (CollectorAssignment.collector_id == user.id) & (CollectorAssignment.household_id == tax_data.household_id)
    #     )
    # ).first()

    # if not assignment:
    #     raise HTTPException(status_code=403, detail="You are not assigned to this household")
    taxRecord = TaxRecordPOST(collectorId=user.id, **taxData.dict())
    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord

#@router.get("/tax-records", response_model=List[TaxRecordGET])
def getTaxRecords(db: SessionDep):
    return db.exec(select(TaxRecord)).all()

#@router.get("/tax-records/{household_id}", response_model=List[TaxRecordGET])
def getTaxRecordByHouse(
        houseNumber: str, 
        db: SessionDep
):
    return db.exec(select(TaxRecord).where(TaxRecord.houseId == houseNumber)).all()

# @router.put("/tax-records/{record_id}", response_model=TaxRecordPOST)
def update_tax_record(
    recordId: int,
    updateData: TaxRecordPOST,
    db: SessionDep,
    admin=Depends(getCurrentAdmin),
):
    taxRecord = db.get(TaxRecord, recordId)
    if not taxRecord:
        raise HTTPException(status_code=404, detail="Tax record not found")

    if updateData.amount is not None:
        taxRecord.amount = updateData.amount

    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord