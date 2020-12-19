from .Exception import BadRequest, NotAuthorized, OutOfQuota, NoData
import click
import requests

def request_data( parameters, format ):
    final_url = "http://localhost:8765/energy/api"
    for param in parameters:
        if param is None:
            click.echo("Invalid Parameters")
            return
        final_url += "/" + param
    if format is not None:
        final_url += "?format=" + format
    try:
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
            print("token")
    except EnvironmentError:
        click.echo("Could not find token! Please try logging in!")
        return
    if len(token) == 0:
        click.echo("Invalid request: token not found")
        return
    try:
        response = requests.get( final_url, headers = { "X-OBSERVATORY-AUTH": token } )
        if response.status_code == 400:
            raise BadRequest
        elif response.status_code == 401:
            raise NotAuthorized
        elif response.status_code == 402:
            raise OutOfQuota    
        elif response.status_code == 403:
            raise NoData
        if format != 'csv':
            response = response.json()
            for packet in response:
                click.echo( packet )
                click.echo('\n')
        else:
            click.echo( response.text )
    except OutOfQuota:
        click.echo("Out of Quota")
    except NoData:
        click.echo("No Data")
    except NotAuthorized:
        click.echo("Not Authorized: check that your token is valid")
    except BadRequest:
        click.echo("Bad Request")
