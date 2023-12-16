"""
Script to build the database and populate it with data from Notion

"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base, Client, FermentorModel, Fermentor, FermentationProcess, FermentationSample
from notion import download_notion_data


def build_database():
    engine = create_engine('sqlite:///ferment.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    df = download_notion_data()

    for index, row in df.iterrows():
        client = session.query(Client).filter_by(name=row['Dye House']).first()
        if not client:
            client = Client(name=row['Dye House'], location=row['Location'])
            session.add(client)

        model = session.query(FermentorModel).filter_by(name=row['Fermentor Model']).first()
        if not model:
            model = FermentorModel(name=row['Fermentor Model'])
            session.add(model)

        fermentor = session.query(Fermentor).filter_by(
            name=row['Fermentor Name'], client_id=client.id, model_id=model.id
        ).first()
        if not fermentor:
            fermentor = Fermentor(name=row['Fermentor Name'], model=model, client=client)
            session.add(fermentor)

        process = FermentationProcess(is_blank=(row['Type'] == 'Blank'), fermentor=fermentor)
        sample = FermentationSample(timestamp=row['Timestamp'], url=row['URL'], process=process)

        session.add_all([process, sample])

    # Commit the changes to the database
    session.commit()


if __name__ == "__main__":
    build_database()
