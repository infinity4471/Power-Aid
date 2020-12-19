import unittest
import cli
import click
from click.testing import CliRunner

runner = CliRunner()

class actualTotalLoad_testing( unittest.TestCase ):
    def test_request( self ):
        result = runner.invoke(cli.main, ['energy_group001', 'Login', '--username', 'admin', '--passw', 'nimda123'])
        token = result.output
        result = runner.invoke(cli.main, ['energy_group001', 'AggregatedGenerationPerType', '--area', 'Austria', '--productiontype', '1', '--timeres', 'PT60M', '--date', '2018-01-06'])
        self.assertNotEqual( result.output, 'No Data')
        self.assertNotEqual( result.output, 'Bad request')
        self.assertNotEqual( result.output, 'Not Authorized')
        result = runner.invoke(cli.main, ['energy_group001', 'Logout'])
        result = runner.invoke(cli.main, ['energy_group001', 'AggregatedGenerationPerType', '--area', 'Austria', '--productiontype', '1', '--timeres', 'PT60M', '--date', '2018-01-06'])
        self.assertEqual( result.output, 'Could not find token! Please try logging in!\n')


if __name__ == '__main__':
    unittest.main()
