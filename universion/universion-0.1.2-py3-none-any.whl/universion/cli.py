import click
import pkg_resources

versionStr = pkg_resources.require("universion")[0].version

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True)
def cli(version):
	if version:
		click.echo(f'universion {versionStr}')

@cli.group(help='Bump the version of a project.')
def bump():
	pass

tagHelp = 'Create and commit a git tag for this version.'
tagFlag = '--tag'
tagF = '-t'

jsonHelp = 'Create a json file containing the new version.'
jsonFlag = '--json'
jsonF = '-j'

@bump.command(help='Bump version of a python project (setup.py).')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option(jsonFlag, jsonF, is_flag=True, help=jsonHelp)
def python(tag, json):
	click.echo('Not Implemented')

@bump.command(help='Bump version of a dotnet core project (*.csproj).')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option(jsonFlag, jsonF, is_flag=True, help=jsonHelp)
def netcore(tag, json):
	click.echo('Not Implemented')

@bump.command(help='Bump version of a .net framework project (AssemblyInfo.cs).')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option(jsonFlag, jsonF, is_flag=True, help=jsonHelp)
def net(tag, json):
	click.echo('Not Implemented')

@bump.command(help='Bump version of a nodejs project (package.json).')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option(jsonFlag, jsonF, is_flag=True, help=jsonHelp)
def node(tag, json):
	click.echo('Not Implemented')

@bump.command(help='Bump version stored in a json file.')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option('--filename', '-f', required=False, type=str, default='version.json', help='Use a filename other than version.json')
def json(tag, filename):
	click.echo('Not Implemented')

@bump.command(help='Bump version stored in a flat file.')
@click.option(tagFlag, tagF, is_flag=True, help=tagHelp)
@click.option('--filename', '-f', required=False, type=str, default='VERSION', help='Use a filename other than VERSION')
def flat(tag, filename):
	click.echo('Not Implemented')

@cli.command(help='Generate a changelog based on commit history.')
@click.option('--allcommits', '-a', is_flag=True, help='Use all commits whether or not they conform to conventional commits.')
@click.option('--template', '-t', required=False, type=str, help='Use a custom template for the changelog.')
def changelog(allcommits, template):
	click.echo('Not Implemented')

if __name__ == '__main__':
	cli()
