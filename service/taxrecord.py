"""
This module defines API endpoints for managing tax records in a tax collection system.
Endpoints:
    - POST /recordcollections:
        Inserts multiple tax records into the database. Ensures that the user is a collector
        and is assigned to the specified households. Only collectors and admins are authorized
        to perform this operation.
    - GET /gettaxrecords:
        Retrieves all tax records from the database. Requires the user to be authenticated.
    - GET /tax-records/{houseNumber}:
        Retrieves tax records for a specific house number. Requires the user to be authenticated.
    - PUT /tax-record/{recordId}:
        Updates a specific tax record by its ID. Ensures that the user is either an admin or
        the collector who created the record. Only authorized users can update the record.
Dependencies:
    - FastAPI's APIRouter for defining routes.
    - SQLModel's Session for database interactions.
    - Authentication and authorization utilities from the `auth` module.
    - Controllers for tax records and assignments.
    - Constants for error messages and user role definitions.
Models:
    - TaxRecordPOSTRequest: Represents the request body for creating tax records.
    - TaxRecordPOSTResponse: Represents the response body for created tax records.
    - TaxRecordGETRequest: Represents the response body for retrieving tax records.
    - TaxRecordPUTRequest: Represents the request body for updating a tax record.
    - TaxRecordPUTResponse: Represents the response body for updated tax records.
Error Handling:
    - Raises HTTP 403 Forbidden if the user is not authorized to perform an operation.
    - Raises HTTP 404 Not Found if a requested tax record does not exist.
    - Raises HTTP 401 Unauthorized if the user lacks sufficient permissions to update a record.
"""

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


@router.post(
    "/recordcollections",
    response_model=List[TaxRecordPOSTResponse],
)
def insertTaxRecords(
        taxData : List[TaxRecordPOSTRequest],
        user=Depends(getCurrentUser),
        db: Session = Depends(getSession)    
):
    """
    Inserts tax records into the database after performing necessary validations.
    Args:
        taxData (List[TaxRecordPOSTRequest]): A list of tax record data to be inserted.
        user (User, optional): The current authenticated user, injected via dependency. Defaults to Depends(getCurrentUser).
        db (Session, optional): The database session, injected via dependency. Defaults to Depends(getSession).
    Raises:
        HTTPException: If the user is not a collector.
        HTTPException: If the collector is not assigned to the specified household(s).
        HTTPException: If the user does not have the correct house mapping.
    Returns:
        Any: The result of the tax record insertion operation.
    """

    if constants.USER_ROLE_COLLECTOR not in user.userRole.split(','):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, 
            detail = constants.ONLY_COLLECTORS_RECORD_TAX_COLLECTION
        )

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
    return controller.insertTaxRecords(
        taxRecords=taxData,
        db=db,
    )


@router.get(
    "/gettaxrecords",
    response_model=List[TaxRecordGETRequest],
    dependencies=[Depends(getCurrentUser)],
)
def getTaxRecords(db: Session = Depends(getSession)):
    """
    Fetches tax records from the database.

    Args:
        db (Session): The database session dependency, provided by FastAPI's Depends.

    Returns:
        List[TaxRecord]: A list of tax records retrieved from the database.
    """
    return controller.getTaxRecords(db=db)


@router.get(
    "/tax-records/{houseNumber}",
    response_model=List[TaxRecordGETRequest],
    dependencies=[Depends(getCurrentUser)],
)
def getTaxRecordByHouse(
    houseNumber: str,
    db: Session = Depends(getSession),
):
    """
    Retrieve tax record information for a specific house.

    Args:
        houseNumber (str): The house number for which the tax record is to be retrieved.
        db (Session, optional): The database session dependency. Defaults to a session provided by `Depends(getSession)`.

    Returns:
        Any: The tax record information for the specified house, as retrieved by the controller.
    """
    return controller.getTaxRecordByHouse(
        houseNumber=houseNumber,
        db=db,
    )


@router.put(
    "/tax-record/{recordId}",
    response_model=TaxRecordPUTResponse,
)
def updateTaxRecordById(
    recordId: int,
    updateData: TaxRecordPUTRequest,
    db: Session = Depends(getSession),
    user=Depends(getCurrentUser),
):
    """
    Updates a tax record by its ID.

    Args:
        recordId (int): The ID of the tax record to update.
        updateData (TaxRecordPUTRequest): The data to update the tax record with.
        db (Session, optional): The database session dependency. Defaults to Depends(getSession).
        user (User, optional): The current authenticated user dependency. Defaults to Depends(getCurrentUser).

    Raises:
        HTTPException: If the tax record is not found (404).
        HTTPException: If the user does not have sufficient permissions (401).

    Returns:
        TaxRecord: The updated tax record.
    """
    taxRecord = controller.getTaxRecordById(
        recordId=recordId,
        db=db,
    )
    if not taxRecord:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.RECORD_NOT_FOUND,
        )
    if constants.USER_ROLE_ADMIN not in user.userRole.split(',') and user.username != taxRecord.collectorId:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.INSUFFICIENT_PERMISSIONS,
        )
    if updateData.amount is not None:
        taxRecord.amount = updateData.amount
    return controller.updateTaxRecordById(
        taxRecord=taxRecord,
        db=db,
    )
