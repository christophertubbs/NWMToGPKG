import json
import typing

from datetime import datetime, timedelta


class GeometryConfiguration(object):
    """
    Configuration detailing where to get data that will dictate what the points
    in the national water model data mean and how to interpret that dataset
    """
    def __init__(self, path: str, input_format: str, feature_id_field: str):
        self.path = path
        """(:class:`str`) Where to find the geometry dataset"""

        self.input_format = input_format
        """(:class:`str`) The file format for the data (geojson, shapefile, netcdf, etc)"""

        self.feature_id_field = feature_id_field
        """(:class:`str`) The field within the dataset that corresponds to the `feature_id` field within the NWM"""


class DataConstraintConfiguration(object):
    """
    Configuration detailing the limits as to what data should be used
    """
    def __init__(self, constraint_configuration: dict):
        """
        Constructor

        :param constraint_configuration: JSON configuration detailing the configuration of constraints
        """
        self.absolute_minimum_issuance: typing.Union[None, datetime] = None
        """(:class:`datetime`) The earliest forecast or simulation to consider in absolute time"""

        self.absolute_maximum_issuance: typing.Union[None, datetime] = None
        """(:class:`datetime`) The latest forecast or simulation to consider in absolute time"""

        self.relative_minimum_issuance: typing.Union[None, timedelta] = None
        """(:class:`timedelta`) The earliest forecast or simulation to consider in an amount of time relative to now"""

        self.relative_maximum_issuance: typing.Union[None, timedelta] = None
        """(:class:`timedelta`) The latest forecast or simulation to consider in an amount of time relative to now"""

        # TODO: Interpret issuance restrictions by correctly converting date strings to dates and
        #       duration strings to time deltas


class DataConfiguration(object):
    """
    Configuration detailing where to get the input national water model data and what limits to place upon it
    """
    def __init__(self, data_configuration: dict):
        """
        Constructor

        :param data_configuration: JSON configuration detailing what data to use as the input for the conversion
        """
        self.data_address = data_configuration['address']
        """(:class:`str`) Where the root of the input data is"""

        self.model_configuration = data_configuration['model_configuration']
        """(:class:`str`) What configuration of data to use (`short_range`, `analysis_assim`, etc)"""

        self.model = data_configuration['model']
        """(:class:`str`) What type of model data to use (channel_rt, land, reservoir, etc)"""

        self.constraints = DataConstraintConfiguration(data_configuration.get("constraints"))
        """(:class:`DataConstraintConfiguration`) Limitations on what data to convert"""


class ConversionConfiguration(object):
    """
    Configuration needed to perform the overall conversion from netcdf to geopackage
    """
    def __init__(self, configuration_path: str):
        """
        Constructor

        :param configuration_path: The path to the configuration file 
        """
        with open(configuration_path, 'r') as configuration_file:
            self.configuration = json.load(configuration_file)

        self.geometry = GeometryConfiguration(**self.configuration['geometry'])
        """(:class:`GeometryConfiguration`) Details on how to correlate NWM data to geographic data"""

        self.input = DataConfiguration(self.configuration['input'])
        """(:class:`DataConfiguration`) Details on what data to convert"""

        self.output_path = self.configuration['output_path']
        """(:class:`str`) Where to put the converted data"""
