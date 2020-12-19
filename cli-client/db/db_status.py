import requests
import click

def healthCheck():
    req = requests.get("http://localhost:8765/energy/api/HealthCheck")
    try:
        click.echo(req.text)
    except EnvironmentError:
        click.echo("Could not receive response")

def reset():
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
    except EnvironmentError:
        click.echo("Could not find token! Please try logging in!")
        return
    req = requests.post("http://localhost:8765/energy/api/Reset", headers = { "X-OBSERVATORY-AUTH": token } )
    try:
        click.echo(req.text)
    except EnvironmentError:
        click.echo("Could not receive response")
