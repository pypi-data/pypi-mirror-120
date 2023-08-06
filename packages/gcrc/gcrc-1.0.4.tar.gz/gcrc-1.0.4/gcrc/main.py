import re
from datetime import datetime, timedelta, timezone

import typer

from gcrc import gcloud
from gcrc.gcloud import ImageTag
from gcrc.settings import conf

DT_FORMAT = "%Y-%m-%d"
KEEP_EXTRAS: dict[str, re.Pattern] = {val: re.compile(val) for val in conf.KEEP_EXTRA}
_BEFORE = None
app = typer.Typer()


def _get_before():
    global _BEFORE
    if not _BEFORE:
        _BEFORE = datetime.now(timezone.utc) - timedelta(days=-conf.KEEP_TAGS_DAYS)

    return _BEFORE


def _pick_cleanup_tags(tags: list[ImageTag]) -> (list[ImageTag], list[ImageTag]):
    """
    Figure out which tags to keep and which to clean up, based on

    1) age - "KEEP_TAGS_DAYS"
    2) important tags - "KEEP_EXTRA"
    3) minimum limits - "KEEP_TAGS_MIN"

    Will not always clean up everything that could be cleaned up, but
    guarantees the desired things are always kept.
    """
    keep = []
    clean = []
    extras = {}
    before = _get_before()

    # Process latest first
    for tag in sorted(tags, key=lambda t: t.timestamp, reverse=True):
        keep_this = False

        # Keep recent items
        if tag.timestamp >= before:
            keep_this = True

        # Keep extras
        for key, regex in KEEP_EXTRAS.items():
            for t in tag.tags:
                if regex.match(t):
                    extras[key] = extras.get(key, []) + [tag]
                    if len(extras[key]) <= conf.KEEP_TAGS_MIN:
                        keep_this = True

        # Keep minimum X items
        if len(keep) < conf.KEEP_TAGS_MIN:
            keep_this = True

        if keep_this:
            keep.append(tag)
        else:
            clean.append(tag)

    return keep, clean


@app.command()
def list_images(gcr_repo: str):
    """
    List information about all the images on the repository
    """
    typer.echo(
        typer.style(
            f" ----- {gcr_repo} images ----- ", fg=typer.colors.GREEN, bold=True
        )
    )
    for image in gcloud.list_images(gcr_repo):
        typer.echo(image)


@app.command()
def image_info(gcr_repo: str):
    """
    Display some current statistics on the repository
    """
    images = gcloud.list_images(gcr_repo)

    for image in images:
        tags = gcloud.list_tags(image)

        image_name = typer.style(
            image.removeprefix(gcr_repo + "/"), fg=typer.colors.BLUE
        )

        if not tags:
            ok = typer.style("EMPTY", fg=typer.colors.GREEN)
            typer.echo(f"{image_name} | {ok} | No tags found, nothing to do.")
            continue

        oldest_ts = None
        oldest_tag = None
        latest_ts = None
        latest_tag = None

        for tag in tags:
            if oldest_ts is None or tag.timestamp < oldest_ts:
                oldest_ts = tag.timestamp
                oldest_tag = tag.name
            if latest_ts is None or tag.timestamp > latest_ts:
                latest_ts = tag.timestamp
                latest_tag = tag.name

        keep, clean = _pick_cleanup_tags(tags)

        count = typer.style(f"{len(clean)}/{len(tags)}", fg=typer.colors.CYAN)
        oldest = typer.style(
            f"{oldest_ts.strftime(DT_FORMAT)} ({oldest_tag})", fg=typer.colors.MAGENTA
        )
        latest = typer.style(
            f"{latest_ts.strftime(DT_FORMAT)} ({latest_tag})", fg=typer.colors.MAGENTA
        )
        ok = (
            typer.style("NEEDS CLEANUP", fg=typer.colors.BRIGHT_RED)
            if clean
            else typer.style("OK", fg=typer.colors.GREEN)
        )

        typer.echo(
            f"{image_name} | {ok} | {count} images to clean | {oldest} - {latest}"
        )


@app.command()
def cleanup(gcr_repo: str):
    """
    Clean up some of the unneeded images
    """
    images = gcloud.list_images(gcr_repo)
    for image in images:
        typer.echo(typer.style(image, fg=typer.colors.BRIGHT_CYAN, bold=True))
        typer.echo(
            typer.style("-" * len(image), fg=typer.colors.BRIGHT_CYAN, bold=True)
        )
        typer.echo("")

        tags = gcloud.list_tags(image)
        keep, clean = _pick_cleanup_tags(tags)

        for tag in clean:
            typer.echo(
                typer.style(
                    f"Removing {', '.join(tag.tags)} from {tag.timestamp.strftime(DT_FORMAT)}",
                    fg=typer.colors.BRIGHT_YELLOW,
                )
            )
            # gcloud.delete_tag(image, tag)

        if clean:
            typer.echo("")

        for tag in keep:
            typer.echo(
                typer.style(
                    f"Keeping {tag.name} from {tag.timestamp.strftime(DT_FORMAT)}",
                    fg=typer.colors.BRIGHT_GREEN,
                )
            )

        typer.echo("")
