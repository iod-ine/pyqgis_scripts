""" A collection of functions to extract WKT from selected features. """

from qgis.core import Qgis, QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.utils import iface


def get_wkt_of_selected_feature(precision=4):
    """ Returns the WKT of the first selected polygon in WGS84. """

    # grab the active layer and the list of selected features in this layer
    active_layer = iface.activeLayer()
    selected_features = active_layer.selectedFeatures()

    # if none are selected, show a message and return
    if len(selected_features) == 0:
        iface.messageBar().pushMessage('Error', 'No features selected', level=Qgis.Critical, duration=3)
        return

    # if there are selected features, grab the first and extract the geometry
    selected_feature = selected_features[0]
    geometry = selected_feature.geometry()

    # reproject to WGS84 if active layer has a different CRS
    source_crs = active_layer.crs()
    if source_crs.authid() != 'EPSG:4326':
        project = QgsProject.instance()  # the QgsCoordinateTransform needs the project for some reason
        target_crs = QgsCoordinateReferenceSystem('EPSG:4326')
        transform = QgsCoordinateTransform(source_crs, target_crs, project)

        geometry.transform(transform)

    return geometry.asWkt(precision=precision)
