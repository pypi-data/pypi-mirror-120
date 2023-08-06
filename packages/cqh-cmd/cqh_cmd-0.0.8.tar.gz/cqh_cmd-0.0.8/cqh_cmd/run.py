import datetime
import time
import click
import hashlib
import base64


@click.group()
def cli():
    pass


def raw_md5(text):
    h = hashlib.md5()
    h.update(text)
    return h.hexdigest()


@click.command()
@click.option("--text")
def md5(text):
    if not text:
        click.echo("`text` is required")
        return
    md5_value = raw_md5(text.encode("utf-8"))
    # print("md5_value:{}".format(md5_value.decode("utf-8")))
    click.echo("md5:")
    click.echo(md5_value)


@click.command()
@click.option("--method", default="md5")
@click.option("--len", default=16)
@click.option("--convert", default="lower")
@click.option("--verbose", default=0, type=int)
def key(method, len, convert, verbose):
    def echo(text):
        if verbose:
            click.echo(text)
    echo("method:{}, len:{}, convert:{}, verbose:{}".format(method, len, convert, verbose))
    method_dict = {
        "md5": lambda : raw_md5("{}".format(time.time()).encode("utf-8"))
    }
    raw_result = method_dict[method]()
    raw_result = raw_result[:len]
    convert_dict = {
        "lower": lambda x :x.lower(),
        "upper": lambda x: x.upper()
    }
    result =  convert_dict[convert](raw_result)
    click.echo("key:{}".format(result))

@click.command()
@click.option("--text")
@click.option("--format", default="%Y-%m-%d %H:%M:%S")
def from_ts(text, format):
    click.echo("text:{}, format:{}".format(text, format))
    now = datetime.datetime.now()
    click.echo("now time:{}".format(now.strftime(format)))
    convert_time = datetime.datetime.fromtimestamp(float(text))
    click.echo("convert time:{}".format(convert_time.strftime(format)))

@click.command()
@click.option("--text")
def from_base64(text):
    val = base64.b64decode(text)
    click.echo("raw_value:{}".format(val))
@click.command()
@click.option("--text")
def to_base64(text):
    val = base64.b64encode(text.encode("utf-8"))
    click.echo("base64:{}".format(val))

    

cli.add_command(md5)
cli.add_command(key)
cli.command(from_ts)
cli.add_command(from_base64)
cli.add_command(to_base64)


if __name__ == "__main__":
    cli()
