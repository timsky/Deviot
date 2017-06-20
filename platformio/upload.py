#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from sys import exit

from .initialize import Initialize
from ..libraries.tools import get_setting, save_setting
from ..libraries.thread_progress import ThreadProgress
from ..libraries.I18n import I18n

_ = I18n

class Upload(Initialize):
    def __init__(self):
        super(Upload, self).__init__()

        global _
        _ = I18n().translate

        self.nonblock_upload()

    def start_upload(self):
        """Upload
        
        Run the upload platformio command checking if a board (environment)
        and a serial port is selected
        """
        if(not self.check_main_requirements()):
            exit(0)

        save_setting('last_action', self.UPLOAD)

        # check board selected or make select it
        self.check_board_selected()
        if(not self.board_id):
            self.derror("select_board_list")
            return

        # check port selected or make select it
        self.check_port_selected()
        if(not self.port_id):
            self.derror("select_port_list")
            return

        # initialize board if it's not
        self.add_board()

        # add extra library board
        self.add_extra_library()

        # check if there is a programmer selected
        self.programmer()
        programmer = get_setting('programmer_id', None)

        if(programmer):
            cmd = ['run', '-t', 'program', '-e', self.board_id]
        else:
            cmd = ['run', '-t', 'upload', '--upload-port', self.port_id, '-e', self.board_id]
        
        out = self.run_command(cmd)

        self.dstop()
        save_setting('last_action', None)

    def nonblock_upload(self):
        """New Thread Execution
        
        Starts a new thread to run the start_upload method
        """
        from threading import Thread

        thread = Thread(target=self.start_upload)
        thread.start()
        ThreadProgress(thread, _('processing'), '')
