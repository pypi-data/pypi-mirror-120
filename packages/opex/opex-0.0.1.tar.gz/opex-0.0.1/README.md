# objdet-predictions-exchange-format
Exchange format for predictions from object detection algorithms (JSON).

## JSON

```json
{
  "timestamp": "%Y%m%d_%H%M%S.%f",
  "id": "str",
  "objects": [
    {
      "score": 1.0,
      "label": "object",
      "bbox": {
        "top": 100,
        "left": 100,
        "bottom": 200,
        "right": 200
      },
      "polygon": {
        "points": [
          [100, 100],
          [200, 200],
          [100, 200]
        ]
      }
    }
  ],
  "meta": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**Notes:**

The following keys are optional: 

* timestamp
* meta
* score 


## Reading/Writing

To read a prediction:

```python
from opex import ObjectPredictions

# From a string
predictions = ObjectPredictions.from_json_string("{...}")

# From a named file
predictions = ObjectPredictions.load_json_from_file("predictions.json")

# From an open stream
with open("predictions.json", "r") as stream:
    predictions = ObjectPredictions.read_json_from_stream(stream)
```

To write a prediction:

```python
from opex import ObjectPredictions

predictions: ObjectPredictions = ...

# Serialise the object to a JSON-formatted string
print(predictions.to_json_string())
print(predictions.to_json_string(indent=2))

# Write the object to a file
predictions.save_json_to_file("predictions.json", indent=2)

# Write to an open stream
with open("predictions.json", "w") as stream:
    predictions.write_json_to_stream(stream, indent=2)
```
