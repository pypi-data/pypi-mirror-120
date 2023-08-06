Base Case
==========

This is the base case that will be created if no specific template is selected. It serves as a foundation for own modeling and to get an overview for the program.

To initialize the base case and create a project folder, no template needs to be specified:

.. code-block:: bash

    $ emobpy create -n <give a name>

.. warning::
    Before running this example, install and activate an emobpy dedicated environment (conda recommended).

After initialisation, run the script in the following order:

.. code-block:: bash

    $ cd <given name>
    $ python Mobility.py
    $ python DrivingConsumption.py
    $ python GridAvailability.py
    $ python GridDemand.py


The initialisation creates a folder and file structure as follows:

.. code-block:: bash

    ├── my_evs
    │   └── config_files
    │       ├── DepartureDestinationTrip_Free.csv
    │       ├── DepartureDestinationTrip_Worker.csv
    │       ├── DistanceDurationTrip.csv
    │       ├── rules.yml
    │       ├── TripsPerDay.csv
    │   ├── DrivingConsumption.py
    │   ├── GridAvailability.py
    │   ├── GridDemand.py
    │   ├── Instructions.rst
    │   ├── Mobility.py
    │   ├── Visualize_and_Export.ipynb

The base case consists of four `.py` files that run the modelling, a `.ipynb` to visualise the results and the `config_files` folder to make configurations.

+---------------------------------+-----------------------------------------------------------------------------------+
| File name                       |  Description                                                                      |
+=================================+===================================================================================+
|``config_files/``                | The configurations can be changed in this folder.                                 |
+---------------------------------+-----------------------------------------------------------------------------------+
|``Mobility.py``                  | Uses :meth:`emobpy.Mobility` to create individual driver time series with         |
|                                 | vehicle location and distance travelled.                                          |
+---------------------------------+-----------------------------------------------------------------------------------+
|``DrivingConsumption.py``        | Uses :meth:`emobpy.Consumption` to assign vehicles and model their consumption.   |
+---------------------------------+-----------------------------------------------------------------------------------+
|``GridAvailability.py``          | Uses :meth:`emobpy.Availability` to create the grid availability time series.     |
+---------------------------------+-----------------------------------------------------------------------------------+
|``GridDemand.py``                | Uses :meth:`emobpy.Charging` to calculate the load profile.                       |
+---------------------------------+-----------------------------------------------------------------------------------+
|``Visualize_and_export.ipynb``   | Jupyter Notebook File to view the results. See Visualization.                     |
+---------------------------------+-----------------------------------------------------------------------------------+

In the default configuration the following profiles are created:

    - 6 mobility profiles
    - 1 consumption profiles
    - 1 grid availability profiles
    - 4 grid demand profiles

The results are saved as pickle files. To read them, they must first be de-serialised. More information can be found in the `pickle documentation <https://docs.python.org/3/library/pickle.html#module-pickle>`_. One option to do this is the following:

.. code-block:: python

    pickle_in = open("data.pickle","rb")
    data = pickle.load(pickle_in)

A `.ipynb` file is created for visualisation. This could look like this, for example:

.. include:: ../../docs/examples/basecase/Visualize_and_Export.html
