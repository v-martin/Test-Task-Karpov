import inspect
import api.models as models
import api.serializers as serializers


def get_model_map():
    model_string_map = {}
    for cls_name, cls_obj in inspect.getmembers(models):
        if inspect.isclass(cls_obj):
            model_string_map.update({cls_name: cls_obj})
    return model_string_map


def get_serializer_map():
    serializer_string_map = {}
    for cls_name, cls_obj in inspect.getmembers(serializers):
        if inspect.isclass(cls_obj):
            serializer_string_map.update({cls_name: cls_obj})
    return serializer_string_map
