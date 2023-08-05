import unittest
from sklearn.pipeline import Pipeline
from pprint import pprint
import pandas as pd
import traceback
from os import environ

from ibm_watson_machine_learning import APIClient

from ibm_watson_machine_learning.experiment import AutoAI
from ibm_watson_machine_learning.deployment import Batch
from ibm_watson_machine_learning.preprocessing import DataJoinGraph
from ibm_watson_machine_learning.preprocessing.data_join_pipeline import OBMPipelineGraphBuilder

from ibm_watson_machine_learning.helpers.connections import S3Connection, S3Location, DataConnection, FSLocation, AssetLocation

from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines

from ibm_watson_machine_learning.tests.utils import print_test_separators
from ibm_watson_machine_learning.utils.autoai.errors import WrongDataJoinGraphNodeName

from ibm_watson_machine_learning.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, bucket_exists, \
    create_bucket, get_space_id

from ibm_watson_machine_learning.tests.utils.cleanup import space_cleanup

from ibm_watson_machine_learning.tests.utils.cleanup import delete_model_deployment

from lale import wrap_imported_operators
from lale.operators import TrainablePipeline
from lale.lib.lale import Hyperopt

get_step_details = OBMPipelineGraphBuilder.get_step_details
get_join_extractors = OBMPipelineGraphBuilder.get_join_extractors
get_extractor_columns = OBMPipelineGraphBuilder.get_extractor_columns
get_extractor_transformations = OBMPipelineGraphBuilder.get_extractor_transformations


class TestOBMAndKB(unittest.TestCase):
    data_join_graph: 'DataJoinGraph' = None
    wml_client: 'APIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines: 'RemoteAutoPipelines' = None
    wml_credentials = None
    cos_credentials = None
    pipeline_opt: 'RemoteAutoPipelines' = None
    historical_opt: 'RemoteAutoPipelines' = None
    service: 'Batch' = None
    data_join_pipeline: 'DataJoinPipeline' = None

    data_location = './autoai/data/'

    trained_pipeline_details = None
    run_id = None

    data_connections = []
    data_connections_space_only = []
    main_conn = None
    customers_conn = None
    transactions_conn = None
    purchases_conn = None
    products_conn = None
    results_connection = None

    train_data = None
    holdout_data = None

    bucket_name = environ.get('BUCKET_NAME', "wml-autoaitests-obm-qa")
    pod_version = environ.get('KB_VERSION', None)
    space_name = environ.get('SPACE_NAME', 'regression_tests_sdk_space')

    cos_endpoint = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    cos_resource_instance_id = None
    data_cos_path = 'data/'

    results_cos_path = 'results_wml_autoai'

    pipeline: 'Pipeline' = None
    lale_pipeline = None
    deployed_pipeline = None
    hyperopt_pipelines = None
    new_pipeline = None
    new_sklearn_pipeline = None

    OPTIMIZER_NAME = 'OBM + KB test'
    DEPLOYMENT_NAME = "OBM + KB deployment test"

    job_id = None

    # note: notebook cos version:
    metadata = None
    local_optimizer_cos = None
    model_location = None
    training_status = None
    pipeline_name = None
    # --- end note

    project_id = None
    space_id = None
    asset_id = None

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.wml_credentials = get_wml_credentials()

        if not is_cp4d():
            cls.cos_credentials = get_cos_credentials()
            cls.cos_endpoint = cls.cos_credentials.get('endpoint_url')
            cls.cos_resource_instance_id = cls.cos_credentials.get('resource_instance_id')

        cls.wml_client = APIClient(wml_credentials=cls.wml_credentials.copy())
        cls.project_id = cls.wml_credentials.get('project_id')
        cls.wml_client.set.default_project(cls.project_id)


    @print_test_separators
    def test_00a_space_cleanup(self):
        space_cleanup(self.wml_client,
                      get_space_id(self.wml_client, self.space_name,
                                   cos_resource_instance_id=self.cos_resource_instance_id),
                      days_old=7)
        TestOBMAndKB.space_id = get_space_id(self.wml_client, self.space_name,
                                             cos_resource_instance_id=self.cos_resource_instance_id)


    @print_test_separators
    def test_00b_prepare_COS_instance(self):
        if self.wml_client.ICP or self.wml_client.WSD:
            self.skipTest("Prepare COS is available only for Cloud")

        import ibm_boto3
        cos_resource = ibm_boto3.resource(
            service_name="s3",
            endpoint_url=self.cos_endpoint,
            aws_access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
            aws_secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']
        )
        # Prepare bucket
        if not bucket_exists(cos_resource, self.bucket_name):
            TestOBMAndKB.bucket_name = create_bucket(cos_resource, self.bucket_name)

            self.assertIsNotNone(TestOBMAndKB.bucket_name)
            self.assertTrue(bucket_exists(cos_resource, TestOBMAndKB.bucket_name))

        print(f"Using COS bucket: {TestOBMAndKB.bucket_name}")

    @print_test_separators
    def test_01_create_multiple_data_connections__connections_created(self):
        print("Creating multiple data connections...")
        if self.wml_client.ICP:
            TestOBMAndKB.data_connections = []
            TestOBMAndKB.data_connections_space_only = []

            self.wml_client.set.default_project(self.project_id)

            for dataset_name in ['main', 'customers', 'transactions', 'purchase', 'products']:

                data_filename = f'group_customer_{dataset_name}.csv'
                asset_details = self.wml_client.data_assets.create(
                    name=data_filename,
                    file_path=self.data_location + data_filename)
                asset_id = asset_details['metadata']['guid']

                conn = DataConnection(
                    data_join_node_name=dataset_name,
                    data_asset_id=asset_id)

                TestOBMAndKB.data_connections.append(conn)


            # self.wml_client = APIClient(wml_credentials=self.wml_credentials)

            self.wml_client.set.default_space(self.space_id)
            for dataset_name in ['main', 'customers', 'transactions', 'purchase', 'products']:
                data_filename = f'group_customer_{dataset_name}.csv'
                # additional data assets for scoring in space should be also created

                asset_details = self.wml_client.data_assets.create(
                    name=data_filename,
                    file_path=self.data_location + data_filename)
                asset_id = asset_details['metadata']['guid']

                conn_space = DataConnection(
                    data_join_node_name=dataset_name,
                    data_asset_id=asset_id
                )
                    # location=AssetLocation(asset_id=asset_id))

                TestOBMAndKB.data_connections_space_only.append(conn_space)

            self.wml_client.set.default_project(self.project_id)

            TestOBMAndKB.results_connection = None
        else:
            TestOBMAndKB.main_conn = DataConnection(
                data_join_node_name="main",
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_main.csv'))

            TestOBMAndKB.customers_conn = DataConnection(
                data_join_node_name="customers",
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_customers.csv'))

            TestOBMAndKB.transactions_conn = DataConnection(
                data_join_node_name="transactions",
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_transactions.csv'))

            TestOBMAndKB.purchases_conn = DataConnection(
                data_join_node_name="purchase",
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_purchase.csv'))

            TestOBMAndKB.products_conn = DataConnection(
                data_join_node_name="products",
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_products.csv'))

            TestOBMAndKB.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )

            TestOBMAndKB.data_connections = [self.main_conn,
                                             self.customers_conn,
                                             self.transactions_conn,
                                             self.purchases_conn,
                                             self.products_conn]

    @print_test_separators
    def test_02_create_data_join_graph__graph_created(self):
        print("Defining DataJoinGraph...")
        data_join_graph = DataJoinGraph()
        data_join_graph.node(name="main")
        data_join_graph.node(name="customers")
        data_join_graph.node(name="transactions")
        data_join_graph.node(name="purchase")
        data_join_graph.node(name="products")
        data_join_graph.edge(from_node="main", to_node="customers",
                             from_column=["group_customer_id"], to_column=["group_customer_id"])
        data_join_graph.edge(from_node="main", to_node="transactions",
                             from_column=["transaction_id"], to_column=["transaction_id"])
        data_join_graph.edge(from_node="main", to_node="purchase",
                             from_column=["group_id"], to_column=["group_id"])
        data_join_graph.edge(from_node="transactions", to_node="products",
                             from_column=["product_id"], to_column=["product_id"])

        TestOBMAndKB.data_join_graph = data_join_graph

        print(f"data_join_graph: {data_join_graph}")

    # @print_test_separators
    # def test_03_data_join_graph_visualization(self):
    #     print("Visualizing data_join_graph...")
    #     self.data_join_graph.visualize()

    @print_test_separators
    def test_04_initialize_AutoAI_experiment__pass_credentials__object_initialized(self):
        print("Initializing AutoAI experiment...")
        TestOBMAndKB.experiment = AutoAI(wml_credentials=self.wml_credentials.copy(),
                                         project_id=self.project_id)

        self.assertIsInstance(self.experiment, AutoAI, msg="Experiment is not of type AutoAI.")

    @print_test_separators
    def test_05_save_remote_data_and_DataConnection_setup(self):
        print("Writing multiple data files to COS...")
        if is_cp4d():
            pass

        else:  # for cloud and COS
            self.main_conn.write(data=self.data_location + 'group_customer_main.csv',
                                 remote_name=self.data_cos_path + 'group_customer_main.csv')
            self.customers_conn.write(data=self.data_location + 'group_customer_customers.csv',
                                      remote_name=self.data_cos_path + 'group_customer_customers.csv')
            self.transactions_conn.write(data=self.data_location + 'group_customer_transactions.csv',
                                         remote_name=self.data_cos_path + 'group_customer_transactions.csv')
            self.purchases_conn.write(data=self.data_location + 'group_customer_purchase.csv',
                                      remote_name=self.data_cos_path + 'group_customer_purchase.csv')
            self.products_conn.write(data=self.data_location + 'group_customer_products.csv',
                                     remote_name=self.data_cos_path + 'group_customer_products.csv')

    @print_test_separators
    def test_06_initialize_optimizer(self):
        print("Initializing optimizer with data_join_graph...")
        TestOBMAndKB.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            prediction_type=AutoAI.PredictionType.REGRESSION,
            prediction_column='next_purchase',
            scoring=AutoAI.Metrics.ROOT_MEAN_SQUARED_ERROR,
            max_number_of_estimators=1,
            include_only_estimators=[self.experiment.RegressionAlgorithms.LGBM],
            data_join_graph=self.data_join_graph,
            t_shirt_size=self.experiment.TShirtSize.L if not is_cp4d() else self.experiment.TShirtSize.S,
            holdout_size=0.1,
            autoai_pod_version=self.pod_version
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    @print_test_separators
    def test_07_get_configuration_parameters_of_remote_auto_pipeline(self):
        print("Getting experiment configuration parameters...")
        parameters = self.remote_auto_pipelines.get_params()
        print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_08a_check_data_join_node_names(self):
        if self.wml_client.ICP:
            main_conn = DataConnection(
                location=FSLocation(path=self.data_location + 'group_customer_main.csv'))

            customers_conn = DataConnection(
                location=FSLocation(path=self.data_location + 'group_customer_customers.csv'))

            transactions_conn = DataConnection(
                location=FSLocation(path=self.data_location + 'group_customer_transactions.csv'))

            purchases_conn = DataConnection(
                location=FSLocation(path=self.data_location + 'group_customer_purchase.csv'))

            products_conn = DataConnection(
                location=FSLocation(path=self.data_location + 'group_customer_products.csv'))
        else:
            main_conn = DataConnection(
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_main.csv'))

            customers_conn = DataConnection(
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_customers.csv'))

            transactions_conn = DataConnection(
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_transactions.csv'))

            purchases_conn = DataConnection(
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_purchase.csv'))

            products_conn = DataConnection(
                connection=S3Connection(
                    endpoint_url=self.cos_endpoint,
                    access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                    secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path + 'group_customer_products.csv'))

        data_connections = [main_conn,
                            customers_conn,
                            transactions_conn,
                            purchases_conn,
                            products_conn]

        with self.assertRaises(WrongDataJoinGraphNodeName, msg="Training started with wrong data join node names"):
            self.remote_auto_pipelines.fit(
                training_data_reference=data_connections,
                training_results_reference=self.results_connection,
                background_mode=False)

    @print_test_separators
    def test_08b_fit_run_training_of_auto_ai_in_wml(self):
        print("Scheduling OBM + KB training...")
        TestOBMAndKB.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=self.data_connections,
            training_results_reference=self.results_connection,
            background_mode=False)

        TestOBMAndKB.run_id = self.trained_pipeline_details['metadata']['id']

        TestOBMAndKB.pipeline_name = 'Pipeline_4'

        status = self.remote_auto_pipelines.get_run_status()
        run_details = self.remote_auto_pipelines.get_run_details().get('entity')
        self.assertNotIn(status, ['failed', 'canceled'], msg=f"Training finished with status {status}. \n"
                                                             f"Details: {run_details.get('status')}")

        TestOBMAndKB.model_location = \
            self.trained_pipeline_details['entity']['status']['metrics'][-1]['context']['intermediate_model'][
                'location'][
                'model']
        TestOBMAndKB.training_status = self.trained_pipeline_details['entity']['results_reference']['location'][
            'training_status']

        for connection in self.data_connections:
            self.assertIsNotNone(
                connection.auto_pipeline_params,
                msg=f'DataConnection auto_pipeline_params was not updated for connection: {connection.id}')

    @print_test_separators
    def test_09_download_original_training_data(self):
        print("Downloading each training file...")
        for connection in self.remote_auto_pipelines.get_data_connections():
            train_data = connection.read()

            print(f"Connection: {connection.id} - train data sample:")
            print(train_data.head())
            self.assertGreater(len(train_data), 0)

    @print_test_separators
    def test_10_download_preprocessed_obm_training_data(self):
        print("Downloading OBM preprocessed training data with holdout split...")
        TestOBMAndKB.train_data, TestOBMAndKB.holdout_data = (
            self.remote_auto_pipelines.get_preprocessed_data_connection().read(with_holdout_split=True))

        print("OBM train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("OBM holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    @print_test_separators
    def test_11_visualize_obm_pipeline(self):
        print("Visualizing OBM model ...")
        TestOBMAndKB.data_join_pipeline = self.remote_auto_pipelines.get_preprocessing_pipeline()
        assert isinstance(self.data_join_pipeline._pipeline_json, list)
        assert '40 [label=NumberSet]' in self.data_join_pipeline._graph.__str__()

    #     self.data_join_pipeline.visualize()

    @print_test_separators
    def test_11b_check_if_data_join_pipeline_graph_correct(self):
        pipeline_json = self.data_join_pipeline._pipeline_json
        graph = self.data_join_pipeline._graph_json

        step_types = [message['feature_engineering_components']['obm'][0]['step_type'] for message in pipeline_json]
        last_non_join_iteration = step_types.index('join')
        selection_iteration = step_types.index('feature selection') + 1
        join_iterations = [i + 1 for i, x in enumerate(step_types) if x == "join"]

        for message in pipeline_json:
            name, iteration, _ = get_step_details(message)
            self.assertTrue(str(iteration) in graph['nodes'])

            if 1 < iteration <= 2:
                self.assertTrue(str(iteration) in graph['edges'][str(iteration - 1)])
            elif iteration in join_iterations:
                self.assertTrue(str(iteration) in graph['edges'][str(last_non_join_iteration)])
                extractors = get_join_extractors(message)

                if extractors is None:
                    continue
                for ext, i in zip(extractors, range(len(extractors))):
                    ext_index = str(iteration) + str(i)
                    self.assertTrue(ext_index in graph['nodes'] and
                                    ext_index in ext_index in graph['edges'][str(iteration)])

                    columns = get_extractor_columns(extractors[ext])
                    transformations = get_extractor_transformations(extractors[ext])
                    for j, column in enumerate(columns):
                        col_index = str(iteration) + str(i) + str(j)
                        self.assertTrue(col_index in graph['nodes'] and col_index in graph['edges'][str(ext_index)])

                        for transformation in transformations:
                            self.assertTrue(transformation in graph['edges'][str(col_index)])
                            self.assertTrue(str(selection_iteration) in graph['edges'][str(transformation)])

            elif iteration > selection_iteration:
                self.assertTrue(str(iteration) in graph['edges'][str(iteration - 1)])

    @print_test_separators
    def test_12_get_run_status(self):
        print("Getting training status...")
        status = self.remote_auto_pipelines.get_run_status()
        print(status)
        self.assertEqual("completed", status, msg="AutoAI run didn't finished successfully. Status: {}".format(status))

    @print_test_separators
    def test_13_get_run_details(self):
        print("Getting training details...")
        parameters = self.remote_auto_pipelines.get_run_details()
        print(parameters)
        self.assertIsNotNone(parameters)

    def test_13b_get_metrics(self):
        self.wml_client.training.get_metrics(self.run_id)

    @print_test_separators
    def test_14_predict_using_fitted_pipeline(self):
        print("Make predictions on best pipeline...")
        predictions = self.remote_auto_pipelines.predict(X=self.holdout_data.drop(['next_purchase'], axis=1).values[:5])
        print(predictions)
        self.assertGreater(len(predictions), 0)

    @print_test_separators
    def test_15_summary_listing_all_pipelines_from_wml(self):
        print("Getting pipelines summary...")
        pipelines_details = self.remote_auto_pipelines.summary()
        print(pipelines_details)

    @print_test_separators
    def test_16__get_data_connections__return_a_list_with_data_connections_with_optimizer_params(self):
        print("Getting all data connections...")
        data_connections = self.remote_auto_pipelines.get_data_connections()
        self.assertIsInstance(data_connections, list, msg="There should be a list container returned")
        self.assertIsInstance(data_connections[0], DataConnection,
                              msg="There should be a DataConnection object returned")

    @print_test_separators
    def test_17_get_pipeline_params_specific_pipeline_parameters(self):
        print("Getting details of Pipeline_1...")
        pipeline_params = self.remote_auto_pipelines.get_pipeline_details(pipeline_name='Pipeline_1')
        print(pipeline_params)

    @print_test_separators
    def test_18__get_pipeline_params__fetch_best_pipeline_parameters__parameters_fetched_as_dict(self):
        print("Getting details of the best pipeline...")
        best_pipeline_params = self.remote_auto_pipelines.get_pipeline_details()
        print(best_pipeline_params)

    ########
    # LALE #
    ########

    @print_test_separators
    def test_19__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        print("Download and load Pipeline_4 as lale...")
        TestOBMAndKB.lale_pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4')
        self.assertWarnsRegex(Warning, "OBM",
                              msg="Warning (OBM pipeline support only for inspection and deployment) was not raised")
        print(f"Fetched pipeline type: {type(self.lale_pipeline)}")

        self.assertIsInstance(self.lale_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")

    @print_test_separators
    def test_19b_get_all_pipelines_as_lale(self):
        print("Fetching all pipelines as lale...")
        summary = self.remote_auto_pipelines.summary()
        print(summary)
        failed_pipelines = []
        for pipeline_name in summary.reset_index()['Pipeline Name']:
            print(f"Getting pipeline: {pipeline_name}")
            lale_pipeline = None
            try:
                lale_pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name=pipeline_name)
                self.assertWarnsRegex(Warning, "OBM",
                                     msg="Warning (OBM pipeline support only for inspection and deployment) was not raised")
                self.assertIsInstance(lale_pipeline, TrainablePipeline)
                predictions = lale_pipeline.predict(X=self.holdout_data.drop(['next_purchase'], axis=1).values[:1])
                print(predictions)
                self.assertGreater(len(predictions), 0, msg=f"Returned prediction for {pipeline_name} are empty")
            except:
                print(f"Failure: {pipeline_name}")
                failed_pipelines.append(pipeline_name)
                traceback.print_exc()

            if not TestOBMAndKB.lale_pipeline:
                TestOBMAndKB.lale_pipeline = lale_pipeline
                print(f"{pipeline_name} loaded for next test cases")

        self.assertEqual(len(failed_pipelines), 0, msg=f"Some pipelines failed. Full list: {failed_pipelines}")

    @unittest.skip("Skipped lale pretty print")
    def test_20__pretty_print_lale__checks_if_generated_python_pipeline_code_is_correct(self):
        pipeline_code = self.lale_pipeline.pretty_print()
        try:
            exec(pipeline_code)

        except Exception as exception:
            self.assertIsNone(
                exception,
                msg=f"Pretty print from lale pipeline was not successful \n\n Full pipeline code:\n {pipeline_code}")

    @print_test_separators
    def test_20a_remove_last_freeze_trainable_prefix_returned(self):
        print("Prepare pipeline to refinery...")
        from lale.lib.sklearn import KNeighborsClassifier, DecisionTreeClassifier, LogisticRegression
        prefix = self.lale_pipeline.remove_last().freeze_trainable()
        self.assertIsInstance(prefix, TrainablePipeline,
                              msg="Prefix pipeline is not of TrainablePipeline instance.")
        TestOBMAndKB.new_pipeline = prefix >> (KNeighborsClassifier | DecisionTreeClassifier | LogisticRegression)

    @print_test_separators
    def test_20b_hyperopt_fit_new_pipepiline(self):
        print("Do a hyperparameters optimization...")
        hyperopt = Hyperopt(estimator=TestOBMAndKB.new_pipeline, cv=3, max_evals=2)
        try:
            TestOBMAndKB.hyperopt_pipelines = hyperopt.fit(self.holdout_data.drop(['next_purchase'], axis=1).values,
                                                           self.holdout_data['next_purchase'].values)
        except ValueError as e:
            print(f"ValueError message: {e}")
            traceback.print_exc()
            hyperopt_results = hyperopt._impl._trials.results
            print(hyperopt_results)
            self.assertIsNone(e, msg="hyperopt fit was not successful")

    @print_test_separators
    def test_20c_get_pipeline_from_hyperopt(self):
        print("Get locally optimized pipeline...")
        new_pipeline_model = TestOBMAndKB.hyperopt_pipelines.get_pipeline()
        self.assertWarnsRegex(Warning, "OBM",
                             msg="Warning (OBM pipeline support only for inspection and deployment) was not raised")
        print(f"Hyperopt_pipeline_model is type: {type(new_pipeline_model)}")
        TestOBMAndKB.new_sklearn_pipeline = new_pipeline_model.export_to_sklearn_pipeline()
        self.assertIsInstance(
            TestOBMAndKB.new_sklearn_pipeline,
            Pipeline,
            msg=f"Incorect Sklearn Pipeline type after conversion. Current: {type(TestOBMAndKB.new_sklearn_pipeline)}")

    @print_test_separators
    def test_21_predict_refined_pipeline(self):
        print("Make predictions on locally optimized pipeline...")
        predictions = TestOBMAndKB.new_sklearn_pipeline.predict(
            X=self.holdout_data.drop(['next_purchase'], axis=1).values[:1])
        print(predictions)
        self.assertGreater(len(predictions), 0, msg=f"Returned prediction for refined pipeline are empty")

    @print_test_separators
    def test_22_get_pipeline__load_specified_pipeline__pipeline_loaded(self):
        print("Loading pipeline as sklearn...")
        TestOBMAndKB.pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4',
                                                                        astype=self.experiment.PipelineTypes.SKLEARN)
        print(f"Fetched pipeline type: {type(self.pipeline)}")
        self.assertWarnsRegex(Warning, "OBM",
                             msg="Warning (OBM pipeline support only for inspection and deployment) was not raised")

        self.assertIsInstance(self.pipeline, Pipeline,
                              msg="Fetched pipeline is not of sklearn.Pipeline instance.")

    @print_test_separators
    def test_23_predict__do_the_predict_on_sklearn_pipeline__results_computed(self):
        print("Make predictions on sklearn pipeline...")
        predictions = self.pipeline.predict(self.holdout_data.drop(['next_purchase'], axis=1).values)
        print(predictions)

    @print_test_separators
    def test_24_get_historical_optimizer_with_data_join_graph(self):
        print("Fetching historical optimizer with OBM and KB...")
        TestOBMAndKB.historical_opt = self.experiment.runs.get_optimizer(
            run_id=self.remote_auto_pipelines._engine._current_run_id)
        # TestOBMAndKB.historical_opt = self.experiment.runs.get_optimizer(run_id='ead25ed8-0218-4d13-b6ad-c6218f910154')
        self.assertIsInstance(self.historical_opt.get_params()['data_join_graph'], DataJoinGraph,
                              msg="data_join_graph was incorrectly loaded")

        TestOBMAndKB.pipeline = self.historical_opt.get_pipeline()
        self.assertWarnsRegex(Warning, "OBM",
                             msg="Warning (OBM pipeline support only for inspection and deployment) was not raised")

    @print_test_separators
    def test_25_get_obm_training_data_from_historical_optimizer(self):
        print("Download historical preprocessed data from OBM stage...")
        train_data, holdout_data = (
            self.historical_opt.get_preprocessed_data_connection().read(with_holdout_split=True))

        print("OBM train data sample:")
        print(train_data.head())
        self.assertGreater(len(train_data), 0)
        print("OBM holdout data sample:")
        print(holdout_data.head())
        self.assertGreater(len(holdout_data), 0)

    #################################
    #      DEPLOYMENT SECTION       #
    #################################

    @print_test_separators
    def test_26_batch_deployment_setup_and_preparation(self):
        TestOBMAndKB.service = Batch(source_wml_credentials=self.wml_credentials.copy(),
                                     source_project_id=self.project_id,
                                     target_wml_credentials=self.wml_credentials.copy(),
                                     target_space_id=self.space_id)


    @print_test_separators
    def test_27_deploy__deploy_best_computed_pipeline_from_autoai_on_wml(self):
        self.service.create(
            experiment_run_id=self.remote_auto_pipelines._engine._current_run_id,
            model=self.pipeline_name,
            deployment_name=self.DEPLOYMENT_NAME)


    @print_test_separators
    def test_28_score_deployed_model(self):
        from ibm_watson_machine_learning.helpers.connections import DeploymentOutputAssetLocation
        if is_cp4d():
            scoring_params = self.service.run_job(
                payload=self.data_connections_space_only,
                output_data_reference=DataConnection(
                    location=DeploymentOutputAssetLocation(name='output')
                ),
                background_mode=False)

        else:
            scoring_params = self.service.run_job(
                payload=self.data_connections,
                output_data_reference=DataConnection(
                    connection=S3Connection(endpoint_url=self.cos_endpoint,
                                            access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                            secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                    location=S3Location(bucket=self.bucket_name,
                                        path="prediction_results.csv")
                ),
                background_mode=False)
        print(scoring_params)

    @print_test_separators
    def test_29_list_deployments(self):
        deployments = self.service.list()
        print(deployments)
        params = self.service.get_params()
        print(params)
        self.assertIsNotNone(params)

    @print_test_separators
    def test_30_delete_deployment(self):
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()
        self.wml_client.set.default_space(self.space_id) if not self.wml_client.default_space_id else None
        self.wml_client.repository.delete(self.service.asset_id)
        self.wml_client.set.default_project(self.project_id) if is_cp4d() else None

    #################################
    #      NOTEBOOK SECTION       #
    #################################

    @print_test_separators
    def test_31_prepare_notebook_cos_version(self):
        if is_cp4d():
            TestOBMAndKB.metadata = dict(
                training_data_reference=self.data_connections,
                training_result_reference=DataConnection(
                    location=FSLocation(
                        path=f'/projects/{self.project_id}/assets/auto_ml/auto_ml.92f52d47-8f51-4001-ae7b-87b4681ec066/wml_data/{self.run_id}/data/automl',
                    )),
                prediction_type='regression',
                prediction_column='next_purchase',
                holdout_size=0.1,
                scoring='neg_log_loss',
                max_number_of_estimators=1,
            )

            TestOBMAndKB.local_optimizer_cos = AutoAI(
                self.wml_credentials,
                project_id=self.project_id).runs.get_optimizer(metadata=self.metadata)

        else:
            TestOBMAndKB.metadata = dict(
                training_data_reference=self.data_connections,
                training_result_reference=DataConnection(
                    connection=S3Connection(endpoint_url=self.cos_endpoint,
                                            access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                            secret_access_key=self.cos_credentials['cos_hmac_keys'][
                                                'secret_access_key']),
                    location=S3Location(bucket=self.bucket_name,
                                        path=self.results_cos_path,
                                        model_location=self.model_location,
                                        training_status=self.training_status
                                        )
                ),
                prediction_type='regression',
                prediction_column='next_purchase',
                holdout_size=0.1,
                scoring='neg_log_loss',
                max_number_of_estimators=1,
            )

            print("HMAC: Initializing AutoAI local scenario with metadata...")

            TestOBMAndKB.local_optimizer_cos = AutoAI().runs.get_optimizer(
                metadata=self.metadata
            )

    # @print_test_separators
    # def test_32_data_join_graph_visualization_notebook(self):
    #     optimizer_params = self.local_optimizer_cos.get_params()
    #     data_join_graph = optimizer_params['data_join_graph']
    #     print("Visualizing data_join_graph...")
    #     data_join_graph.visualize()

    @print_test_separators
    def test_33_download_preprocessed_obm_training_data_notebook(self):
        print("Downloading OBM preprocessed training data with holdout split...")
        TestOBMAndKB.train_data, TestOBMAndKB.holdout_data = (
            self.local_optimizer_cos.get_preprocessed_data_connection().read(with_holdout_split=True))

        print("OBM train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("OBM holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    @print_test_separators
    def test_34_visualize_obm_pipeline_notebook(self):
        print("Visualizing OBM model ...")
        data_join_pipeline = self.local_optimizer_cos.get_preprocessing_pipeline()
        assert isinstance(data_join_pipeline._pipeline_json, list)
        assert '40 [label=NumberSet]' in data_join_pipeline._graph.__str__()

    #     data_join_pipeline.visualize()

    @print_test_separators
    def test_35_batch_deployment_setup_and_preparation_notebook(self):
        TestOBMAndKB.service = Batch(source_wml_credentials=self.wml_credentials.copy(),
                                     source_project_id=self.project_id,
                                     target_wml_credentials=self.wml_credentials.copy(),
                                     target_space_id=self.space_id)


    @print_test_separators
    def test_36__deploy__deploy_best_computed_pipeline_from_autoai_on_wml_notebook(self):
        self.service.create(
            metadata=self.metadata,
            model=self.pipeline_name,
            deployment_name=self.DEPLOYMENT_NAME)


    @print_test_separators
    def test_37a_score_deployed_model_notebook(self):
        from ibm_watson_machine_learning.helpers.connections import DeploymentOutputAssetLocation
        if is_cp4d():
            scoring_params = self.service.run_job(
                payload=self.data_connections_space_only,
                output_data_reference=DataConnection(
                    location=DeploymentOutputAssetLocation(name='output')
                ),
                background_mode=False)

        else:
            scoring_params = self.service.run_job(
                payload=self.data_connections,
                output_data_reference=DataConnection(
                    connection=S3Connection(endpoint_url=self.cos_endpoint,
                                            access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                            secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                    location=S3Location(bucket=self.bucket_name,
                                        path="prediction_results")
                ),
                background_mode=False)
        print(scoring_params)

        TestOBMAndKB.job_id = scoring_params['metadata']['id']

    @print_test_separators
    def test_37b_list_jobs_notebook(self):
        jobs = self.service.list_jobs()
        print(jobs)

    @print_test_separators
    def test_37c_rerun_job_notebook(self):
        scoring_params = self.service.rerun_job(self.job_id, background_mode=False)
        print(scoring_params)

    @print_test_separators
    def test_37d_get_job_result_notebook(self):
        result = self.service.get_job_result(self.job_id)
        print(result)

    @print_test_separators
    def test_38_list_deployments_notebook(self):
        deployments = self.service.list()
        print(deployments)
        params = self.service.get_params()
        print(params)
        self.assertIsNotNone(params)

    @print_test_separators
    def test_39_delete_deployment_notebook(self):
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()
        self.wml_client.set.default_space(self.space_id) if not self.wml_client.default_space_id else None
        self.wml_client.repository.delete(self.service.asset_id)
        self.wml_client.set.default_project(self.project_id) if is_cp4d() else None


if __name__ == '__main__':
    unittest.main()
