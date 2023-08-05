import datetime
import decimal
import json
from copy import deepcopy

import pytz
import redis

from .utils import check_types, get_ids_from_untyped_data, check_callable


### FIELDS ###


class RedisField:
    
    def __init__(self, default=None, choices=None, null=True):
        default = check_callable(default)
        choices = check_callable(choices)
        null = check_callable(null)
        check_types(choices, dict)
        check_types(null, bool)
        self.default = default
        self.value = None
        self.choices = choices
        self.null = null
    
    def _get_default_value(self):
        self.value = check_callable(self.default)
        return self.value
    
    def _check_choices(self, value):
        if self.choices:
            if value not in self.choices.keys():
                raise Exception(f'{value} is not allowed. Allowed values: {", ".join(list(self.choices.keys()))}')
    
    def check_value(self):
        if self.value is None:
            self.value = self._get_default_value()
        if self.value is None:
            if self.null:
                self.value = 'null'
            else:
                raise Exception('null is not allowed')
        if self.value:
            self._check_choices(self.value)
        return self.value
    
    def clean(self):
        self.value = self.check_value()
        return self.value
    
    def deserialize_value_check_null(self, value, redis_root):
        if value == 'null':
            if not self.null:
                if redis_root.ignore_deserialization_errors:
                    print(
                        f'{datetime.datetime.now()} - {value} can not be deserialized like {self.__class__.__name__}, ignoring')
                else:
                    raise Exception(f'{value} can not be deserialized like {self.__class__.__name__}')
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        return value
    

class RedisString(RedisField):
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            self.value = f'{self.value}'
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = f'{value}'
        else:
            value = None
        return value


class RedisNumber(RedisField):
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, (int, float))
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            if type(value) == str:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            else:
                check_types(value, (int, float))
        else:
            value = None
        return value


class RedisId(RedisNumber):
    
    def __init__(self, *args, **kwargs):
        kwargs['null'] = False
        super().__init__(*args, **kwargs)


class RedisBool(RedisNumber):
    
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = {True: 'Yes', False: 'No'}
        super().__init__(*args, **kwargs)
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, bool)
            self.value = int(self.value)
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            check_types(value, int)
            value = bool(value)
        return value


class RedisDecimal(RedisString):
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, (int, float, decimal.Decimal))
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = decimal.Decimal(value)
        else:
            value = None
        return value


class RedisJson(RedisField):
    
    def __init__(self, json_allowed_types=(list, dict), *args, **kwargs):
        self.json_allowed_types = json_allowed_types
        super().__init__(*args, **kwargs)
    
    def set_json_allowed_types(self, allowed_types):
        self.json_allowed_types = allowed_types
        return self.json_allowed_types
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, self.json_allowed_types)
            json_string = json.dumps(self.value)
            self.value = json_string
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            check_types(value, str)
            value = json.loads(value)
            check_types(value, self.json_allowed_types)
        else:
            value = None
        return value


class RedisDict(RedisJson):
    
    def clean(self):
        self.set_json_allowed_types(dict)
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.set_json_allowed_types(dict)
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = super().deserialize_value(value, redis_root)
        else:
            value = None
        return value


class RedisList(RedisJson):
    
    def clean(self):
        self.set_json_allowed_types(list)
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.set_json_allowed_types(list)
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = super().deserialize_value(value, redis_root)
        else:
            value = None
        return value


class RedisDateTime(RedisString):
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, datetime.datetime)
            string_datetime = self.value.replace(tzinfo=pytz.UTC).strftime('%Y.%m.%d-%H:%M:%S+%Z')
            self.value = string_datetime
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = super().deserialize_value(value, redis_root)
            check_types(value, str)
            value = datetime.datetime.strptime(value, '%Y.%m.%d-%H:%M:%S+%Z').replace(tzinfo=pytz.UTC)
        else:
            value = None
        return value


class RedisDate(RedisString):
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            check_types(self.value, datetime.date)
            string_date = self.value.strftime('%Y.%m.%d+%Z')
            self.value = string_date
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = super().deserialize_value(value, redis_root)
            check_types(value, str)
            value = datetime.datetime.strptime(value, '%Y.%m.%d+%Z').date()
        else:
            value = None
        return value


class RedisForeignKey(RedisNumber):
    
    def __init__(self, model=None, *args, **kwargs):
        model = check_callable(model)
        if args:
            args = list(map(check_callable, *args))
        allowed = True
        if model is None:
            allowed = False
        elif not issubclass(model, RedisModel):
            allowed = False
        if not allowed:
            raise Exception(f'{model.__name__} class is not RedisModel')
        else:
            self.model = model
            super().__init__(*args, **kwargs)
    
    def _get_id_from_instance_dict(self):
        if self.value:
            if type(self.value) == dict:
                if 'id' in self.value.keys():
                    self.value = self.value['id']
                else:
                    raise Exception(
                        f"{self.value} has no key 'id', please provide serialized instance or dict like " + "{'id': 1, ...}")
            else:
                raise Exception(
                    f'{self.value} type is not dict, please provide serialized instance or dict like ' + "{'id': 1, ...}")
        return self.value
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            self.value = get_ids_from_untyped_data(self.value)[0]
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            check_types(value, int)
            model_name = self.model.__name__
            instance_id = value
            instance_qs = redis_root._get_instances_by_key(f'{redis_root.prefix}:{model_name}:{instance_id}')
            if instance_id in instance_qs.keys():
                value = instance_qs[instance_id]
            else:
                value = {'id': value}
        else:
            value = None
        return value


class RedisManyToMany(RedisList):
    
    def __init__(self, model=None, *args, **kwargs):
        model = check_callable(model)
        if args:
            args = list(map(check_callable, *args))
        allowed = True
        if model is None:
            allowed = False
        elif not issubclass(model, RedisModel):
            allowed = False
        if not allowed:
            raise Exception(f'{model.__name__} class is not RedisModel')
        else:
            self.model = model
            super().__init__(*args, **kwargs)
    
    def clean(self):
        self.value = self.check_value()
        if self.value not in [None, 'null']:
            self.value = get_ids_from_untyped_data(self.value)
        return super().clean()
    
    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value not in ['null', None]:
            value = super().deserialize_value(value, redis_root)
            model_name = self.model.__name__
            isntances_ids = value
            instances_list = []
            for instance_id in isntances_ids:
                instances = redis_root._get_instances_by_key(f'{redis_root.prefix}:{model_name}:{instance_id}')
                if len(instances.keys()):
                    instance = instances[instance_id]
                    instances_list.append(instance)
            value = instances_list
        
        return value


### REDIS ROOT ###


class RedisRoot:
    
    def __init__(
        self,
        connection_pool=None,
        prefix='redis_test',
        ignore_deserialization_errors=True,
        save_consistency=False,
        economy=False,
        use_keys=False,
    ):
        connection_pool = check_callable(connection_pool)
        prefix = check_callable(prefix)
        ignore_deserialization_errors = check_callable(ignore_deserialization_errors)
        save_consistency = check_callable(save_consistency)
        economy = check_callable(economy)
        use_keys = check_callable(use_keys)
        check_types(ignore_deserialization_errors, bool)
        check_types(save_consistency, bool)
        check_types(economy, bool)
        check_types(use_keys, bool)
        self.registered_models = []
        self.registered_django_models = {}
        prefix = check_callable(prefix)
        if type(prefix) == str:
            self.prefix = prefix
        else:
            print(
                f'{datetime.datetime.now()} - Prefix {prefix} is type of {type(prefix)}, allowed only str, using default prefix "redis_test"')
            self.prefix = 'redis_test'
        self.connection_pool = self._get_connection_pool(connection_pool)
        self.ignore_deserialization_errors = ignore_deserialization_errors
        self.save_consistency = save_consistency
        self.economy = economy
        self.use_keys = use_keys
    
    @property
    def redis_instance(self):
        redis_instance = redis.Redis(connection_pool=self.connection_pool)
        return redis_instance
    
    @property
    def cached_models(self):
        return self.registered_models
    
    def fast_get_keys_values(self, string):
        if self.use_keys:
            keys = list(self.redis_instance.keys(string))
        else:
            keys = list(self.redis_instance.scan_iter(string))
        values = self.redis_instance.mget(keys)
        results = dict(zip(keys, values))
        return results
    
    def _get_connection_pool(self, connection_pool):
        if isinstance(connection_pool, redis.ConnectionPool):
            connection_pool.connection_kwargs['decode_responses'] = True
            self.connection_pool = connection_pool
        else:
            print(
                f'{datetime.datetime.now()} - {self.__class__.__name__}: No connection_pool provided, trying default config...')
            default_host = 'localhost'
            default_port = 6379
            default_db = 0
            try:
                connection_pool = redis.ConnectionPool(
                    decode_responses=True,
                    host=default_host,
                    port=default_port,
                    db=default_db,
                )
                self.connection_pool = connection_pool
            except BaseException as ex:
                raise Exception(
                    f'Default config ({default_host}:{default_port}, db={default_db}) failed, please provide connection_pool to {self.__class__.__name__}')
        return self.connection_pool
    
    def register_models(self, models_list):
        for model in models_list:
            if issubclass(model, RedisModel):
                if model not in self.registered_models:
                    self.registered_models.append(model)
            else:
                raise Exception(f'{model.__name__} class is not RedisModel')
    
    def _get_registered_model_by_name(self, model_name):
        found = False
        model = None
        for registered_model in self.registered_models:
            if registered_model.__name__ == model_name:
                found = True
                model = registered_model
                break
        if not found:
            if self.ignore_deserialization_errors:
                print(f'{datetime.datetime.now()} - {model_name} not found in registered models, ignoring')
                model = model_name
            else:
                raise Exception(f'{model_name} not found in registered models')
        return model
    
    def _get_field_instance_by_name(self, field_name, model):
        field_instance = None
        try:
            if field_name == 'id':
                field_instance = getattr(model, field_name)
            else:
                field_instance = getattr(model, field_name)
        except BaseException as ex:
            if self.ignore_deserialization_errors:
                print(
                    f'{datetime.datetime.now()} - {model.__name__} has no field {field_name}, ignoring deserialization')
                field_instance = field_name
            else:
                raise Exception(f'{model.__name__} has no field {field_name}')
        return field_instance
    
    def _deserialize_value_by_field_instance(self, raw_value, field_instance):
        value = field_instance.deserialize_value(raw_value, self)
        try:
            pass
        except BaseException as ex:
            if self.ignore_deserialization_errors:
                print(
                    f'{datetime.datetime.now()} - {raw_value} can not be deserialized like {field_instance.__class__.__name__}, ignoring')
                value = raw_value
            else:
                raise Exception(f'{raw_value} can not be deserialized like {field_instance.__class__.__name__}')
        return value
    
    def deserialize_value(self, raw_value, model_name, field_name):
        value = raw_value
        saved_model = self._get_registered_model_by_name(model_name)
        if issubclass(saved_model, RedisModel):
            saved_field_instance = self._get_field_instance_by_name(field_name, saved_model)
            if issubclass(saved_field_instance.__class__, RedisField):
                value = self._deserialize_value_by_field_instance(raw_value, saved_field_instance)
        return value
    
    def _return_with_format(self, instances, return_dict=False):
        if return_dict:
            return instances
        else:
            instances_list = [
                {
                    'id': instance_id,
                    **instance_fields
                }
                for instance_id, instance_fields in instances.items()
            ]
            return instances_list
    
    def _check_fields_existence(self, model, instances_with_allowed, filters):
        checked_instances = {}
        fields = model.__dict__
        cleaned_fields = {}
        for field_name, field in fields.items():
            if not field_name.startswith('__'):
                cleaned_fields[field_name] = field
        if 'id' not in cleaned_fields.keys():
            cleaned_fields['id'] = RedisString(null=True)
        fields = cleaned_fields
        for instance_id, instance_fields in instances_with_allowed.items():
            checked_instances[instance_id] = {}
            for field_name, field in fields.items():
                if field_name in instance_fields.keys():
                    checked_instances[instance_id][field_name] = instance_fields[field_name]
                else:
                    field.value = None
                    cleaned_value = field.clean()
                    allowed = self._filter_field_name(model, field_name, cleaned_value, filters)
                    checked_instances[instance_id][field_name] = {
                        'value': cleaned_value,
                        'allowed': allowed
                    }
        return checked_instances
    
    def _filter_value(self, value, filter_type, filter_by):
        allowed = True
        if filter_type == 'exact':
            if value != filter_by:
                allowed = False
        elif filter_type == 'iexact':
            if value.lower() != filter_by.lower():
                allowed = False
        elif filter_type == 'contains':
            if filter_by not in value:
                allowed = False
        elif filter_type == 'icontains':
            if filter_by.lower() not in value.lower():
                allowed = False
        elif filter_type == 'in':
            if value not in filter_by:
                allowed = False
        elif filter_type == 'gt':
            if value <= filter_by:
                allowed = False
        elif filter_type == 'gte':
            if value < filter_by:
                allowed = False
        elif filter_type == 'lt':
            if value >= filter_by:
                allowed = False
        elif filter_type == 'lte':
            if value > filter_by:
                allowed = False
        elif filter_type == 'startswith':
            if not value.startswith(filter_by):
                allowed = False
        elif filter_type == 'istartswith':
            if not value.lower().startswith(filter_by.lower()):
                allowed = False
        elif filter_type == 'endswith':
            if not value.endswith(filter_by):
                allowed = False
        elif filter_type == 'iendswith':
            if not value.lower().endswith(filter_by.lower()):
                allowed = False
        elif filter_type == 'range':
            if value not in range(filter_by):
                allowed = False
        elif filter_type == 'isnull':
            if (value in ['null', None]) != filter_by:
                allowed = False
        return allowed
    
    def _split_filtering(self, filter_param):
        filter_field_name, filter_type = filter_param, 'exact'
        if '__' in filter_param:
            filter_param_split = filter_param.split('__')
            if filter_param_split[-1] in ['exact', 'iexact', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte',
                                          'startswith', 'istartswith', 'endswith', 'iendswith', 'range']:
                fields_to_filter = filter_param_split[:-1]
                filter_type = filter_param_split[-1]
            else:
                fields_to_filter = filter_param_split
        else:
            fields_to_filter = [filter_field_name]
        return fields_to_filter, filter_type
    
    def _filter(self, value, fields_to_filter, filter_type, filter_by):
        for field_to_filter in fields_to_filter:
            if value in ['null', None]:
                value = None
            else:
                try:
                    value = value[field_to_filter]
                except BaseException as ex:
                    print(f'Exception: {ex}\n'
                          f'Info: {field_to_filter}, {value}\n'
                          f'Maybe: deep filtering is not included on this model')
                    value = None
        if isinstance(value, datetime.datetime) and isinstance(filter_by, datetime.datetime):
            value = value.replace(tzinfo=pytz.UTC)
            filter_by = filter_by.replace(tzinfo=pytz.UTC)
        try:
            allowed = self._filter_value(value, filter_type, filter_by)
        except:
            allowed = False
        return allowed
    
    def _filter_field_name(self, field_name, value, raw_filters):
        allowed_list = [True]
        for filter_param in raw_filters.keys():
            filter_by = raw_filters[filter_param]
            fields_to_filter, filter_type = self._split_filtering(filter_param)
            if field_name == fields_to_filter[0]:
                fields_to_filter = fields_to_filter[1:]
                allowed_list.append(self._filter(value, fields_to_filter, filter_type, filter_by))
        allowed = all(allowed_list)
        return allowed
    
    def _get_instances_by_key(self, key):
        raw_instances = self.fast_get_keys_values(key)
        instances = {}
        for instance_key, fields_json in raw_instances.items():
            prefix, model_name, instance_id = instance_key.split(':')
            instance_id = int(instance_id)
            fields_dict = json.loads(fields_json)
            for field_name, raw_value in fields_dict.items():
                value = self.deserialize_value(raw_value, model_name, field_name)
                if instance_id not in instances.keys():
                    instances[instance_id] = {}
                instances[instance_id][field_name] = value
        return instances
    
    def _get_all_stored_model_instances(self, model, filters=None):
        model_name = model.__name__
        instances = self._get_instances_by_key(f'{self.prefix}:{model_name}:*')
        instances_with_allowed = {}
        for instance_id, instance_fields in instances.items():
            for field_name, field_value in instance_fields.items():
                allowed = self._filter_field_name(model, field_name, field_value, filters)
                if instance_id not in instances_with_allowed.keys():
                    instances_with_allowed[instance_id] = {}
                instances_with_allowed[instance_id][field_name] = {
                    'value': field_value,
                    'allowed': allowed
                }
        return instances_with_allowed
    
    def _get_instances_from_instances_with_allowed(self, instances_with_allowed):
        instances = {}
        for instance_id, instance_fields in instances_with_allowed.items():
            instance_allowed = all([
                instance_field_data['allowed']
                for instance_field_data in instance_fields.values()
            ])
            if instance_allowed and instance_id not in instances.keys():
                instances[instance_id] = {
                    instance_field_name: instance_field_data['value']
                    for instance_field_name, instance_field_data in instance_fields.items()
                }
        return instances
    
    def _get_all_model_instances(self, model, filters=None):
        if filters is None:
            filters = {}
        instances_with_allowed = self._get_all_stored_model_instances(model, filters)
        if self.save_consistency:
            instances_with_allowed = self._check_fields_existence(model, instances_with_allowed, filters)
        instances = self._get_instances_from_instances_with_allowed(instances_with_allowed)
        return instances
    
    def get(self, model, return_dict=False, **filters):
        instances = self._get_all_model_instances(model, filters)
        return self._return_with_format(instances, return_dict)
    
    def order(self, instances, field_name):
        reverse = False
        if field_name.startswith('-'):
            reverse = True
            field_name = field_name[1:]
        
        return sorted(instances, key=(lambda instance: instance[field_name]), reverse=reverse)
    
    def _update_by_instance_key(self, instance_key, fields_to_update, renew_ttl, new_ttl):
        updated_data = None
        prefix, model_name, instance_id = instance_key.split(':')
        model = self._get_registered_model_by_name(model_name)
        instance_id = int(instance_id)
        instance_data_json = self.redis_instance.get(instance_key)
        instance_data = json.loads(instance_data_json)
        data_to_write = {}
        for field_name, field_data in instance_data.items():
            saved_field_instance = self._get_field_instance_by_name(field_name, model)
            if field_name in fields_to_update.keys():
                saved_field_instance.value = fields_to_update[field_name]
                cleaned_value = saved_field_instance.clean()
            else:
                cleaned_value = field_data
            if instance_key not in data_to_write.keys():
                data_to_write[instance_key] = {}
            data_to_write[instance_key][field_name] = cleaned_value
        for instance_key, fields_to_write in data_to_write.items():
            ttl = None
            if renew_ttl:
                ttl = model.get_model_ttl()
            elif new_ttl:
                ttl = new_ttl
            fields_to_write_json = json.dumps(fields_to_write)
            self.redis_instance.set(instance_key, fields_to_write_json, ex=ttl)
            updated_data = {
                'model': model,
                'id': instance_id
            }
        return updated_data
    
    def _get_allowed_model_params(self, model, params):
        model_fields_names = model.__dict__.keys()
        allowed_param_names = list(filter(
            lambda param_name: param_name in model_fields_names and not param_name.startswith('__'),
            params.keys()
        ))
        result_params = {param_name: params[param_name] for param_name in params.keys() if
                         param_name in allowed_param_names}
        return result_params
    
    def update(self, model, instances=None, return_dict=False, renew_ttl=False, new_ttl=None,
               **fields_to_update):
        model_name = model.__name__
        updated_datas = []
        if instances is None:
            for key in self.redis_instance.keys(f'{self.prefix}:{model_name}:*'):
                updated_data = self._update_by_instance_key(key, fields_to_update, renew_ttl, new_ttl)
                if updated_data is not None:
                    updated_datas.append(updated_data)
        else:
            ids_to_update = get_ids_from_untyped_data(instances)
            for instance_id in ids_to_update:
                for key in self.redis_instance.keys(f'{self.prefix}:{model_name}:{instance_id}'):
                    updated_data = self._update_by_instance_key(key, fields_to_update, renew_ttl, new_ttl)
                    if updated_data is not None:
                        updated_datas.append(updated_data)
        updated_instances = {}
        for updated_data in updated_datas:
            updated_model = updated_data['model']
            updated_id = updated_data['id']
            if self.economy:
                updated_instances[updated_id] = {'id': updated_id}
            else:
                updated_instance_qs = self.get(updated_model, id=updated_id)
                updated_instance = updated_instance_qs[0]
                updated_instances[updated_id] = updated_instance
        result = self._return_with_format(updated_instances, return_dict)
        return result
    
    def _delete_by_key(self, key):
        self.redis_instance.delete(key)
    
    def delete(self, model, instances=None):
        model_name = model.__name__
        if instances is None:
            for key in self.redis_instance.keys(f'{self.prefix}:{model_name}:*'):
                self._delete_by_key(key)
        else:
            ids_to_delete = get_ids_from_untyped_data(instances)
            for instance_id in ids_to_delete:
                for key in self.redis_instance.keys(f'{self.prefix}:{model_name}:{instance_id}'):
                    self._delete_by_key(key)
    
    def create(self, model, **params):
        params = self._get_allowed_model_params(model, params)
        redis_instance = model(redis_root=self, **params).save()
        return redis_instance


### REDIS MODEL ###


class RedisModel:
    id = RedisId()
    
    def __init__(self, redis_root=None, **kwargs):
        self.__model_data__ = {
            'redis_root': None,
            'name': None,
            'fields': None,
            'meta': {}
        }
        
        if isinstance(redis_root, RedisRoot):
            self.__model_data__['redis_root'] = redis_root
            self.__model_data__['name'] = self.__class__.__name__
            if self.__class__ != RedisModel:
                self._renew_fields()
                self.__model_data__['redis_root'].register_models([self.__class__])
                self._fill_fields_values(kwargs)
        
        else:
            raise Exception(f'{redis_root.__name__} type is {type(redis_root)}. Allowed only RedisRoot')
    
    def _check_meta_ttl(self, ttl):
        check_types(ttl, (int, float))
        return ttl
    
    def _set_meta(self, meta_fields):
        allowed_meta_fields_with_check_functions = {
            'ttl': self._check_meta_ttl,
        }
        for field_name, field_value in meta_fields.items():
            if field_name in allowed_meta_fields_with_check_functions.keys():
                cleaned_value = allowed_meta_fields_with_check_functions[field_name](field_value)
                if cleaned_value is not None:
                    self.__model_data__['meta'][field_name] = cleaned_value
    
    def _get_initial_model_field(self, field_name):
        name = self.__model_data__['name']
        if field_name in self.__class__.__dict__.keys():
            return deepcopy(self.__class__.__dict__[field_name])
        else:
            raise Exception(f'{name} has no field {field_name}')
    
    def _renew_fields(self):
        class_fields = self.__class__.__dict__.copy()
        fields = {}
        for field_name, field in class_fields.items():
            if not field_name.startswith('__'):
                if field_name == 'Meta':
                    self._set_meta(self.__class__.Meta.__dict__)
                else:
                    fields[field_name] = self._get_initial_model_field(field_name)
        self._get_new_id()
        if 'id' not in fields.keys():
            fields['id'] = self.id
        self.__model_data__['fields'] = fields
    
    def _fill_fields_values(self, field_values_dict):
        for name, value in field_values_dict.items():
            fields = self.__model_data__['fields']
            if name in fields.keys():
                self.__model_data__['fields'][name].value = value
            else:
                raise Exception(f'{self.__class__.__name__} has no field {name}')
    
    def _serialize_data(self):
        redis_root = self.__model_data__['redis_root']
        name = self.__model_data__['name']
        fields = self.__model_data__['fields']
        fields = dict(fields)
        instance_key = f'{redis_root.prefix}:{name}:{self.id.value}'
        deserialized_fields = {}
        cleaned_fields = {}
        for field_name, field in fields.items():
            if not field_name.startswith('__'):
                try:
                    cleaned_value = field.clean()
                    cleaned_fields[field_name] = cleaned_value
                    deserialized_value = redis_root.deserialize_value(cleaned_value, name, field_name)
                    deserialized_fields[field_name] = deserialized_value
                except BaseException as ex:
                    raise Exception(f'{ex} ({name} -> {field_name})')
        return instance_key, cleaned_fields, deserialized_fields
    
    def get_model_ttl(self):
        ttl = None
        meta = self.__model_data__['meta']
        if 'ttl' in meta.keys():
            ttl = meta['ttl']
        return ttl
    
    def _set_fields(self):
        instance_key, fields_dict, deserialized_fields = self._serialize_data()
        model_ttl = self.get_model_ttl()
        redis_root = self.__model_data__['redis_root']
        prefix, model_name, instance_id = instance_key.split(':')
        redis_instance = redis_root.redis_instance
        fields_json = json.dumps(fields_dict)
        redis_instance.set(instance_key, fields_json, ex=model_ttl)
        saved_instance = deserialized_fields
        return saved_instance
    
    def _get_new_id(self):
        redis_root = self.__model_data__['redis_root']
        instances_with_ids = redis_root.get(self.__class__, return_dict=True)
        all_ids = [int(instance_id) for instance_id in list(instances_with_ids.keys())]
        if all_ids:
            max_id = max(all_ids)
        else:
            max_id = 0
        self.id.value = int(max_id + 1)
    
    def save(self):
        saved_instance = self._set_fields()
        return saved_instance
    
    def set(self, **fields_with_values):
        name = self.__model_data__['name']
        fields = self.__model_data__['fields']
        meta = self.__model_data__['meta']
        for field_name, value in fields_with_values.items():
            if field_name in fields.keys():
                field = fields[field_name]
                field.value = value
                return field.value
            elif field_name in meta.keys():
                meta[field_name] = value
                return meta[field_name]
            else:
                raise Exception(f'{name} has no field {field_name}')
    
    def get(self, field_name):
        name = self.__model_data__['name']
        fields = self.__model_data__['fields']
        meta = self.__model_data__['meta']
        if field_name in fields.keys():
            field = fields[field_name]
            return field.value
        elif field_name in meta.keys():
            return meta[field_name]
        else:
            raise Exception(f'{name} has no field {field_name}')
