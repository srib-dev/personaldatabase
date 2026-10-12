from datetime import date
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel

class PersonFilterParams(BaseModel):
    # Tekstsøk
    q: Annotated[str | None, Query(description="Søk i fornavn, etternavn eller e-post")] = None

    # Status
    is_active: Annotated[bool | None, Query(description="Filtrer på aktiv status")] = None

    # Relasjoner: Verv og Avdeling/Gruppe
    verv_id: Annotated[int | None, Query(description="Filtrer etter ID på verv")] = None
    group_id: Annotated[int | None, Query(description="Filtrer etter ID på gruppe/avdeling")] = None

    # Alder (regnes om til fødselsdato)
    min_age: Annotated[int | None, Query(ge=0, le=120, description="Minimumsalder i år")] = None
    max_age: Annotated[int | None, Query(ge=0, le=120, description="Maksimumsalder i år")] = None

    # Medarbeideravtale
    signed_contract_after: Annotated[date | None, Query(description="Signert avtale etter eller på dato")] = None
    signed_contract_before: Annotated[date | None, Query(description="Signert avtale før eller på dato")] = None

    # Paginering
    skip: Annotated[int, Query(ge=0)] = 0
    limit: Annotated[int, Query(ge=1, le=100)] = 50
