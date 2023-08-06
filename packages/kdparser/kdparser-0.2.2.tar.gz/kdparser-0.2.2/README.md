# KD_Parser
**kd_parser** is a simple and elegant python library. \
This library allows you easily parse data types such as `json` or `xml`.


## Installing kd_parser
```console
$ python -m pip install kd_parser
```

## Usage

### Parsing json objects

```python
from kdparser import jsonParser
```
##### Parsing a json object by `keys`
```python
parsed_json = parse_json_by_keys(json_to_parse, ['key_one', 'key_two'], is_recursive)
```
##### Parsing a json object by `values`
```python
parsed_json = parse_json_by_value(json_to_parse, ['value_one', 'value_two'], is_recursive)
```
##### Parsing a json object by `values types`
```python
parsed_json = parse_json_by_value_types(json_to_parse, ['int', 'str'], is_recursive)
```

### Parsing xml objects

```python
from kdparser import xmlParser
```
##### Parsing an xml object by `tags`
```python
parsed_xml = xmlParser.parse_xml_by_tags(xml_root_object, ['tag_one', 'tag_two'], isRecursive)
```
##### Parsing an xml object by `attribute`
```python
parsed_xml = xmlParser.parse_xml_by_attribute(xml_root_object, ['attribute'], isRecursive)
```
##### Parsing an xml object by `attributes values`
```python
parsed_xml = xmlParser.parse_xml_by_attributes_values(xml_root_object, ['attribute_value1, attribute_value2'], isRecursive)
```
##### Parsing an xml object by `tag values`
```python
parsed_xml = xmlParser.parse_xml_by_values(xml_root_object, ['value_one, value_two'], isRecursive)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate :laughing:
## Authors
- Kobi Shabaton - @kobis2113
- Dor Dvir-Raviv - @dor1402
