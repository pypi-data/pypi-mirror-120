import json
import urllib

import requests


def get_pulsar_admin_headers(token, **kwargs):
    headers = {
        "Authorization": "Bearer {token}".format(token=token),
        "Content-Type": "application/json",
    }
    return {**headers, **kwargs}


def get_pulsar_admin_form_headers(token, **kwargs):
    headers = {
        "Authorization": "Bearer {token}".format(token=token)
        #  , 'Content-Type': 'multipart/form-data; boundary=1'
    }
    return {**headers, **kwargs}


def create_response_obj(response):
    # Check the type
    body = response.content

    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type:
        result = {"content": body}
    elif "application/json" in content_type:
        result = json.loads(body)
    else:
        result = {"content": ""}

    return {
        "status_code": response.status_code,
        "result": result,
        "message": response.reason,
    }


class PulsarAdmin:
    def create_tenant(
        base_url, token, tenant, body
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/tenants/{tenant}".format(
            base_url=base_url, tenant=tenant
        )
        return create_response_obj(requests.put(url, headers=headers, json=body, verify=False))

    def create_tenant_all_clusters(
        base_url, token, tenant, body
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        clusters_url = "{base_url}/admin/v2/clusters/".format(base_url=base_url)
        clusters_response = requests.get(clusters_url, headers=headers, verify=False)
        body["allowedClusters"] = json.loads(clusters_response.content)
        url = "{base_url}/admin/v2/tenants/{tenant}".format(
            base_url=base_url, tenant=tenant
        )

        return create_response_obj(requests.put(url, headers=headers, json=body, verify=False))

    def create_namespace(
        base_url, token, tenant, namespace, policies
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/namespaces/{tenant}/{namespace}".format(
            base_url=base_url, tenant=tenant, namespace=namespace
        )
        return create_response_obj(requests.put(url, headers=headers, json=policies, verify=False))

    def create_topic(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.put(url, headers=headers, verify=False))

    def create_topic_subscription(
        base_url, token, tenant, namespace, name, sub_name, message_id
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        sub_name_encoded = urllib.parse.quote(sub_name, safe="")
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}/subscription/{sub_name_encoded}".format(
            base_url=base_url,
            tenant=tenant,
            namespace=namespace,
            name=name,
            sub_name_encoded=sub_name_encoded,
        )
        return create_response_obj(requests.put(url, headers=headers, json=message_id, verify=False))

    def grant_permissions_namespace(
        base_url, token, tenant, namespace, role, actions
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/namespaces/{tenant}/{namespace}/permissions/{role}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, role=role
        )
        return create_response_obj(requests.post(url, headers=headers, json=actions, verify=False))

    def grant_permissions_topic(
        base_url, token, tenant, namespace, name, role, actions
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}/permissions/{role}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name, role=role
        )
        return create_response_obj(requests.post(url, headers=headers, json=actions, verify=False))

    def delete_topic(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.delete(url, headers=headers, verify=False))

    def delete_topic_subscription(
        base_url, token, tenant, namespace, name, sub_name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        sub_name_encoded = urllib.parse.quote(sub_name, safe="")
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}/subscription/{sub_name_encoded}".format(
            base_url=base_url,
            tenant=tenant,
            namespace=namespace,
            name=name,
            sub_name_encoded=sub_name_encoded,
        )
        return create_response_obj(requests.delete(url, headers=headers, verify=False))

    def skip_all_messages_on_subscription(
        base_url, token, tenant, namespace, name, sub_name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        sub_name_encoded = urllib.parse.quote(sub_name, safe="")
        url = "{base_url}/admin/v2/persistent/{tenant}/{namespace}/{name}/subscription/{sub_name_encoded}/skip_all".format(
            base_url=base_url,
            tenant=tenant,
            namespace=namespace,
            name=name,
            sub_name_encoded=sub_name_encoded,
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def get_tenants(
            base_url, token
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/tenants".format(base_url=base_url)
        return create_response_obj(requests.get(url, headers=headers, verify=False))

    def get_namespaces(
            base_url, token, tenant
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v2/namespaces/{tenant}".format(base_url=base_url, tenant=tenant)
        return create_response_obj(requests.get(url, headers=headers, verify=False))

    def rebalance(base_url, token):
        headers = get_pulsar_admin_form_headers(token)
        url = "{base_url}/admin/v2/worker/rebalance".format(base_url=base_url)
        result = create_response_obj(requests.put(url, headers=headers, verify=False))
        return result


class PulsarFunctionAdmin:
    def get_function(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.get(url, headers=headers, verify=False))

    def start_function(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}/start".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def stop_function(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}/stop".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def delete_function(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.delete(url, headers=headers, verify=False))

    def create_function(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "functionConfig": (None, json.dumps(config), "application/json"),
            "url": (None, fn_url),
        }
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        result = create_response_obj(requests.post(url, headers=headers, files=form, verify=False))
        return result

    def update_function(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "functionConfig": (None, json.dumps(config), "application/json"),
            "url": (None, fn_url),
        }
        url = "{base_url}/admin/v3/functions/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        result = create_response_obj(requests.put(url, headers=headers, files=form, verify=False))
        return result

    def conditional_upsert_function(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        get_response = PulsarFunctionAdmin.get_function(
            base_url, token, tenant, namespace, name
        )
        if get_response["status_code"] == 404:
            return PulsarFunctionAdmin.create_function(
                base_url, token, tenant, namespace, name, config, fn_url
            )
        else:
            return PulsarFunctionAdmin.update_function(
                base_url, token, tenant, namespace, name, config, fn_url
            )

    def unconditional_upsert_function(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        upsert_response = PulsarFunctionAdmin.conditional_upsert_function(
            base_url, token, tenant, namespace, name, config, fn_url
        )
        if upsert_response["status_code"] != 200:
            PulsarFunctionAdmin.delete_function(
                base_url, token, tenant, namespace, name
            )
            return PulsarFunctionAdmin.create_function(
                base_url, token, tenant, namespace, name, config, fn_url
            )


class PulsarSinkAdmin:
    def get_sink(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.get(url, headers=headers, verify=False))

    def start_sink(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}/start".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def stop_sink(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}/stop".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def delete_sink(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.delete(url, headers=headers, verify=False))

    def create_sink(
        base_url, token, tenant, namespace, name, config, sink_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "sinkConfig": (None, json.dumps(config), "application/json"),
            "url": (None, sink_url),
        }
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, files=form, verify=False))

    def update_sink(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "sinkConfig": (None, json.dumps(config), "application/json"),
            "url": (None, fn_url),
        }
        url = "{base_url}/admin/v3/sinks/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        result = create_response_obj(requests.put(url, headers=headers, files=form, verify=False))
        return result

    def conditional_upsert_sink(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        get_response = PulsarSinkAdmin.get_sink(
            base_url, token, tenant, namespace, name
        )
        if get_response["status_code"] == 404:
            return PulsarSinkAdmin.create_sink(
                base_url, token, tenant, namespace, name, config, fn_url
            )
        else:
            return PulsarSinkAdmin.update_sink(
                base_url, token, tenant, namespace, name, config, fn_url
            )

    def unconditional_upsert_sink(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        upsert_response = PulsarSinkAdmin.conditional_upsert_sink(
            base_url, token, tenant, namespace, name, config, fn_url
        )
        if upsert_response["status_code"] != 200:
            PulsarSinkAdmin.delete_sink(base_url, token, tenant, namespace, name)
            return PulsarSinkAdmin.create_sink(
                base_url, token, tenant, namespace, name, config, fn_url
            )


class PulsarSourceAdmin:
    def get_source(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument

        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/sources/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.get(url, headers=headers, verify=False))

    def start_source(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/source/{tenant}/{namespace}/{name}/start".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def stop_source(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/source/{tenant}/{namespace}/{name}/stop".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.post(url, headers=headers, verify=False))

    def delete_source(
        base_url, token, tenant, namespace, name
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_headers(token)
        url = "{base_url}/admin/v3/source/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        return create_response_obj(requests.delete(url, headers=headers, verify=False))

    def create_source(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "sourceConfig": (None, json.dumps(config), "application/json"),
            "url": (None, fn_url),
        }
        url = "{base_url}/admin/v3/source/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        result = create_response_obj(requests.post(url, headers=headers, files=form, verify=False))
        return result

    def update_source(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        headers = get_pulsar_admin_form_headers(token)
        form = {
            "sourceConfig": (None, json.dumps(config), "application/json"),
            "url": (None, fn_url),
        }
        url = "{base_url}/admin/v3/sources/{tenant}/{namespace}/{name}".format(
            base_url=base_url, tenant=tenant, namespace=namespace, name=name
        )
        result = create_response_obj(requests.put(url, headers=headers, files=form, verify=False))
        return result

    def conditional_upsert_source(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        get_response = PulsarSourceAdmin.get_source(
            base_url, token, tenant, namespace, name
        )
        if get_response["status_code"] == 404:
            return PulsarSourceAdmin.create_source(
                base_url, token, tenant, namespace, name, config, fn_url
            )
        else:
            return PulsarSourceAdmin.update_source(
                base_url, token, tenant, namespace, name, config, fn_url
            )

    def unconditional_upsert_source(
        base_url, token, tenant, namespace, name, config, fn_url
    ):  # pylint: disable=no-self-argument
        upsert_response = PulsarSourceAdmin.conditional_upsert_source(
            base_url, token, tenant, namespace, name, config, fn_url
        )
        if upsert_response["status_code"] != 200:
            PulsarSourceAdmin.delete_source(base_url, token, tenant, namespace, name)
            return PulsarSourceAdmin.create_source(
                base_url, token, tenant, namespace, name, config, fn_url
            )
