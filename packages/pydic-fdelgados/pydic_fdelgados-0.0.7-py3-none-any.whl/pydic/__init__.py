import os
import os.path
from typing import List, Dict, Generator, Optional, Union
from importlib import util
import xml.etree.ElementTree as ElementTree
from dependency_injector import containers


def create_container(services_files: List, event_handlers_files: Optional[Union[str, List[str]]] = None):
    service_container = containers.DynamicContainer()
    services = _get_services(services_files)
    service_provider_cls = _import_cls('dependency_injector.providers.Factory')

    event_handlers = {}
    actual_services_ids = []
    for service_id, info in services.items():
        if not info.get('alias'):
            continue

        try:
            services[service_id] = services[info.get('alias')]
            actual_services_ids.append(info.get('alias'))
        except KeyError:
            continue

    for actual_services_id in actual_services_ids:
        del services[actual_services_id]

    for service_id, info in services.items():
        _create_service(services, service_container, service_provider_cls, service_id, info)

    if event_handlers_files is not None:
        if isinstance(event_handlers_files, str):
            event_handlers_files = [event_handlers_files]

        for event_handlers_file in event_handlers_files:
            event_handlers.update(_get_event_handlers(event_handlers_file))

    class Container:
        @classmethod
        def get(cls, registered_service_id: str):
            return getattr(service_container, registered_service_id.replace('.', '_'))()

        @classmethod
        def event_handlers(cls, event_name: str) -> Generator:
            subscribers = event_handlers.get(event_name, {}).get('subscribers', {})

            for subscriber in subscribers:
                yield Container.get(subscriber)

    return Container


def _get_services(services_files: List) -> Dict:
    services = {}

    for services_file in services_files:
        services.update(_get_service_from_file(services_file))

    return services


def _get_service_from_file(services_file: str) -> Dict:
    _ensure_file_exist(services_file)
    _ensure_file_is_valid(services_file)

    services = {}

    tree = ElementTree.parse(services_file)
    root = tree.getroot()

    for service in root:
        if service.tag != 'service':
            continue

        if service.attrib.get('alias'):
            services[service.attrib['id']] = {'alias': service.attrib.get('alias')}

            continue

        service_data = {'class_name': service.attrib['class'], 'arguments': []}

        for service_argument in service:
            if service_argument.tag != 'argument':
                continue

            service_data['arguments'].append(
                {
                    'type': service_argument.attrib['type'],
                    'name': service_argument.attrib['name'],
                    'value': service_argument.attrib['value']
                }
            )

        services[service.attrib['id']] = service_data

    return services


def _import_cls(full_class_name: str):
    path_components = full_class_name.split('.')
    class_name = path_components[-1]
    mod = '.'.join(path_components[:-1])

    spec = util.find_spec(mod)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, class_name)


def _create_service(services, service_container, service_provider_cls, id: str, info):
    service_key = id.replace('.', '_')
    if hasattr(service_container, service_key):
        return getattr(service_container, service_key)

    service_args = info.get('arguments')
    args = {}

    for argument in service_args:
        if argument.get('type') == 'env':
            args[argument['name']] = os.environ.get(argument['value'])
        elif argument.get('type') == 'parameter':
            args[argument['name']] = argument['value']
        elif argument.get('type') == 'service':
            dependency_service_id = argument['value']

            if isinstance(services[dependency_service_id], str):
                dependency_service_id = services[dependency_service_id]

            dependency_service_info = services[dependency_service_id]

            args[argument['name']] = _create_service(
                services,
                service_container,
                service_provider_cls,
                dependency_service_id,
                dependency_service_info
            )

    service_cls = _import_cls(info.get('class_name'))
    setattr(service_container, service_key, service_provider_cls(service_cls, **args))

    return getattr(service_container, service_key)


def _get_event_handlers(event_handlers_file: str):
    _ensure_file_exist(event_handlers_file)
    _ensure_file_is_valid(event_handlers_file)

    events = {}

    tree = ElementTree.parse(event_handlers_file)
    root = tree.getroot()

    for event in root:
        if event.tag != 'event':
            continue

        event_class_name = event.attrib['class']
        events[event_class_name] = {'class': _import_cls(event_class_name), 'subscribers': []}

        for event_handler in event:
            if event_handler.tag != 'handler':
                continue

            events[event_class_name]['subscribers'].append(event_handler.attrib['id'])

    return events


def _ensure_file_exist(services_file: str):
    if not os.path.exists(services_file):
        raise FileNotFoundError('File {} does not exists'.format(services_file))


def _ensure_file_is_valid(services_file: str):
    if not services_file.endswith('.xml'):
        raise ValueError('Services file must be an xml file')
