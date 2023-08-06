import logging
import os

import click
from requests import Session

from glean.credentials import parse_credentials
from glean.glean_api import (
    build_details_uri,
    create_build_from_git_revision,
    create_build_from_local_files,
    login,
    preview_uri,
)

DEBUG = os.environ.get("DEBUG")


git_revision_option = click.option(
    "--git-revision",
    type=str,
    required=False,
    help="""
    If specified, Glean will pull configuration files from your configured git repository at the provided commit,
    instead of using local files.
    """,
)
path_argument = click.argument("filepath", type=click.Path(exists=True), default=".")


@click.group()
@click.option(
    "--credentials-filepath",
    type=str,
    default="~/.glean/glean_access_key.json",
    show_default=True,
    help="Path to your Glean access key credentials. You can also control this by setting a "
    "GLEAN_CREDENTIALS_FILEPATH environment variable.",
    envvar="GLEAN_CREDENTIALS_FILEPATH",
)
@click.pass_context
def cli(ctx, credentials_filepath):
    """A command-line interface for interacting with Glean."""
    if DEBUG:
        _enable_http_logging()

    ctx.ensure_object(dict)
    ctx.obj["credentials"] = parse_credentials(os.path.expanduser(credentials_filepath))


@cli.command()
@git_revision_option
@path_argument
@click.pass_context
def preview(ctx, git_revision, filepath):
    """Validates resource configurations and generates a preview link."""
    click.echo("Creating preview build...")

    build_results = _create_build_using_options(
        ctx, git_revision, filepath, deploy=False
    )
    _echo_build_results(build_results, False)


@cli.command()
@git_revision_option
@path_argument
@click.option(
    "--preview / --no-preview",
    default=True,
    help="Whether to generate a Preview Build before deploying.",
)
@click.pass_context
def deploy(ctx, git_revision, preview, filepath):
    """Validates and deploys resource configurations to your project."""
    if preview:
        click.echo("Creating preview build...")
        build_results = _create_build_using_options(
            ctx, git_revision, filepath, deploy=False
        )
        _echo_build_results(build_results, False)
        click.echo("")
        if not click.confirm("Continue with deploy?"):
            exit(1)

    click.echo("Creating deploy build...")
    build_results = _create_build_using_options(
        ctx, git_revision, filepath, deploy=True
    )
    _echo_build_results(build_results, True)
    click.echo("")
    click.echo(click.style("Deploy complete.", fg="bright_green"))


def _create_build_using_options(ctx, git_revision=None, filepath=None, deploy=False):
    s = Session()
    project_id = login(s, ctx.obj["credentials"])
    if git_revision:
        return create_build_from_git_revision(s, project_id, git_revision, deploy)
    else:
        return create_build_from_local_files(s, project_id, filepath, deploy)


def _echo_build_results(build_results, deploy):
    """Outputs user-friendly build results."""
    if "errors" in build_results and build_results["errors"]:
        _echo_build_errors_and_exit(
            [
                e["extensions"]["userMessage"]
                for e in build_results["errors"]
                if "extensions" in e and "userMessage" in e["extensions"]
            ]
        )

    created_build_results = build_results["data"]["createBuild"]
    if created_build_results["errors"]:
        _echo_build_errors_and_exit(created_build_results["errors"])

    click.echo(
        click.style("Build ", fg="bright_green")
        + click.style(created_build_results["id"], bold=True)
        + click.style(" created successfully.", fg="bright_green")
    )
    click.echo("")

    if created_build_results["warnings"]:
        _echo_build_warnings(created_build_results["warnings"])

    _echo_build_resources(created_build_results["resources"], deploy)
    click.echo("")
    click.echo(f"Details: {build_details_uri(build_results)}")
    if not deploy:
        click.echo(f"Preview: {preview_uri(build_results)}")


def _echo_build_errors_and_exit(errors):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("  Errors encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Glean for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.secho("Build failed.", fg="red")
    exit(1)


def _echo_build_warnings(warnings):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    click.echo("  Warnings encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    if not warnings:
        warnings = ["Warning message missing, please contact Glean for support."]
    _echo_list(warnings, color="yellow")
    click.echo("")


def _echo_build_resources(resources, deploy):
    added_styled = click.style("(added)   " if deploy else "(will add)    ", fg="green")
    updated_styled = click.style(
        "(updated) " if deploy else "(will update) ", fg="cyan"
    )
    deleted_styled = click.style("(deleted) " if deploy else "(will delete) ", fg="red")

    click.secho("Models", bold=True)
    _echo_list([added_styled + f"{r['name']}" for r in resources["added"]["models"]])
    _echo_list(
        [updated_styled + f"{r['name']}" for r in resources["updated"]["models"]]
    )
    _echo_list(
        [deleted_styled + f"{r['name']}" for r in resources["deleted"]["models"]]
    )
    click.secho("Views", bold=True)
    _echo_list(
        [added_styled + f"{r['name']}" for r in resources["added"]["savedViews"]]
    )
    _echo_list(
        [updated_styled + f"{r['name']}" for r in resources["updated"]["savedViews"]]
    )
    _echo_list(
        [deleted_styled + f"{r['name']}" for r in resources["deleted"]["savedViews"]]
    )


def _echo_list(items, color="white"):
    for item in items:
        lines = item.split("\n")
        click.echo(click.style("*", fg=color) + "  " + lines[0])
        for line in lines[1:]:
            click.echo("   " + line)


def _enable_http_logging():
    # From: https://docs.python-requests.org/en/master/api/#api-changes
    from http.client import HTTPConnection

    HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
