
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import simpledialog, messagebox
from firewall import *

class TestFirewallApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = FirewallApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch.object(simpledialog, 'askinteger', return_value=8080)
    @patch.object(messagebox, 'showinfo')
    def test_add_rule(self, mock_showinfo, mock_askinteger):
        self.app.add_rule()
        mock_askinteger.assert_called_once_with("Add Rule", "Enter port number:")
        mock_showinfo.assert_called_once_with("Success", "Rule added: allow 8080")

    @patch.object(simpledialog, 'askinteger', return_value=8080)
    @patch.object(messagebox, 'showinfo')
    def test_block_rule(self, mock_showinfo, mock_askinteger):
        self.app.block_rule()
        mock_askinteger.assert_called_once_with("Block Rule", "Enter port number:")
        mock_showinfo.assert_called_once_with("Success", "Rule added: deny 8080")

    @patch.object(messagebox, 'showinfo')
    @patch.object(subprocess, 'run')
    def test_enable_firewall(self, mock_run, mock_showinfo):
        self.app.enable_firewall()
        mock_run.assert_called_once_with(["sudo", "ufw", "enable"], capture_output=True, text=True, check=True)
        mock_showinfo.assert_called_once_with("Success", "Firewall enabled")

    @patch.object(messagebox, 'showinfo')
    @patch.object(subprocess, 'run')
    def test_disable_firewall(self, mock_run, mock_showinfo):
        self.app.disable_firewall()
        mock_run.assert_called_once_with(["sudo", "ufw", "disable"], capture_output=True, text=True, check=True)
        mock_showinfo.assert_called_once_with("Success", "Firewall disabled")

    @patch('subprocess.run')
    @patch.object(messagebox, 'showinfo')
    def test_run_ufw_command_success(self, mock_showinfo, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=['sudo', 'ufw', 'some_command'],
            stdout="Command Result",
            stderr="",
            returncode=0
        )

        result = self.app.run_ufw_command("some_command", "Success Message")

        mock_run.assert_called_once_with(['sudo', 'ufw', 'some_command'], capture_output=True, text=True, check=True)
        mock_showinfo.assert_called_once_with("Success", "Success Message")
        self.assertEqual(result, "Command Result")
    
    
    @patch.object(messagebox, 'showinfo')
    @patch('subprocess.run')
    def test_show_rules(self, mock_run, mock_showinfo):
        # Assuming your `run_ufw_command` method returns "Rules output" for "status verbose"
        mock_run.return_value = MagicMock(
            stdout="Rules output",
            stderr="",
            returncode=0
        )

        with patch('subprocess.run', mock_run):
            self.app.show_rules()

        mock_run.assert_called_once_with(["sudo", "ufw", "status", 'verbose'], capture_output=True, text=True, check=True)
        mock_showinfo.assert_called_once_with("UFW Rules", "Rules output")

if __name__ == '__main__':
    unittest.main()
