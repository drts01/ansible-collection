# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Carlos Meza <carlos@digitalr00ts.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Sample filter plugin for testing collection infrastructure."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def sample_filter(value):
    """
    Simple filter that prepends 'Hello, ' to the input value.

    Args:
        value (str): The input string to process

    Returns:
        str: The input string with 'Hello, ' prepended

    Examples:
        >>> sample_filter('world')
        'Hello, world'
        >>> sample_filter('ansible-creator')
        'Hello, ansible-creator'
    """
    return f"Hello, {value}"


class FilterModule:
    """Ansible filter plugin class."""

    def filters(self):
        """
        Return filter plugin mappings.

        Returns:
            dict: Dictionary mapping filter names to filter functions
        """
        return {
            "sample_filter": sample_filter,
        }
