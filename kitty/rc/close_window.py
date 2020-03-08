#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>


from typing import TYPE_CHECKING

from .base import (
    MATCH_WINDOW_OPTION, ArgsType, Boss, MatchError, PayloadGetType,
    PayloadType, RCOptions, RemoteCommand, ResponseType, Window
)

if TYPE_CHECKING:
    from kitty.cli_stub import CloseWindowRCOptions as CLIOptions


class CloseWindow(RemoteCommand):
    '''
    match: Which window to close
    self: Boolean indicating whether to close the window the command is run in
    '''

    short_desc = 'Close the specified window(s)'
    options_spec = MATCH_WINDOW_OPTION + '''\n
--self
type=bool-set
If specified close the window this command is run in, rather than the active window.
'''
    argspec = ''

    def message_to_kitty(self, global_opts: RCOptions, opts: 'CLIOptions', args: ArgsType) -> PayloadType:
        return {'match': opts.match, 'self': opts.self}

    def response_from_kitty(self, boss: 'Boss', window: 'Window', payload_get: PayloadGetType) -> ResponseType:
        match = payload_get('match')
        if match:
            windows = tuple(boss.match_windows(match))
            if not windows:
                raise MatchError(match)
        else:
            windows = [window if window and payload_get('self') else boss.active_window]
        for window in windows:
            if window:
                boss.close_window(window)


close_window = CloseWindow()
