# Databricks notebook source
# %% Select test/train data

import numpy as np
import pandas as pd
from azureml.core.model import Model
from azureml.core import Run
from forecastlib.training.ForecastTrainer import ForecastTrainer

pd.set_option('display.max_columns', None)

# %%


class TrainingRunner(object):
    def __init__(self, file_name, prepare_dataset_delegate, features, args=None):
        run = Run.get_context()
        ws = run.experiment.workspace
        ds = ws.get_default_datastore()

        ds.download(target_path="./", prefix=file_name, overwrite=True, show_progress=True)

        blob_data = pd.read_csv(file_name, delimiter=",")

        blob_data.describe(include='all')

        self.train_data, self.test_data = prepare_dataset_delegate(blob_data)
        self.features = features
        self.args = args

    def parse_args(self):
        import argparse
        print("Parsing parameters")

        parser = argparse.ArgumentParser()

        parser.add_argument('--batch_size', type=int, dest='batch_size', default=1000, help='batch size for training')

        parser.add_argument('--epochs', type=int, dest='epochs', default=13, help='number of epochs')

        parser.add_argument('--layers', type=int, dest='layers', default=1, help='number of hidden layers')

        parser.add_argument('--nodes', type=int, dest='nodes', default=50, help='number of nodes in one hidden layer')

        parser.add_argument('--dropout', type=float, dest='dropout', default=0.5, help='dropout in hidden layers')

        parser.add_argument('--features', type=int, dest='features', default=0, help='features set')

        parser.add_argument('--modelname', type=str, dest='modelname', default="high_sell_known",
                            help='name of the model found in MLservice => Models')

        # parser.add_argument('--learning-rate', type=float, dest='learning_rate', default=0.001, help='learning rate')

        self.args = parser.parse_args()

        print('Running with batch size:', self.args.batch_size)
        print('Running with epochs:', self.args.epochs)
        print('Running with hidden layers:', self.args.layers)
        print('Running with hidden nodes:', self.args.nodes)
        print('Running with dropout:', self.args.dropout)
        print('Running with feature set:', self.args.features)
        print('Running with modelname:', self.args.modelname)

        return self.args

    # COMMAND ----------

    def run(self):
        accuracy_sampling = 1

        if self.args is None:
            self.parse_args()

        # start an Azure ML run
        run = Run.get_context()

        trainer = ForecastTrainer(
            run.id,
            self.args.batch_size,
            self.args.epochs,
            self.args.nodes,
            self.test_data,
            self.train_data,
            accuracy_sampling,
            self.features,
            self.args.dropout,
            self.args.layers)

        run.log("epochs", self.args.epochs)
        run.log("batch_size", self.args.batch_size)
        run.log("nodes", self.args.nodes)
        run.log("layers", self.args.layers)
        run.log("dropout", self.args.dropout)
        run.log("feature_set", self.args.features)
        run.log("features_num", len(self.features))
        run.log("modelname", self.args.modelname)

        lossesIn, accuraciesIn = trainer.train()

        acc = trainer.get_accuracy()

        # log a single value
        run.log("Accuracy:", acc)
        print('Accuracy log:', acc)

        print("Inliner acc: ", accuraciesIn)

        # COMMAND ----------

        model = trainer.get_best_model()
        path = "./outputs/" + run.id + "/"
        model.save(path)

        if self.args.modelname is not None:
            Model.register(
                workspace=run.experiment.workspace,
                model_name=self.args.modelname,
                model_path=path,
                properties={"Accuracy": trainer.get_accuracy(), "ModelFit": trainer.get_model_fit()},
                description="Accuracy: {:.2f} | ModelFit: {:.2f}".format(trainer.get_accuracy(), trainer.get_model_fit())
            )
            print("Model {0} successfully registered to experiment".format(self.args.modelname))
        run.complete()
