from kenna.api import Kenna

import click
import hodgepodge.types
import hodgepodge.click
import json


@click.group()
@click.option('--connector-ids')
@click.option('--connector-names')
@click.pass_context
def connectors(ctx, connector_ids: str, connector_names: str):
    api = ctx.obj['kenna_api']
    assert isinstance(api, Kenna)

    ctx.obj.update({
        'connector_ids': hodgepodge.click.str_to_list_of_int(connector_ids),
        'connector_names': hodgepodge.click.str_to_list_of_str(connector_names),
    })


@connectors.command()
@click.pass_context
def count_connectors(ctx):
    api = ctx.obj['kenna_api']
    assert isinstance(api, Kenna)

    rows = api.iter_connectors(
        connector_ids=ctx.obj['connector_ids'],
        connector_names=ctx.obj['connector_names'],
    )
    n = sum(1 for _ in rows)
    click.echo(n)


@connectors.command()
@click.option('--limit', type=int)
@click.pass_context
def get_connectors(ctx, limit):
    api = ctx.obj['kenna_api']
    assert isinstance(api, Kenna)

    rows = api.iter_connectors(
        connector_ids=ctx.obj['connector_ids'],
        connector_names=ctx.obj['connector_names'],
        limit=limit,
    )
    for row in rows:
        row = hodgepodge.types.dict_to_json(row)
        click.echo(row)
