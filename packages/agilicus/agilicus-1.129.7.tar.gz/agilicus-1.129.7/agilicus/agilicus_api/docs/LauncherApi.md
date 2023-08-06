# agilicus_api.LauncherApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_launcher**](LauncherApi.md#delete_launcher) | **DELETE** /v1/launchers/{launcher_id} | Delete a Launcher
[**get_launcher**](LauncherApi.md#get_launcher) | **GET** /v1/launchers/{launcher_id} | Get a single launcher
[**replace_launcher**](LauncherApi.md#replace_launcher) | **PUT** /v1/launchers/{launcher_id} | Create or update a launcher


# **delete_launcher**
> delete_launcher(launcher_id)

Delete a Launcher

Delete a Launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launcher_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = launcher_api.LauncherApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Launcher
        api_instance.delete_launcher(launcher_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->delete_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Launcher
        api_instance.delete_launcher(launcher_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->delete_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Launcher has been deleted |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_launcher**
> Launcher get_launcher(launcher_id)

Get a single launcher

Get a single launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launcher_api
from agilicus_api.model.launcher import Launcher
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = launcher_api.LauncherApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    expand_resource_members = False # bool | On resource requests, when True will populate member_resources with its full Resource object.  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single launcher
        api_response = api_instance.get_launcher(launcher_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->get_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single launcher
        api_response = api_instance.get_launcher(launcher_id, org_id=org_id, expand_resource_members=expand_resource_members)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->get_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **expand_resource_members** | **bool**| On resource requests, when True will populate member_resources with its full Resource object.  | [optional] if omitted the server will use the default value of False

### Return type

[**Launcher**](Launcher.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return Launcher |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_launcher**
> Launcher replace_launcher(launcher_id)

Create or update a launcher

Create or update a launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launcher_api
from agilicus_api.model.launcher import Launcher
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = launcher_api.LauncherApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    launcher = Launcher(
        metadata=MetadataWithId(),
        spec=LauncherSpec(
            name="name_example",
            org_id="123",
            resource_members=[
                ResourceMember(
                    id="123",
                ),
            ],
            config=LauncherConfig(
                command_path="command_path_example",
                command_arguments="command_arguments_example",
                start_in="start_in_example",
            ),
        ),
        status=LauncherStatus(
            application_services=[
                ApplicationService(
                    name="my-local-service",
                    org_id="org_id_example",
                    hostname="db.example.com",
                    ipv4_addresses=[
                        "192.0.2.1",
                    ],
                    name_resolution="static",
                    config=NetworkServiceConfig(
                        ports=[
                            NetworkPortRange(
                                protocol="tcp",
                                port=NetworkPort("5005-5010"),
                            ),
                        ],
                    ),
                    port=1,
                    protocol="tcp",
                    assignments=[
                        ApplicationServiceAssignment(
                            app_id="app_id_example",
                            environment_name="environment_name_example",
                            org_id="org_id_example",
                        ),
                    ],
                    service_type="vpn",
                    tls_enabled=True,
                    tls_verify=True,
                    connector_id="123",
                    stats=ApplicationServiceStats(),
                ),
            ],
            file_shares=[
                FileShareService(
                    metadata=MetadataWithId(),
                    spec=FileShareServiceSpec(
                        name="share1",
                        share_name="share1",
                        org_id="123",
                        local_path="/home/agilicus/public/share1",
                        connector_id="123",
                        share_index=1,
                        transport_end_to_end_tls=True,
                        transport_base_domain="transport_base_domain_example",
                        client_config=[
                            NetworkMountRuleConfig(
                                rules=ResourceRuleGroup(
                                    tags=[
                                        SelectorTag("service-desk"),
                                    ],
                                ),
                                mount=FileShareClientConfig(
                                    windows_config=FileShareClientConfigWindowsConfig(
                                        name="name_example",
                                        type="mapped_drive",
                                    ),
                                    linux_config=FileShareClientConfigLinuxConfig(
                                        path="",
                                    ),
                                    mac_config=FileShareClientConfigLinuxConfig(
                                        path="",
                                    ),
                                ),
                            ),
                        ],
                    ),
                    status=FileShareServiceStatus(
                        share_base_app_name="share_base_app_name_example",
                        instance_id="asdas9Gk4asdaTH",
                        instance_org_id="39ddfGAaslts8qX",
                        share_uri="https://share-4.cloud.egov.city/",
                        stats=FileShareServiceStats(),
                    ),
                ),
            ],
        ),
    ) # Launcher |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a launcher
        api_response = api_instance.replace_launcher(launcher_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->replace_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a launcher
        api_response = api_instance.replace_launcher(launcher_id, org_id=org_id, launcher=launcher)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LauncherApi->replace_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **launcher** | [**Launcher**](Launcher.md)|  | [optional]

### Return type

[**Launcher**](Launcher.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated Launcher |  -  |
**400** | Error updating the Launcher |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

