import os
import tempfile
from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import List, Optional

import sagemaker
import typer
from huggingface_hub import HfFolder
from sagemaker.huggingface import HuggingFace

app = typer.Typer()


def get_sagemaker_role(arn=None):
    try:
        role = arn or sagemaker.get_execution_role()
    except ValueError:
        # TODO - maybe auth with boto3 here via role name.
        if arn is None:
            raise RuntimeError(
                "Could not determine sagemaker execution role automatically.\n\nThis probably means you're running this script outside of a Sagemaker Studio Notebook.\n"
                "To resolve this issue, please provide a valid ARN to the --role flag or set it as the SAGEMAKER_ROLE_ARN environment variable."
            )
    return role


@app.command(name='run', context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def run(
    ctx: typer.Context,
    script: Path,
    role: str = typer.Option(
        os.getenv("SAGEMAKER_ROLE_ARN"),
        help="Arn of role with access to sagemaker.",
    ),
    wait: bool = typer.Option(True, help="Whether to wait and view logs or run the script async"),
    dependencies: Optional[List[Path]] = typer.Option([]),
    exclude: Optional[List[str]] = typer.Option(
        None,
        help="Exclude patterns when copying example folder to tmp folder for launch. You can add multiple. Ex: fuego run --exclude '*.zip' --exclude 'big_file.jsonl' your_script.py [SCRIPT-ARGS]",
    ),
    instance_type: str = typer.Option('ml.g4dn.xlarge'),
    use_latest_transformers: bool = typer.Option(True),
    use_latest_datasets: bool = typer.Option(False),
    use_latest_hf_hub: bool = typer.Option(False),
):

    source_dir = Path(script).absolute().parent

    transformers_examples_reqs = source_dir.parent / '_tests_requirements.txt'
    if transformers_examples_reqs.exists() and transformers_examples_reqs not in dependencies:
        typer.echo(f"- 👋 hey there - we're adding _tests_requirements.txt to dependencies list")
        dependencies = [transformers_examples_reqs] + list(dependencies)

    default_reqs = source_dir / 'requirements.txt'
    if default_reqs.exists() and default_reqs not in dependencies:
        typer.echo(f"- 👋 hey there - we found requirements.txt and we're adding to dependencies list")
        dependencies += [default_reqs]

    if not dependencies:
        typer.echo(f"No requirements given!")

    requirements = []
    for f in dependencies:
        f = Path(f)
        assert f.exists(), f"Given requirements file '{f}' not found."
        requirements += f.read_text().strip().split('\n')

    if use_latest_transformers:
        requirements += ['git+git://github.com/huggingface/transformers@master']

    if use_latest_datasets:
        requirements += ['git+git://github.com/huggingface/datasets@master']

    if use_latest_hf_hub:
        requirements += ['git+git://github.com/huggingface/huggingface_hub@main']

    hyperparameters = {'push_to_hub_token': HfFolder.get_token()}
    for i in range(0, len(ctx.args), 2):
        hyperparameters[ctx.args[i].replace('-', '')] = ctx.args[i + 1]

    assert Path(script).exists(), f"Given script to run '{script}' does not exist."
    ignore = None if not exclude else ignore_patterns(*exclude)
    with tempfile.TemporaryDirectory() as tmp:
        save_dir = Path(tmp) / source_dir.name
        copytree(source_dir, save_dir, ignore=ignore)
        requirements_file = save_dir / 'requirements.txt'
        requirements_file.write_text('\n'.join(requirements))

        typer.echo('-' * 40)

        typer.echo(f"👀 - entrypoint: {script.name}")
        typer.echo(f"👀 - source_dir: {str(save_dir)}")
        typer.echo(f"👀 - instance type: {instance_type}")
        typer.echo(f"👀 - role: {get_sagemaker_role(role)}")
        typer.echo(f"👀 - hparams: {hyperparameters}")
        typer.echo(f"👀 - dependencies: {[str(requirements_file)]}")
        typer.echo("\n👀 Files to push to Sagemaker ⤵️")
        print('\n'.join([str(x) for x in save_dir.glob('**/*')]))

        typer.echo('-' * 40)

        huggingface_estimator = HuggingFace(
            entry_point=script.name,
            source_dir=str(save_dir),
            instance_type=instance_type,
            instance_count=1,
            role=get_sagemaker_role(role),
            transformers_version='4.6',
            pytorch_version='1.7',
            py_version='py36',
            hyperparameters=hyperparameters,
            dependencies=[str(requirements_file)],
        )
        huggingface_estimator.fit(wait=wait)


@app.command(name='hello')
def say_hi(
    name: Optional[str] = 'world',
):
    typer.echo(f"Hey there, {name}!")
