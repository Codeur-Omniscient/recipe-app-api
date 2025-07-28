"""
Test custom Django managment commands.
"""
# patch va nous permettre de mock notre base de donnée
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command  # Fixed typo here
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the db if db is ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the db if db is not ready"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        """ On mocke l'erreur Psycopg2Error 2 fois,
              puis l'erreur OperationalError 3 fois,
              et enfin True 1 fois.
             Cela simule une situation où la base de données est en train de
             se lancer, mais pas encore prête.
             Après 5 secondes, la base de données devrait être prête, et la
             commande wait_for_db devrait se terminer avec succès."""

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
