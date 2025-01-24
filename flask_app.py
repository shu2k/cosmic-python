from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()  #(1)
    repo = repository.SqlAlchemyRepository(session)  #(1)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],  #(2)
    )

    try:
        batchref = services.allocate(line, repo, session)  #(2)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400  #(3)

    return {"batchref": batchref}, 201  #(3)
