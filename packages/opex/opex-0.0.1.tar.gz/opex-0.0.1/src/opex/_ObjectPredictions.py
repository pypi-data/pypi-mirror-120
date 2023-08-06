from typing import Dict, List

from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import StringProperty, ArrayProperty, MapProperty

from ._ObjectPrediction import ObjectPrediction


class ObjectPredictions(StrictJSONObject['ObjectPredictions']):
    """
    A collection of object predictions.
    """
    # The time at which the picture was taken
    timestamp: OptionallyPresent[str] = StringProperty(format="date-time", optional=True)

    # The camera that took the picture
    id: str = StringProperty()

    # The object predictions
    objects: List[ObjectPrediction] = ArrayProperty(
        element_property=ObjectPrediction.as_property()
    )

    # Any meta-data
    meta: OptionallyPresent[Dict[str, str]] = MapProperty(
        value_property=StringProperty(),
        optional=True
    )

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "timestamp=%s, id=%s, #objects=%d" % (self.timestamp, self.id, len(self.objects))
