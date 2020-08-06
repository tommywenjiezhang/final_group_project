from flask_restful import Resource, reqparse
from flask import Response, request, render_template, make_response, redirect
import json
from server.model.datasetModel import DatasetModel, DatasetSchema
from datetime import datetime
import re
import pytz
from server.calculator.Calculator import basicStatisic
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_user, logout_user, \
    login_required, current_user
from .form import DatasetForm
from server.util import combinUrl

class IndexRoute(Resource):
    def get(self):
        datasets = DatasetModel.query.all()
        datasetSchema = DatasetSchema()
        jsonRes = json.dumps([datasetSchema.dump(dataset) for dataset in datasets])
        return Response(response=jsonRes, status=200)

class NewRoute(Resource):

    def get(self):
        datasetForm = DatasetForm()
        html = render_template('dataset/new.html', form=datasetForm)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)

    @login_required
    def post(self):
        datasetForm = DatasetForm(request.form)
        user = current_user
        datasetObj = {"title": datasetForm.title.data,
                      'description': datasetForm.description.data,
                      "created_at": datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'),
                      'user_id': current_user.id
                      }
        datasetValue = getValues(datasetForm.values.data)
        dataset = DatasetModel(**datasetObj)
        dataset.save_to_db(datasetValue)
        return redirect("http://localhost:8081/")



class CalculationRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('values', type=str)

    def get(self,id):
        dataset = DatasetModel.findById(id)
        values = dataset.getDataSet()
        schema = DatasetSchema()
        datasetSchema= schema.dump(dataset)
        valuesJson = {"values":values}
        basicstats = {'calculation': basicStatisic(values)}
        mergeObj = {**datasetSchema, **valuesJson, **basicstats}
        return Response(response=json.dumps(mergeObj), status=200, mimetype="application/json")

    def delete(self, id):
        dataset = DatasetModel.findById(id)
        if dataset:
            schema = DatasetSchema()
            deletedDataset = schema.dump(dataset)
            dataset.delete_from_db()
            message = {"dataset": deletedDataset, "message" : "dataset has successufully deleted"}
            jsonResponse = json.dumps({**message})
            return Response(response=jsonResponse,status=200, mimetype="application/json")

    def put(self, id):
        data = CalculationRoute.parser.parse_args()
        dataset = DatasetModel.findById(id)
        if dataset:
            dataset.modified_db_value(data['title'],data['description'],getValues(data['values']))
        else:
            datasetObj = {"title": data['title'],
                          'description': data['description'],
                          "created_at": datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'),
                          'user_id': 1
                          }
            dataset = DatasetModel(**datasetObj)
            dataset.save_to_db(getValues(data['values']))
        return Response(response=json.dumps({"message": "dataset successfully edited"}),status=200,mimetype="application/json")







def getValues(data):
    sparator = re.compile(r'\,')
    return sparator.split(data)