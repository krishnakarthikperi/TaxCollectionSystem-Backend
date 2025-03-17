"""
This module provides functions to manage tax records in the database.
Functions:
    insertTaxRecords(taxRecords: List[TaxRecordPOSTRequest], db: Session):
        Inserts a list of tax records into the database.
    getTaxRecords(db: Session):
        Retrieves all tax records from the database.
    getTaxRecordByHouse(houseNumber: str, db: Session):
        Retrieves tax records associated with a specific house number.
    updateTaxRecordById(taxRecord: TaxRecord, db: Session, admin):
        Updates an existing tax record in the database by its ID.
    getTaxRecordById(recordId: int, db: Session):
        Retrieves a tax record by its unique ID.
"""

from typing import List
from sqlmodel import Session, select
from objects.taxrecord import TaxRecordPOSTRequest, TaxRecord, TaxRecordPUTRequest
from db import getSession
from auth.auth import getCurrentAdmin
from fastapi import Depends


def insertTaxRecords(
    taxRecords: List[TaxRecordPOSTRequest],
    db: Session = Depends(getSession),
):
    """
    Inserts a list of tax records into the database.
    Args:
        taxRecords (List[TaxRecordPOSTRequest]): A list of tax record objects to be inserted.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.
    Returns:
        List[TaxRecord]: A list of the inserted tax record objects with updated database state.
    """

    taxRecords = [TaxRecord(**taxRecord.model_dump()) for taxRecord in taxRecords]
    db.add_all(taxRecords)
    db.flush()
    [db.refresh(taxRecord) for taxRecord in taxRecords]
    db.commit()
    return taxRecords


def getTaxRecords(
    db: Session = Depends(getSession),
):
    """
    Retrieve all tax records from the database.
    Args:
        db (Session): A database session dependency, automatically provided by FastAPI's Depends.
    Returns:
        List[TaxRecord]: A list of all tax records retrieved from the database.
    """

    return db.exec(select(TaxRecord)).all()


def getTaxRecordByHouse(
    houseNumber: str,
    db: Session = Depends(getSession),
):
    """
    Retrieve tax records associated with a specific house number.
    Args:
        houseNumber (str): The unique identifier for the house.
        db (Session, optional): The database session dependency. Defaults to a session provided by `getSession`.
    Returns:
        List[TaxRecord]: A list of tax records matching the specified house number.
    """
    return db.exec(select(TaxRecord).where(TaxRecord.houseId == houseNumber)).all()


def updateTaxRecordById(
    taxRecord: TaxRecord,
    db: Session = Depends(getSession),
    admin=Depends(getCurrentAdmin),
):
    """
    Updates an existing tax record in the database by its ID.
    Args:
        taxRecord (TaxRecord): The tax record object containing updated data.
        db (Session, optional): The database session dependency. Defaults to Depends(getSession).
        admin (Any, optional): The current admin user dependency. Defaults to Depends(getCurrentAdmin).
    Returns:
        TaxRecord: The updated tax record object after being committed to the database.
    """

    db.add(taxRecord)
    db.commit()
    db.refresh(taxRecord)
    return taxRecord


def getTaxRecordById(
    recordId: int,
    db: Session = Depends(getSession),
):
    """
    Retrieve a tax record by its unique identifier.
    Args:
        recordId (int): The unique identifier of the tax record to retrieve.
        db (Session, optional): The database session dependency. Defaults to a session provided by `getSession`.
    Returns:
        TaxRecord: The tax record corresponding to the given `recordId`, or `None` if no record is found.
    """

    return db.get(TaxRecord, recordId)
