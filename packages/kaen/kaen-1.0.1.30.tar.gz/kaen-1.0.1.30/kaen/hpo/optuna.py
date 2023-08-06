import os
import time

import optuna
from optuna.samplers import TPESampler
from optuna.trial import TrialState

import argparse

import mlflow
from mlflow import ActiveRun
from mlflow.entities import RunStatus
from mlflow.tracking import MlflowClient

import numpy as np

from kaen.hpo.mlflow_utils import get_parent_run, get_active_child_run, make_feature_set_ids, get_client, get_existing_run

from kaen.hpo.mlflow import BaseMLFlowService

class BaseOptunaService(BaseMLFlowService):
  def on_experiment_start(self, experiment, parent_run):
    seed = super().seed
    experiment_name = super().mlflow_experiment_name    

    #create the hyperparameter study
    self._study = optuna.create_study( study_name = experiment_name,
      pruner = optuna.pruners.SuccessiveHalvingPruner(),
      sampler = TPESampler( seed = seed) )

  def on_run_create(self, run):
    self._trial = self._study.ask()
    super().mlflow_client.set_tag(run.info.run_id,
      "optuna.trial_number", self._trial.number)

  def on_run_update(self, run, idx):
    trial = self._trial

    loss = run.data.metrics['loss'] if 'loss' in run.data.metrics else None
    step = run.data.metrics['step'] if 'step' in run.data.metrics else None

    if loss and step:
      trial.report(loss, step)
      if trial.should_prune():
          print(f"{run.info.run_id}: pruning...")        
          super().mlflow_client.set_terminated(run.info.run_id, status = 'KILLED')

  def on_run_end(self, run):
    if 'loss' in run.data.metrics:
      self._study.tell(self._trial, run.data.metrics['loss'])
    else:
      self._study.tell(self._trial, None, state = TrialState.FAIL)


class XorExperimentService(BaseOptunaService):
  def hparams(self):
    trial = self._trial

    #define hyperparameters
    return {
      "seed": trial.suggest_int('seed', 0, np.iinfo(np.int32).max - 1),
        
      "bins": trial.suggest_categorical('bins', [32, 48, 64, 96, 128]),
        
      "optimizer": trial.suggest_categorical('optimizer', ['SGD', 'Adam']),
        
      "lr": trial.suggest_loguniform('lr', 89e-3, 91e-3),
        
      "num_hidden_neurons": [trial.suggest_int(f"num_hidden_layer_{layer}_neurons", 5, 17) \
                                for layer in range(trial.suggest_int('num_layers', 1, 2))],
      
      "batch_size": trial.suggest_categorical('batch_size', [32, 64, 128]),
        
      "max_epochs": trial.suggest_int('max_epochs', 100, 400, log = True)
    }

  def hparams_set_id(self):
    #specify the subsets of hyperparameter name/values to id
    return {
        "hp_bin_id": 'bins'
    }    

  def on_experiment_end(self, experiment, parent_run):
    study = self._study
    try:
      for key, fig in {
        "plot_param_importances": optuna.visualization.plot_param_importances(study),
        "plot_parallel_coordinate": optuna.visualization.plot_parallel_coordinate(study, params=["max_epochs", "num_hidden_layer_0_neurons"]),
        "plot_parallel_coordinate_max_epochs_lr": optuna.visualization.plot_parallel_coordinate(study, params=["max_epochs", "lr"]),
        "plot_parallel_coordinate_lr_layer_0": optuna.visualization.plot_parallel_coordinate(study, params=["lr", "num_hidden_layer_0_neurons"]),
        "plot_contour": optuna.visualization.plot_contour(study, params=["max_epochs", "num_hidden_layer_0_neurons"]),
        "plot_contour_max_epochs_lr": optuna.visualization.plot_contour(study, params=["max_epochs", "lr"]),
      }.items():
        fig.write_image(key + ".png")
        self.mlflow_client.log_artifact(run_id = parent_run.info.run_id, 
                            local_path = key + ".png")
    except:
      print(f"Failed to correctly persist experiment visualization artifacts")
              
    #log the dataframe with the study summary  
    study.trials_dataframe().describe().to_html(experiment.name + ".html")  
    self.mlflow_client.log_artifact(run_id = parent_run.info.run_id, 
                        local_path = experiment.name + ".html")
          
    #log the best hyperparameters in the parent run
    self.mlflow_client.log_metric(parent_run.info.run_id, "loss", study.best_value)
    for k, v in study.best_params.items():
      self.mlflow_client.log_param(parent_run.info.run_id, k, v)

    print('Best trial: {} value: {} params: {}\n'.format(study.best_trial, study.best_value, study.best_params))    