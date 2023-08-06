# Django Elastic Filter

## Install:
`pip install django_elastic_filter` 

## Usage:
```python
# import package
from django_elastic_filter.elastic_filter import ElasticFilter
from django_elastic_filter.dynamic import generate_serializer

elastic_filter = ElasticFilter('fields', 'user_id', request)
elastic_filter_fields = elastic_filter.get_scope_other_fields()
elastic_serializer = generate_serializer(Stockholder,
                                         elastic_filter_fields['fields'],
                                         elastic_filter_fields['rest'],
                                         request,
                                         {
                                             'info': 'users.models.Natural',
                                         })
serializer = elastic_serializer(stockholders, many=True)
```