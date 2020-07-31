from flask_restful import Resource, reqparse
from flask import Response
import json
from server.model.datasetModel import DatasetModel, DatasetSchema
from datetime import datetime
import re
import pytz


class IndexRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('values', type=str)

    def get(self):
        datasets = DatasetModel.query.all()
        datasetSchema = DatasetSchema()
        jsonRes = json.dumps([datasetSchema.dump(dataset) for dataset in datasets])
        return Response(response=jsonRes, status=200)

    def post(self):
        data = IndexRoute.parser.parse_args()
        datasetObj = {"title": data['title'],
                      'description': data['description'],
                      "created_at": datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'),
                      'user_id':1
                      }
        datasetValue = getValues(data['values'])
        dataset = DatasetModel(**datasetObj)
        dataset.save_to_db(datasetValue)

        return datasetObj


class CalculationRoute(Resource):
    def get(self,id):
        dataset = DatasetModel.query.filter_by(id=id).first()
        values = dataset.getDataSet()
        schema = DatasetSchema()
        datasetSchema= schema.dump(dataset)
        valuesJson = {"values":values}
        mergeObj = {**datasetSchema, **valuesJson}
        return Response(response=json.dumps(mergeObj), status=200, mimetype="application/json")





def getValues(data):
    sparator = re.compile(r'\,')
    return sparator.split(data)