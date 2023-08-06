.. _quickstart:
========================================
Quickstart: Single Parameter Calibration
========================================

This is a minimal optimization task for a simple single parameter problem in a python script. Alternatively you can run the code will work an Jupyter Python Notebook.

Prerequisites
=============

* Access to an installed software instance with url i.e. 
    * https://www.qcalibrate.beta.optimal-control.net:31603 (external)
    * https://www.qcalibrate.staging.optimal-control.net:31603 (FZ Jülich network)
* LDAP account in the FZJ network or a GitHub account. To get the authorization please register yourself on `https://iffgit.fz-juelich.de/`_ using FZJ LDAP or GitHub.com account  
  and then contact :email:`Roman Razilov <r.razilov@fz-juelich.de>`.
* Python 3.8 or higher

Experiment Definition
=====================

* Open the web UI using one of the URLs 
* Login with credentials and consent access to basic profile data, the software:
    * process your name and (if available) avatar image to display logged in user information
    * process and store: your e-mail as primary owner identifier
* After the login you will see the starting page 

.. figure :: _static/quickstart-experiment-list.png
    
    * Home page: List of experiments * 

.. |add| image:: _static/add-icon.png
  :width: 16
  :height: 16

* Start by creating a new configuration by clicking on the |add| symbol.
* Select **Parameter Optimization** in pop-up menu
* Rename the first parameter from **param1** to **x**. 
  By default, the parameter domain is from 0.0 to 1.0 with an initial value of 0.5

    .. figure :: _static/quickstart-experiment-create.png

        * Experiment creation page * 

    .. |save| image:: _static/save-icon.png
        :width: 16
        :height: 16

* Click |save| to save the configuration

    .. figure :: _static/quickstart-experiment-saved.png   

        * Experiment creation page * 

Client Code
===========

* We recommend to use `virtual environment <https://docs.python.org/3/library/venv.html>`_ to avoid dependency conflicts
* Install qcalibrateremote library in your environment with **pip**.
    .. code-block:: console

        (.venv)$ pip install qcalibrateremote

* For *conda* environment install *grcpio* explicitly.
    .. code-block:: console

        (.venv)$ conda install grpcio 

* Create a client script:

    .. code-block:: python
        :name: qcalibrateremote-quickstart.py
        
        from typing import Dict

        from qcalibrateremote import EvaluateFigureOfMerit, FigureOfMerit, create_optimizer_client

        class QuickstartFom(EvaluateFigureOfMerit):

            def __init__(self, *args, **kwargs) -> None:
                super().__init__()

            def infidelity(self, x) -> float:
                return (x - 0.33)**2

            def evaluate(self, parameters: Dict[str, float], **kwargs) -> FigureOfMerit:
                """Abstract method for figure of merit evaluation"""
                return FigureOfMerit(self.infidelity(**parameters), '')

        experiment_id="0x..."
        token=("ey...")

        optimizer_client = create_optimizer_client(
            host="grpc.qcalibrate.staging.optimal-control.net", port=31603, token=token)

        optimization_result = optimizer_client.run(
            experiment_id=experiment_id, evaluate_fom_class=QuickstartFom)

        print(optimization_result.top[0].parameters["x"])

.. |key| image:: _static/key-icon.png
  :width: 17
  :height: 16

* get experiment_id and create an access token by click on the |key| icon

    .. figure :: _static/quickstart-experiment-key.png

        * Experiment creation page *

* paste the experiment_id and token to your script

Optimization
============

* run the script

* while the optimization run you can observe the progress by selecting the last run of your experiment

Results
=======

* The :meth:`qcalibrateremote.QOptimizerClient.run` method returns a :class:`qcalibrateremote.OptimizationResultCollector` object,
  containing initial parameters and configuration, all iterations and the iteration with best (lowest) figure-of-merit value 
  (:attr:`qcalibrateremote.OptimizationResultCollector.top`).

.. raw:: latex

    \clearpage