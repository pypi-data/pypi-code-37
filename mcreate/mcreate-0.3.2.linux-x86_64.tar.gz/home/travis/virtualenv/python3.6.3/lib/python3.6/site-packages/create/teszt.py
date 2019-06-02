import click

@click.command()
@click.argument('project')
def create(project):
  print(f'Succesfully created {project}')

if __name__ == "__main__":
  create()