#!/usr/bin/env python


from unittest import TestCase
import switch_pane


class Tester(TestCase):

    def test_parse_title(self):
        old_bash = switch_pane.bash
        try:
            switch_pane.bash = lambda *args, **kwargs: 'bash'
            name, pane_id, window_id = switch_pane.parse_title()
            self.assertEqual(name, 'bash')
            self.assertEqual(pane_id, None)
            self.assertEqual(window_id, None)

            switch_pane.bash = lambda *args, **kwargs: 'bash@1'
            name, pane_id, window_id = switch_pane.parse_title()
            self.assertEqual(name, 'bash')
            self.assertEqual(pane_id, 1)
            self.assertEqual(window_id, None)

            switch_pane.bash = lambda *args, **kwargs: 'bash@1@2'
            name, pane_id, window_id = switch_pane.parse_title()
            self.assertEqual(name, 'bash')
            self.assertEqual(pane_id, 1)
            self.assertEqual(window_id, 2)
        finally:
            switch_pane.bash = old_bash

    def test_get_next_window_id(self):
        old_get_window_ids = switch_pane.get_window_ids
        try:
            switch_pane.get_window_ids = lambda: [0, 1, 2, 3]
            result = switch_pane.get_next_window_id(1)
            self.assertEqual(result, 2)
            result = switch_pane.get_next_window_id(3)
            self.assertEqual(result, 1)
            result = switch_pane.get_next_window_id(4)
            self.assertEqual(result, 1)
            switch_pane.get_window_ids = lambda: [0, 1, 2, 3, 8]
            result = switch_pane.get_next_window_id(4)
            self.assertEqual(result, 8)
            switch_pane.get_window_ids = lambda: [0, 1]
            result = switch_pane.get_next_window_id(1)
            self.assertEqual(result, None)
        finally:
            switch_pane.get_window_ids = old_get_window_ids

