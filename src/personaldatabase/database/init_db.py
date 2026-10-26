import os
from datetime import date
from sqlalchemy import select

from personaldatabase.core.security import get_password_hash
from personaldatabase.database.session import SessionLocal
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel


def init_db() -> None:
    """Oppretter Admin-verv og første admin-bruker hvis de ikke finnes fra før."""
    admin_email = os.getenv("ADMIN_EMAIL").strip().lower()
    admin_password = os.getenv("ADMIN_PASSWORD")

    with SessionLocal() as db:
        # 1. Sikre at "Admin"-vervet eksisterer
        admin_verv = db.scalar(select(VervModel).where(VervModel.verv_name.ilike("Admin")))
        if not admin_verv:
            admin_verv = VervModel(verv_name="Admin", role="Admin")
            db.add(admin_verv)
            db.flush()

        # 2. Sikre at første admin-person eksisterer
        admin_person = db.scalar(select(PersonModel).where(PersonModel.email == admin_email))
        if not admin_person:
            admin_person = PersonModel(
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                first_name="Admin",
                last_name="SRIB",
                school="UiB",
                last_signed_contract=date.today(),
                phone_number="00000000",
                postbox="5007",
                street_name="Fosswinckels gate 14",
                student_card_number=0,
                status=True,
                birthdate=date(2000, 1, 1),
                picture="",
                gender="Annet",
                is_active=True,
            )
            db.add(admin_person)
            db.flush()
        elif not admin_person.hashed_password:
            admin_person.hashed_password = get_password_hash(admin_password)

        # 3. Koble admin-personen til Admin-vervet hvis koblingen mangler
        if not db.get(PersonVervModel, (admin_person.id, admin_verv.id)):
            db.add(PersonVervModel(person_id=admin_person.id, verv_id=admin_verv.id))

        db.commit()
