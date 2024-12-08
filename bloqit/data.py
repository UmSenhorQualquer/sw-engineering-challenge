from sqlmodel import Session, select
import json
import os

from .models.bloq import Bloq
from .models.locker import Locker
from .models.rent import Rent

def load_json_data(engine):
    with Session(engine) as session:
        # Check if data already exists
        existing_bloqs = session.exec(select(Bloq)).first()
        if existing_bloqs:
            return  # Data already loaded
        
        # Load JSON files
        data_dir = "./data"
        
        # Load Bloqs first
        with open(os.path.join(data_dir, "bloqs.json")) as f:
            bloqs_data = json.load(f)
            for bloq_data in bloqs_data:
                bloq_id = bloq_data["id"]

                bloq = session.get(Bloq, bloq_id)
                if not bloq:
                    bloq = Bloq(**bloq_data)
                    session.add(bloq)

        session.commit()
        
        # Load Lockers
        with open(os.path.join(data_dir, "lockers.json")) as f:
            lockers_data = json.load(f)
            for locker_data in lockers_data:
                
                locker_id = locker_data["id"]
                locker = session.get(Locker, locker_id)
                if not locker:
                    locker = Locker(**locker_data)
                    session.add(locker)
        session.commit()
        
        # Load Rents
        with open(os.path.join(data_dir, "rents.json")) as f:
            rents_data = json.load(f)
            for rent_data in rents_data:
                
                rent_id = rent_data["id"]
                rent = session.get(Rent, rent_id)
                if not rent:
                    rent = Rent(**rent_data)
                    session.add(rent)
        session.commit()
