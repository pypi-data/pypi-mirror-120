import os
import re
import sys
import json
import shutil
import logging
import zipfile
import requests
from datetime import datetime

import pandas as pd

from onesaitplatform.iotbroker import DigitalClient
from onesaitplatform.files import FileManager

import urllib3
urllib3.disable_warnings()

DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%SZ"
DIGITAL_CLIENT_JOIN_MESSAGE = "Digital Client joining server"
DIGITAL_CLIENT_GET_ERROR_MESSAGE = "Not possible to get data from server with Digital Client: {}"
DIGITAL_CLIENT_JOIN_ERROR_MESSAGE = "Not possible to join server with Digital Client: {}"
DIGITAL_CLIENT_JOIN_SUCCESS_MESSAGE = "Digital Client joined server: {}"
FILE_MANAGER_GET_ERROR_MESSAGE = "Not possible to download with File Manager: {}"
TRAINING_SUCCESS_MESSAGE = "Training finished with metrics: {}"
logger = logging.getLogger('onesait.platform.model.BaseModelService')
logger.setLevel(logging.WARNING)

class AuditClient(object):
    """Client to API for audit in Platform"""

    def __init__(self, protocol=None, host=None, port=None, token=None):

        ERROR_MESSAGE = 'Mandatory attribute {} not specified'
        if protocol is None:
            raise AttributeError(ERROR_MESSAGE.format('protocol'))
        if host is None:
            raise AttributeError(ERROR_MESSAGE.format('host'))
        if port is None:
            raise AttributeError(ERROR_MESSAGE.format('port'))
        if token is None:
            raise AttributeError(ERROR_MESSAGE.format('token'))

        port = str(port)
        url = "{protocol}://{host}:{port}/controlpanel/api/audit/".format(
            protocol=protocol, host=host, port=port
            )
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'accept': '*/*'
            }

        self.url = url
        self.headers = headers

    def report(
        self, message=None, ontology=None, operation_type=None,
        other_type=None, result_operation=None, type_=None
        ):
        now = datetime.now()
        date_formated = now.strftime(DATETIME_PATTERN)
        data = [{
            "formatedTimeStamp": date_formated,
            "message": message,
            "ontology": ontology,
            "operationType": operation_type,
            "otherType": other_type,
            "resultOperation": result_operation,
            "timeStamp": datetime.timestamp(now),
            "type": type_
            }]
        response = requests.post(
            self.url, headers=self.headers, json=data, timeout=5
            )

        return response.status_code, response.text

class Config(object):
    """Class that manages configuration"""
    def __init__(self, parameters=None, file_path=None):

        self.PLATFORM_HOST = None
        self.PLATFORM_PORT = None
        self.PLATFORM_DIGITAL_CLIENT = None
        self.PLATFORM_DIGITAL_CLIENT_TOKEN = None
        self.PLATFORM_DIGITAL_CLIENT_PROTOCOL = 'https'
        self.PLATFORM_DIGITAL_CLIENT_AVOID_SSL_CERTIFICATE = True
        self.PLATFORM_ONTOLOGY_MODELS = None
        self.PLATFORM_USER_TOKEN = None
        self.TMP_FOLDER = '/tmp/'
        self.NAME = None

        if parameters:
            self.set_parameters(parameters)

        if file_path:
            with open(file_path, 'r') as filehandle:
                parameters = json.load(filehandle)
                self.set_parameters(parameters)
        ERROR_MESSAGE = 'Mandatory attribute {} not specified'
        if self.PLATFORM_HOST is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_HOST'))
        if self.PLATFORM_PORT is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_PORT'))
        if self.PLATFORM_DIGITAL_CLIENT is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_DIGITAL_CLIENT'))
        if self.PLATFORM_DIGITAL_CLIENT_TOKEN is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_DIGITAL_CLIENT_TOKEN'))
        if self.PLATFORM_DIGITAL_CLIENT_PROTOCOL is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_DIGITAL_CLIENT_PROTOCOL'))
        if self.PLATFORM_ONTOLOGY_MODELS is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_ONTOLOGY_MODELS'))
        if self.PLATFORM_USER_TOKEN is None:
            raise AttributeError(ERROR_MESSAGE.format('PLATFORM_USER_TOKEN'))
        if self.NAME is None:
            raise AttributeError(ERROR_MESSAGE.format('NAME'))

    def set_parameters(self, parameters):
        for key, value in parameters.items():
            self.__setattr__(key, value)
        logger.info('Model Service parameters instantiated: {}'.format(parameters))

class BaseModelService(object):
    """Base definition of a model service"""
    
    def __init__(self, config=None):
        """Initializes clients to interact with Platform ontologies and file system"""
        logger.info('Creating Model Service')
        self.config = Config(parameters=config)
        self.digital_client = self.create_digital_client()
        self.file_manager = self.create_file_manager()
        self.audit_client = self.create_audit_client()
        self.reload_model()

    def reload_model(self):
        """Reloads best model previously trained"""
        logger.info('Searching best available model')
        best_model_info = self.get_active_model()
        if best_model_info:
            logger.info('Best available model specifications: {}'.format(best_model_info))
            self.load_model_from_file_system(model_info=best_model_info)
        else:
            logger.info('Models not found')

    def create_digital_client(self):
        """Creates a digital client to communicate with Platform ontologies"""
        
        host = self.config.PLATFORM_HOST
        port = self.config.PLATFORM_PORT
        iot_client = self.config.PLATFORM_DIGITAL_CLIENT
        iot_client_token = self.config.PLATFORM_DIGITAL_CLIENT_TOKEN
        protocol = self.config.PLATFORM_DIGITAL_CLIENT_PROTOCOL
        avoid_ssl_certificate = self.config.PLATFORM_DIGITAL_CLIENT_AVOID_SSL_CERTIFICATE

        digital_client = DigitalClient(
            host=host, port=port, iot_client=iot_client, iot_client_token=iot_client_token
        )
        digital_client.protocol = protocol
        digital_client.avoid_ssl_certificate = avoid_ssl_certificate
        logger.info('Digital Client created: {}'.format(digital_client.to_json()))
        
        return digital_client

    def create_audit_client(self):
        """Creates a audit client to send logs to platform audit ontology"""
        
        host = self.config.PLATFORM_HOST
        port = self.config.PLATFORM_PORT
        token = self.config.PLATFORM_USER_TOKEN
        protocol = self.config.PLATFORM_DIGITAL_CLIENT_PROTOCOL

        audit_client = AuditClient(
            host=host, port=port, protocol=protocol, token=token
        )

        logger.info('Audit Client created: {}'.format(
            [protocol, host, port, token]
        ))
        
        return audit_client

    def report(self, message=None, result=None):
        """Report event in audit"""
        self.audit_client.report(
            message=message, result_operation=result,
            type_='GENERAL', operation_type='INDICATION'
            )

    def join_digital_client(self):
        """Digital client connects the server"""
        if not self.digital_client.is_connected:
            logger.info(DIGITAL_CLIENT_JOIN_MESSAGE)
            ok_join, res_join = self.digital_client.join()
            if not ok_join:
                self.audit_client.report(
                    message=DIGITAL_CLIENT_JOIN_MESSAGE, result_operation='ERROR',
                    type_='IOTBROKER', operation_type='JOIN'
                    )
                raise ConnectionError(
            DIGITAL_CLIENT_JOIN_ERROR_MESSAGE.format(self.digital_client.to_json())
            )
            else:
                logger.info(DIGITAL_CLIENT_JOIN_SUCCESS_MESSAGE.format(res_join))
                self.audit_client.report(
                    message=DIGITAL_CLIENT_JOIN_MESSAGE, result_operation='SUCCESS',
                    type_='IOTBROKER', operation_type='JOIN'
                    )

    def create_file_manager(self):
        """Creates a file manager to interact with Platform file system"""

        host=self.config.PLATFORM_HOST
        protocol=self.config.PLATFORM_DIGITAL_CLIENT_PROTOCOL
        user_token = self.config.PLATFORM_USER_TOKEN

        file_manager = FileManager(
            host=host, user_token=user_token
        )
        file_manager.protocol = protocol
        logger.info('File Manager created: {}'.format(file_manager.to_json()))
        return file_manager

    def get_model_in_ontology(self, query=None):
        """Search model with specific query"""

        self.join_digital_client()

        ontology = self.config.PLATFORM_ONTOLOGY_MODELS

        ok_query, res_query = self.digital_client.query(
            ontology=ontology, query=query, query_type="SQL"
            )
        if not ok_query:
            message = DIGITAL_CLIENT_GET_ERROR_MESSAGE.format(self.digital_client.to_json())
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='IOTBROKER', operation_type='QUERY'
                )
            raise ConnectionError(message)
        else:
            message = "Digital Client got models information"
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='IOTBROKER', operation_type='QUERY'
                )

        self.digital_client.leave()

        best_model = None
        if len(res_query):
            best_model = res_query[0][ontology]
        return best_model

    def get_model_by_id(self, model_id=None):
        """Search the model active in models ontology"""
        ontology = self.config.PLATFORM_ONTOLOGY_MODELS
        query = 'select * from {ontology} as c where c.{ontology}.id = "{model_id}"'.format(
            ontology=ontology, model_id=model_id
            )
        model_info = self.get_model_in_ontology(query=query)

        return model_info

    def get_active_model(self):
        """Search the model active in models ontology"""
        ontology = self.config.PLATFORM_ONTOLOGY_MODELS
        query = 'select * from {ontology} as c where c.{ontology}.active = 1'.format(
            ontology=ontology
            )
        model_info = self.get_model_in_ontology(query=query)

        return model_info

    def set_new_model_in_ontology(
        self, name=None, version=None, description=None, metrics=None, model_file_id=None,
        dataset_file_id=None, ontology_dataset=None, hyperparameters=None, extra_file_id=None,
        pretrained_model_id=None
        ):
        """Set the new model in models ontology"""

        def create_list_item(key, value):
            """Creates dict with key, value and dtype"""
            if isinstance(value, int):
                dtype = 'int'
            elif isinstance(value, float):
                dtype = 'float'
            else:
                dtype = 'string'
            value = str(value)
            item = {'name': key, 'value': value, 'dtype': dtype}
            return item

        self.join_digital_client()

        model_info = {
            self.config.PLATFORM_ONTOLOGY_MODELS: {
                'asset': self.config.NAME,
                'name': name,
                'version': version,
                'description': description,
                'date': datetime.now().strftime(DATETIME_PATTERN),
                'metrics': [create_list_item(key, value) for key, value in metrics.items()],
                'hyperparameters': [create_list_item(key, value) for key, value in hyperparameters.items()],
                'model_path': model_file_id,
                'active': False
            }
        }

        ontology = self.config.PLATFORM_ONTOLOGY_MODELS
        if ontology_dataset is not None:
            model_info[ontology]['ontology_dataset'] = ontology_dataset
        if dataset_file_id is not None:
            model_info[ontology]['dataset_path'] = dataset_file_id
        if extra_file_id is not None:
            model_info[ontology]['extra_path'] = extra_file_id
        if pretrained_model_id is not None:
            model_info[ontology]['pretrained_model_id'] = pretrained_model_id

        model_id = '_'.join(
            [
                model_info[ontology]['date'],
                str(model_info[ontology]['name']),
                str(model_info[ontology]['version'])
            ]
        )
        model_id = model_id.replace('-', '_')
        model_id = model_id.replace(':', '_')
        model_info[ontology]['id'] = model_id

        logger.info("Digital Client inserting model information: {}".format(model_info))

        ok_query, res_query = self.digital_client.insert(self.config.PLATFORM_ONTOLOGY_MODELS, [model_info])
        if not ok_query:
            message = "Digital Client could not insert model information: {}".format(res_query)
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='IOTBROKER', operation_type='INSERT'
                )
            raise ConnectionError(message)
        else:
            message = "Digital Client inserted model information: {}".format(res_query)
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='IOTBROKER', operation_type='INSERT'
                )

        self.digital_client.leave()

    def create_tmp_folder_name(self, suffix=None):
        """Creates a name for a temporal folder"""
        tmp_model_name = self.config.NAME + ' ' + datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        tmp_model_name = re.sub('[/\s:-]', '_', tmp_model_name)
        tmp_model_folder = self.config.TMP_FOLDER + '/' + tmp_model_name
        if suffix:
            tmp_model_folder = tmp_model_folder + '_' + str(suffix)
        tmp_model_folder = tmp_model_folder + '/'
        return tmp_model_folder, tmp_model_name

    def upload_model_to_file_system(self, model_folder=None, zip_path=None):
        """Zips all elements of model and uploads it to file system"""

        with zipfile.ZipFile(zip_path, 'w') as zip_fh:
            for filename in os.listdir(model_folder):
                zip_fh.write(model_folder + '/' + filename, filename)

        model_filename = os.path.basename(zip_path)
        uploaded, info = self.file_manager.upload_file(model_filename, zip_path)
        if not uploaded:
            message = "Not possible to upload with File Manager: {}".format(
                self.file_manager.to_json()
                )
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='GENERAL', operation_type='INSERT'
                )
            raise ConnectionError(message)
        else:
            message = "File manager uploaded model: {}".format(info)
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='GENERAL', operation_type='INSERT'
                )

        saved_file_id = info['id']

        return saved_file_id

    def download_from_file_system(
        self, file_id=None, local_folder=None, unzip=None
        ):
        """Download file from file repository to local folder"""
        downloaded, info = self.file_manager.download_file(
            file_id, filepath=local_folder
            )
        if not downloaded:
            message = FILE_MANAGER_GET_ERROR_MESSAGE.format(self.file_manager.to_json())
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='GENERAL', operation_type='QUERY'
                )
            raise ConnectionError(message)
        else:
            message = "File manager downloaded file: {}".format(info)
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='GENERAL', operation_type='QUERY'
                )
        if unzip:
            zip_path = info['name']
            zip_obj = zipfile.ZipFile(zip_path)
            files = zip_obj.namelist()
            for file in files:
                zip_obj.extract(file, local_folder)
        return info['name']

    def load_model_from_file_system(self, model_info=None):
        """Downloads a zip from File System and creates a model"""

        file_id = model_info['model_path']
        extra_file_id = None
        if 'extra_path' in model_info:
            extra_file_id = model_info['extra_path']

        hyperparameters = {}
        for hyperparameter in model_info['hyperparameters']:
            name = hyperparameter['name']
            value = hyperparameter['value']
            dtype = hyperparameter['dtype']
            if dtype == 'float':
                value = float(value)
            elif dtype == 'int':
                value = int(value)
            hyperparameters[name] = value

        tmp_model_folder, _ = self.create_tmp_folder_name()
        tmp_extra_folder, _ = self.create_tmp_folder_name(suffix='extra')
        os.mkdir(tmp_model_folder)
        os.mkdir(tmp_extra_folder)
        self.download_from_file_system(
            file_id=file_id, local_folder=tmp_model_folder, unzip=True
        )
        if extra_file_id:
            self.download_from_file_system(
                file_id=extra_file_id, local_folder=tmp_extra_folder, unzip=True
        )
        self.load_model(
            model_path=tmp_model_folder, hyperparameters=hyperparameters,
            extra_path=tmp_extra_folder
            )
        shutil.rmtree(tmp_model_folder)
        shutil.rmtree(tmp_extra_folder)

    def train_from_file_system(
        self, name=None, version=None, description=None,
        dataset_file_id=None, hyperparameters=None,
        extra_file_id=None, pretrained_model_id=None
        ):
        """Trains a model given a file in file system"""

        logger.info("Training model from file repository: {}".format(
            [name, version, dataset_file_id, hyperparameters]
        ))

        tmp_model_folder, model_name = self.create_tmp_folder_name()
        tmp_extra_folder, _ = self.create_tmp_folder_name(suffix='extra')
        tmp_pretrained_folder, _ = self.create_tmp_folder_name(suffix='pretrained')
        os.mkdir(tmp_model_folder)
        os.mkdir(tmp_pretrained_folder)

        dataset_path = self.download_from_file_system(
            file_id=dataset_file_id, local_folder=tmp_model_folder
        )

        if extra_file_id:
            self.download_from_file_system(
                file_id=extra_file_id, local_folder=tmp_extra_folder, unzip=True
                )
        if pretrained_model_id:
            pretrained_model_info = self.get_model_by_id(model_id=pretrained_model_id)
            model_path = pretrained_model_info['model_path']
            self.download_from_file_system(
                file_id=model_path, local_folder=tmp_pretrained_folder, unzip=True
                )

        logger.info("Training started with dataset {} and output folder {}".format(
            dataset_path, tmp_model_folder
            ))
        metrics = self.train(
            dataset_path=dataset_path, hyperparameters=hyperparameters,
            model_path=tmp_model_folder, extra_path=tmp_extra_folder,
            pretrained_path=tmp_pretrained_folder
            )
        logger.info(TRAINING_SUCCESS_MESSAGE.format(metrics))
        os.remove(dataset_path)

        zip_path = self.config.TMP_FOLDER + '/' + model_name + '.zip'
        model_file_id = self.upload_model_to_file_system(
            model_folder=tmp_model_folder, zip_path=zip_path
            )
        shutil.rmtree(tmp_model_folder)
        shutil.rmtree(tmp_extra_folder)
        shutil.rmtree(tmp_pretrained_folder)
        os.remove(zip_path)

        self.set_new_model_in_ontology(
            name=name, version=version, description=description, metrics=metrics,
            model_file_id=model_file_id, dataset_file_id=dataset_file_id,
            hyperparameters=hyperparameters, extra_file_id=extra_file_id,
            pretrained_model_id=pretrained_model_id
            )

    def train_from_ontology(
        self, name=None, version=None, description=None,
        ontology_dataset=None, hyperparameters=None,
        extra_file_id=None, pretrained_model_id=None
        ):
        """Trains a model given the content of an ontology"""

        logger.info("Training model from ontology: {}".format(
            [name, version, ontology_dataset, hyperparameters]
        ))

        tmp_model_folder, model_name = self.create_tmp_folder_name()
        tmp_extra_folder, _ = self.create_tmp_folder_name(suffix='extra')
        tmp_pretrained_folder, _ = self.create_tmp_folder_name(suffix='pretrained')
        os.mkdir(tmp_model_folder)
        os.mkdir(tmp_extra_folder)
        os.mkdir(tmp_pretrained_folder)

        if extra_file_id:
            self.download_from_file_system(
                file_id=extra_file_id, local_folder=tmp_extra_folder, unzip=True
                )

        if pretrained_model_id:
            pretrained_model_info = self.get_model_by_id(model_id=pretrained_model_id)
            model_path = pretrained_model_info['model_path']
            self.download_from_file_system(
                file_id=model_path, local_folder=tmp_pretrained_folder, unzip=True
                )

        query = "db.{ontology}.find()".format(ontology=ontology_dataset)
        query_type = 'NATIVE'
        query_batch_size = 900

        self.join_digital_client()

        ok_query, res_query = self.digital_client.query_batch(
            ontology_dataset, query, query_type, batch_size=query_batch_size
            )
        if not ok_query:
            message = DIGITAL_CLIENT_GET_ERROR_MESSAGE.format(self.digital_client.to_json())
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='IOTBROKER', operation_type='BATCH'
                )
            raise ConnectionError(message)
        else:
            message = "Digital Client got dataset"
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='IOTBROKER', operation_type='BATCH'
                )
    
        self.digital_client.leave()

        dataset = pd.read_json(json.dumps(res_query))
        dataset_path = tmp_model_folder + '/dataset.csv'
        dataset.to_csv(dataset_path, sep='\t', index=False)

        logger.info("Training started with dataset {} and output folder {}".format(
            dataset_path, tmp_model_folder
            ))
        metrics = self.train(
            dataset_path=dataset_path, hyperparameters=hyperparameters,
            model_path=tmp_model_folder, extra_path=tmp_extra_folder,
            pretrained_path=tmp_pretrained_folder
            )
        logger.info(TRAINING_SUCCESS_MESSAGE.format(metrics))
        os.remove(dataset_path)

        zip_path = self.config.TMP_FOLDER + '/' + model_name + '.zip'
        model_file_id = self.upload_model_to_file_system(
            model_folder=tmp_model_folder, zip_path=zip_path
            )
        shutil.rmtree(tmp_model_folder)
        shutil.rmtree(tmp_extra_folder)
        shutil.rmtree(tmp_pretrained_folder)

        self.set_new_model_in_ontology(
            name=name, version=version, description=description, metrics=metrics,
            model_file_id=model_file_id, ontology_dataset=ontology_dataset,
            hyperparameters=hyperparameters, extra_file_id=extra_file_id,
            pretrained_model_id=pretrained_model_id
            )

    def train_from_external_source(
        self, name=None, version=None, description=None, hyperparameters=None,
        extra_file_id=None, pretrained_model_id=None
        ):
        """Trains a model given am external source"""

        logger.info("Training model from external source: {}".format(
            [name, version, hyperparameters]
        ))

        tmp_model_folder, model_name = self.create_tmp_folder_name()
        tmp_extra_folder, _ = self.create_tmp_folder_name(suffix='extra')
        tmp_pretrained_folder, _ = self.create_tmp_folder_name(suffix='pretrained')
        os.mkdir(tmp_model_folder)
        os.mkdir(tmp_extra_folder)
        os.mkdir(tmp_pretrained_folder)

        if extra_file_id:
            self.download_from_file_system(
                file_id=extra_file_id, local_folder=tmp_extra_folder, unzip=True
                )
        if pretrained_model_id:
            pretrained_model_info = self.get_model_by_id(model_id=pretrained_model_id)
            model_path = pretrained_model_info['model_path']
            self.download_from_file_system(
                file_id=model_path, local_folder=tmp_pretrained_folder, unzip=True
                )

        logger.info("Training started with external source and output folder {}".format(
            tmp_model_folder
            ))
        metrics = self.train(
            hyperparameters=hyperparameters, model_path=tmp_model_folder, extra_path=tmp_extra_folder,
            pretrained_path=tmp_pretrained_folder
            )
        logger.info(TRAINING_SUCCESS_MESSAGE.format(metrics))

        zip_path = self.config.TMP_FOLDER + '/' + model_name + '.zip'
        model_file_id = self.upload_model_to_file_system(
            model_folder=tmp_model_folder, zip_path=zip_path
            )
        
        shutil.rmtree(tmp_model_folder)
        shutil.rmtree(tmp_extra_folder)
        shutil.rmtree(tmp_pretrained_folder)
        os.remove(zip_path)

        if not metrics:
            metrics = {}
        if not hyperparameters:
            hyperparameters = {}
        self.set_new_model_in_ontology(
            name=name, version=version, description=description, metrics=metrics,
            model_file_id=model_file_id, hyperparameters=hyperparameters,
            extra_file_id=extra_file_id, pretrained_model_id=pretrained_model_id
            )

    def predict_from_ontology(
        self, input_ontology=None, output_ontology=None
        ):
        """Predicts given input in a ontology"""

        logger.info("Predicting from ontology {}".format(input_ontology))

        query = "db.{ontology}.find()".format(ontology=input_ontology)
        query_type = 'NATIVE'
        query_batch_size = 900

        self.join_digital_client()

        ok_query, res_query = self.digital_client.query_batch(
            input_ontology, query, query_type, batch_size=query_batch_size
            )
        if not ok_query:
            message = DIGITAL_CLIENT_GET_ERROR_MESSAGE.format(self.digital_client.to_json())
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='IOTBROKER', operation_type='BATCH'
                )
            raise ConnectionError(message)
        else:
            message = "Digital Client got dataset"
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='IOTBROKER', operation_type='BATCH'
                )
    
        self.digital_client.leave()

        logger.info("Inference started with ontology {}".format(input_ontology))
        predictions = self.predict(inputs=res_query)
        logger.info("Inference finished")

        if output_ontology is not None:
            self.insert_dataset_in_ontology(
                inputs=predictions, ontology=output_ontology
                )

        return predictions


    def predict_from_file_system(
        self, dataset_file_id=None, output_ontology=None
        ):
        """Predics given a file in file system"""

        logger.info("Predicting from file repository: {}".format(dataset_file_id))

        tmp_folder, _ = self.create_tmp_folder_name()
        os.mkdir(tmp_folder)

        dataset_path = self.download_from_file_system(
            file_id=dataset_file_id, local_folder=tmp_folder
        )

        logger.info("Inference started with dataset {}".format(dataset_path))
        predictions = self.predict(dataset_path=dataset_path)
        logger.info("Inference finished")
        shutil.rmtree(tmp_folder)

        if output_ontology is not None:
            self.insert_dataset_in_ontology(
                inputs=predictions, ontology=output_ontology
                )

        return predictions

    def insert_dataset_in_ontology(self, inputs=None, ontology=None):
        """Inserts predictions in ontology"""
        self.join_digital_client()

        logger.info("Digital Client inserting predictions")

        ok_query, res_query = self.digital_client.insert(ontology, inputs)
        if not ok_query:
            message = "Digital Client could not insert predictions: {}".format(res_query)
            self.audit_client.report(
                message=message, result_operation='ERROR',
                type_='IOTBROKER', operation_type='INSERT'
                )
            raise ConnectionError(message)
        else:
            message = "Digital Client inserted predictions: {}".format(res_query)
            logger.info(message)
            self.audit_client.report(
                message=message, result_operation='SUCCESS',
                type_='IOTBROKER', operation_type='INSERT'
                )

        self.digital_client.leave()

    def load_model(self, model_path=None, hyperparameters=None, extra_path=None):
        """Loads the model given input files and/or folders"""
        raise NotImplementedError

    def train(
        self, dataset_path=None, hyperparameters=None,
        model_path=None, extra_path=None, pretrained_path=None):
        """Trains a model given a dataset"""
        raise NotImplementedError

    def predict(self, inputs=None, dataset_path=None):
        """Predicts given a model and an array of inputs or a dataset"""
        raise NotImplementedError