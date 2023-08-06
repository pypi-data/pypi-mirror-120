"""
Location classe
"""
# Standard library modules
import warnings
import numpy as np
import logging

# Non-standard modules
from obspy.core.util.obspy_types import FloatWithUncertaintiesFixedUnit
from obspy.core.inventory.util import (Latitude, Longitude)
from obspy.geodetics.base import kilometers2degrees


warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Location(object):
    """
    Location class.

    Attributes:
        latitude (float): station latitude (degrees N)
        longitude (float): station longitude (degrees E)
        elevation (float): station elevation (meters above sea level)
        uncertainties_m (dict): 'lat', 'lon', 'elev' in METERS
        geology (str): site geology
        vault (str): vault type
        depth_m (float): depth of station beneath surface (meters)
        localisation_method (str): method used to determine position
        obspy_latitude: latitude as an *obspy* object
        obspy_longitude: longitude as an *obspy* object

    """

    def __init__(self, attributes_dict):
        """
        Create Location object and assign attributes from attributes_dict.
        Validate required location attributes exist
        Convert to obspy longitude and latitude

        :param attributes_dict: location information
        :type attributes_dict: dict or object of :class:`ObsMetadata`
        """
        position = attributes_dict.get('position', None)
        base = attributes_dict.get('base', None)

        if not base:
            msg = 'No base in location'
            warnings.warn(msg)
            logger.error(msg)
            raise TypeError(msg)
        if not position:
            msg = 'No position in location'
            warnings.warn(msg)
            logger.error(msg)
            raise TypeError(msg)

        self.latitude = position.get('lat', None)
        self.longitude = position.get('lon', None)
        self.elevation = position.get('elev', None)
        self.uncertainties_m = base.get('uncertainties.m', None)
        self.geology = base.get('geology', None)
        self.vault = base.get('vault', None)
        self.depth_m = base.get('depth.m', None)
        self.localisation_method = base.get('localisation_method', None)
        #self.obspy_latitude, self.obspy_longitude = \
        #    self.get_obspy_latitude_and_longitude()

    def __repr__(self):
        s = f'Location({self.latitude:g}, {self.longitude:g}, '
        s += f'{self.elevation:g}, {self.uncertainties_m}'
        if not self.geology == 'unknown':
            s += f', "geology: {self.geology}"'
        if self.vault:
            s += f', vault="{self.vault}"'
        if self.depth_m is not None:
            s += f', depth_m={self.depth_m:g}'
        if self.localisation_method:
            s += f', localisation_method="{self.localisation_method}"'
        s += ')'
        return s

    @property
    def obspy_elevation(self):
        """
        Returns elevation as obspy FloatWithUncertaintiesFixedUnit object
        """
        return FloatWithUncertaintiesFixedUnit(
            value=self.elevation,
            lower_uncertainty=self.uncertainties_m.get('elev',None),
            upper_uncertainty=self.uncertainties_m.get('elev',None),
            measurement_method=self.localisation_method)

    @property
    def obspy_latitude(self):
        """
        Returns obspy Latitude object
        """
        uncert_m = self.uncertainties_m.get('lat', None) if self.uncertainties_m else None
        if uncert_m is None:
            uncertainty_lat = None
        else:
            uncertainty_lat = kilometers2degrees(uncert_m / 1000)
            # Round uncertainties to ~ 4 signif digits
            uncertainty_lat = round(uncertainty_lat, -int(np.log10(uncertainty_lat))+4)
        return Latitude(value=self.latitude,
                        lower_uncertainty=uncertainty_lat,
                        upper_uncertainty=uncertainty_lat)  # ,
                        # measurement_method=self.localisation_method)

    @property
    def obspy_longitude(self):
        """
        Returns obspy Longitude object
        """

        uncert_m = self.uncertainties_m.get('lon', None) if self.uncertainties_m else None
        if uncert_m is None or abs(self.latitude) == 90:
            uncertainty_lon = None
        else:
            # lon is along parallel, not a great circle, so we must reduce by
            # cosine.
            uncertainty_lon = kilometers2degrees(
                (uncert_m / 1000) * np.cos(self.latitude))
            # Round uncertainties to ~ 4 signif digits
            uncertainty_lon = round(uncertainty_lon, -int(np.log10(uncertainty_lon))+4)
        return Longitude(value=self.longitude,
                         lower_uncertainty=uncertainty_lon,
                         upper_uncertainty=uncertainty_lon)  # ,
                         # measurement_method=self.localisation_method)

    @staticmethod
    def get_location_from_code(locations, code, type, label):
        """
        Obtain from the locations dictionary one location by code (key).
        Raise exception if not found
        """
        if not locations:
            msg = 'No locations specified in station'
            warnings.warn(msg)
            logger.error(msg)
            raise TypeError(msg)

        loc = locations.get(code, None)

        if not loc:
            if type == 'station':  # station location code is mandatory
                msg = f'Location "{code}" not found in station {label}'
                warnings.warn(msg)
                logger.error(msg)
                raise TypeError(msg)
            else:
                msg = f'Channel {label} has no location code. Assuming '\
                      'location code "00"'
                warnings.warn(msg)
                logger.warning(msg)

                loc = locations.get("00", None)
                if not loc:
                    msg = f'Location "{code}" not found in channel {label}'
                    warnings.warn(msg)
                    logger.error(msg)
                    raise TypeError(msg)
        return loc


    # def get_obspy_latitude_and_longitude(self, location=None):
    #     """
    #     Returns obspy Latitude and Longitude objects
# 
    #     Returns:
    #         (tuple):
    #              (:class:`Latitude`)
    #              (:class:`Longitude`)
    #     """
# 
    #     if not location:
    #         location = self
# 
    #     # Convert meters to kilometers and then to degrees.
    #     # This is along a meridian, so it's a great circle, Assumes
    #     # 40000 km Earth diameter
    #     uncertainty_lat = kilometers2degrees(
    #         location.uncertainties_m.get('lat', 0) / 1000
    #         if location.uncertainties_m else 0)
    #     # print(f'{-int(np.log10(uncertainty_lat))+3=}')
    #     # Round uncertainties to ~ 4 signif digits
    #     uncertainty_lat = round(uncertainty_lat, -int(np.log10(uncertainty_lat))+4)
    #     latitude = Latitude(value=location.latitude,
    #                         lower_uncertainty=uncertainty_lat,
    #                         upper_uncertainty=uncertainty_lat,
    #                         datum=None)
# 
    #     intermediate_uncert_lon = location.uncertainties_m.get(
    #         'lon', 0) / 1000 if location.uncertainties_m else 0
    #     # lon is along parallel, not a great circle, so we must reduce by
    #     # cosine.. Using numpy
    #     # Won't work for poles, make uncertainty zero in that case
    #     uncertainty_lon = kilometers2degrees(
    #         intermediate_uncert_lon * np.cos(latitude)) \
    #         if latitude != 90 else 0
# 
    #     # Round uncertainties to ~ 4 signif digits
    #     uncertainty_lon = round(uncertainty_lon, -int(np.log10(uncertainty_lon))+4)
    #     longitude = Longitude(value=self.longitude,
    #                           lower_uncertainty=uncertainty_lon,
    #                           upper_uncertainty=uncertainty_lon,
    #                           datum=None)
    #     return (latitude, longitude)
