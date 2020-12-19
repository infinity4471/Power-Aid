import click
import datetime

from data import request_data
from data.global_data_cli import *
from usr import *
from db import *

@click.group()
def main():
    pass

@main.command('energy_group001')
@click.argument('scope')
@click.option('--area')
@click.option('--timeres')
@click.option('--productiontype')
@click.option('--date')
@click.option('--month')
@click.option('--year')
@click.option('--format')
@click.option('--newuser')
@click.option('--moduser')
@click.option('--passw')
@click.option('--email')
@click.option('--quota')
@click.option('--username')
@click.option('--userstatus')
@click.option('--newdata')
@click.option('--source')

def data(scope,area,timeres,productiontype,date,month,year,format,newuser,moduser,username,passw,email,quota,userstatus,newdata,source ):
    if not connected("http://localhost:8765"):
        click.echo("Received Exception while connecting. Perharps server is down")
        return
    if scope in scopes:
        if not date is None:
            param = "date"
        elif not month is None:
            param = "month"
            date = month
        elif not year is None:
            param = "year"
            date = year
        else:
            click.echo("Please specify date!")
            return
        if scope == scopes[ 1 ]: #AggregatedGenerationPerType requires productiontype
            param_list = [ scope, area, productiontype, timeres, param, date ]
        else:
            param_list = [ scope, area, timeres, param, date ]
        request_data( param_list, format )
    elif scope == 'Admin':
        admin_params = [passw, email, quota, userstatus, newdata, source]
        if newuser is not None:
            click.echo( add_user( newuser, passw, email, quota ) )
        elif moduser is not None:
            click.echo( modify_user( moduser, passw, email, quota ) )
        elif userstatus is not None:
            click.echo( user_status( userstatus ) )
        elif newdata is not None:
            click.echo( new_data( newdata, source ) )
        else:
            click.echo("Did not specify function")
    elif scope == "Login":
        click.echo( login( username, passw ) )
    elif scope == "Logout":
        click.echo( logout() )
    elif scope == "HealthCheck":
        click.echo( healthCheck() )
    elif scope == "Reset":
        click.echo( reset() )
    else:
        click.echo("Invalid scope: %s" % scope )

if __name__=="__main__": 
    main()
