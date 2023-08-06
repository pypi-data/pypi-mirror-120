import click
import requests


url = 'https://global-trie-cli.herokuapp.com/updatetrie/'

@click.group()
def main():
    pass

@main.command()
def list():
    response = requests.get(url+'list')
    click.echo(response.text)

@main.command()
@click.argument('word')
def check(word):
    response = requests.get(url + 'check/'+word)
    click.echo(response.text)

@main.command()
@click.argument('prefix')
def recommend(prefix):
    response = requests.get(url+'recommend/'+prefix)
    click.echo(response.text)

@main.command()
@click.argument('word')
def remove(word):
    try:
        response = requests.get(url+'remove/'+word)
        click.echo(response.text)
    except:
        click.echo('Word does not exist in Trie!')

@main.command()
@click.argument('word')
def add(word):
    response = requests.get(url+'add/'+word)
    click.echo(response.text)

if __name__ == '__main__':
    main()