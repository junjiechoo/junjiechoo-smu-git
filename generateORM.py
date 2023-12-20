import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator

def generate_model(host, user, password, database, outfile = None):
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
    metadata = MetaData(bind=engine)
    metadata.reflect()
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)

if __name__ == '__main__':
    generate_model('spm.cjoz1mqq6cvp.us-east-1.rds.amazonaws.com:5432', 'spm', 'ilovespm', 'spm', 'db.py')