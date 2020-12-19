import unittest
import cli
import click
from click.testing import CliRunner

runner = CliRunner()

class admin_testing( unittest.TestCase ):
    def test_adminRequest( self ):
        result = runner.invoke(cli.main, ['energy_group001', 'Login', '--username', 'admin', '--passw', 'nimda123'])
        token = result.output
        result = runner.invoke(cli.main, ['energy_group001', 'Admin', '--newuser', 'tester', '--passw', 'password', '--email', 'test@test.gr', '--quota', '0', '--admin', 'False'])
        self.assertNotEqual( result.output, 'Bad request')
        self.assertNotEqual( result.output, 'Not Authorized')
        result = runner.invoke(cli.main, ['energy_group001', 'Logout'])

if __name__ == '__main__':
    unittest.main()