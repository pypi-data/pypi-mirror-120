import logging
import sys
import string
import random

import click
from pulse import lib
from pulse.pulsar_admin import PulsarAdmin

# Logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@click.group()
@click.option('--url', required=True)
@click.option('--admin-token', required=True)
@click.option('--api-url', required=True)
@click.option('--cert-file', required=True)
@click.pass_context
def pulse(ctx, url, admin_token, api_url, cert_file):
    ctx.obj = lib.PulseSecrets(url, admin_token, api_url, cert_file)
    """A CLI tool for getting info from Pulsar"""


@pulse.group()
def functions():
    """Functions resource in pulsar"""


@functions.command()
def ls():
    print("FUNCTIONS!")


@pulse.group()
def namespaces():
    """Namespaces resource in pulsar"""


@namespaces.command()
@click.option('--tenant', '-t', required=True)
@click.pass_obj
def ls(ctx, tenant):
    result = PulsarAdmin.get_namespaces(ctx.api_url, ctx.admin_token, tenant)
    click.echo('\n'.join(result["result"]))


@pulse.group()
def tenants():
    """Tenants resource in pulsar"""


@tenants.command()
@click.pass_obj
def ls(ctx):
    result = PulsarAdmin.get_tenants(ctx.api_url, ctx.admin_token)
    click.echo('\n'.join(result["result"]))


@pulse.group()
def topics():
    """Topics resource in pulsar"""


@topics.command()
@click.option('--topic', '-t', required=True)
@click.option('--file', '-f', 'file_path')
@click.option('--message', '-m')
@click.option('--multi', is_flag=True)
@click.pass_obj
def produce(ctx, topic, message, file_path, multi):
    assert message or file_path
    if message:
        msg_string = message
    else:
        with open(file_path, 'r') as file_obj:
            msg_string = file_obj.read()
    if multi:
        for msg in msg_string.split('\n'):
            lib.send_message(ctx.url, ctx.admin_token, ctx.cert_file, topic, msg)
    else:
        lib.send_message(ctx.url, ctx.admin_token, ctx.cert_file, topic, msg_string)


@topics.command()
@click.option('--topic', '-t', required=True)
@click.option('--file-path', '-f', required=True)
@click.option('--subscription-name', '-n')
@click.option('--num-messages', '-m', default=1)
@click.option('--timeout-seconds', '-s', default=60)
@click.pass_obj
def sample(ctx, topic, file_path, subscription_name, num_messages, timeout_seconds):
    if not subscription_name:
        subscription_name = "pulsar_cli-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    lib.consume_messages(
        ctx.url, ctx.admin_token, ctx.cert_file, topic, subscription_name, num_messages, timeout_seconds, file_path
    )


@functions.command()
@click.pass_obj
def rebalance(ctx):
    result = PulsarAdmin.rebalance(ctx.api_url, ctx.admin_token)
    click.echo(result["result"])


def main():
    pulse(auto_envvar_prefix='PULSE')


if __name__ == "__main__":
    main()
