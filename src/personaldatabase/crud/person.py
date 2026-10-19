from personaldatabase.schemas.filters import PersonFilterParams
from datetime import date
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_group_model import PersonGroupModel
from personaldatabase.models.person_verv_model import PersonVervModel

def get_filtered_persons(db: Session, filters: PersonFilterParams) -> list[PersonModel]:
    query = select(PersonModel)

    # 1. Fritekst-søk (fornavn, etternavn, fullt navn, e-post)
    if filters.q:
        term = f"%{filters.q.strip()}%"
        query = query.where(
            or_(
                PersonModel.first_name.ilike(term),
                PersonModel.last_name.ilike(term),
                PersonModel.email.ilike(term),
            )
        )

    # 2. Aktiv-status
    if filters.is_active is not None:
        query = query.where(PersonModel.is_active == filters.is_active)

    # 3. Filtrering på Verv (bruker .any() for å unngå duplikater via EXISTS)
    if filters.verv_id is not None:
        query = query.where(
            PersonModel.verv.any(PersonVervModel.verv_id == filters.verv_id)
        )

    # 4. Filtrering på Gruppe / Avdeling
    if filters.group_id is not None:
        query = query.where(
            PersonModel.groups.any(PersonGroupModel.group_id == filters.group_id)
        )

    # 5. Filtrering på Alder (regnes om til birthdate-datoer)
    today = date.today()
    if filters.max_age is not None:
        earliest_birthdate = date(today.year - filters.max_age - 1, today.month, today.day)
        query = query.where(PersonModel.birthdate > earliest_birthdate)

    if filters.min_age is not None:
        latest_birthdate = date(today.year - filters.min_age, today.month, today.day)
        query = query.where(PersonModel.birthdate <= latest_birthdate)

    # 6. Dato for signert medarbeideravtale
    if filters.signed_contract_after is not None:
        query = query.where(PersonModel.last_signed_contract >= filters.signed_contract_after)

    if filters.signed_contract_before is not None:
        query = query.where(PersonModel.last_signed_contract <= filters.signed_contract_before)

    # 7. Sortering og paginering
    query = (
        query
        .order_by(PersonModel.last_name, PersonModel.first_name)
        .offset(filters.skip)
        .limit(filters.limit)
    )

    return list(db.scalars(query).all())
