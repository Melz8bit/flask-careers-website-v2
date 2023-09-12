import sqlalchemy

from sqlalchemy import create_engine, text
from sqlalchemy.util import deprecations

deprecations.SILENCE_UBER_WARNING = 1

DB_CONNECTION_STRING = "mysql+pymysql://kjx2kr0lpokqtii1snu8:pscale_pw_QiROPMDC4UVFooJgDjNMY7qndcPSzRyIaQ67GmSQHOa@aws.connect.psdb.cloud/flaskcareers?charset=utf8mb4"

engine = create_engine(DB_CONNECTION_STRING,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem",
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))

    jobs = []
    for row in result.all():
      jobs.append(dict(row))

    return jobs
