from PyQt4 import QtGui, QtCore
import string

import config
import kconfig
import dtree
from pickle_util import PickleUtil
import os

from widgets import ClockWidgit, HistogramWidget, VerticalSeparator, HorizontalSeparator


# noinspection PyArgumentList
class MainWindow(QtGui.QMainWindow):

    def __init__(self, screen_res):
        super(MainWindow, self).__init__()

        self.screen_res = screen_res
        # Load User Preferences

    def init_ui(self):
        self.mainWidgit = MainKeyboardWidget(self, self.key_chars, self.screen_res)
        self.mainWidgit.init_ui()
        self.setCentralWidget(self.mainWidgit)
        self.clock_text_align('auto', message=False)

        # File Menu Actions
        restart_action = QtGui.QAction('&Restart', self)
        restart_action.setShortcut('Ctrl+R')
        restart_action.setStatusTip('Restart application')
        # restart_action.triggered.connect(self.restartEvent)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        # exit_action.triggered.connect(QtGui.qApp.quit)
        exit_action.triggered.connect(self.closeEvent)

        # Clock Menu Actions
        self.high_contrast_action = QtGui.QAction('&High Contrast Mode', self, checkable=True)
        self.high_contrast_action.triggered.connect(lambda: self.high_contrast_event())

        self.default_clock_action = QtGui.QAction('&Default (Clock)', self, checkable=True)
        self.default_clock_action.setStatusTip('Regular Nomon clock with sweeping minute hand')
        self.default_clock_action.triggered.connect(lambda: self.clock_change_event('default'))
        self.default_clock_action.setIcon(QtGui.QIcon(os.path.join("icons/", 'default.png')))

        self.radar_clock_action = QtGui.QAction('&Radar (Clock)', self, checkable=True)
        self.radar_clock_action.setStatusTip('Nomon clock with sweeping minute hand and radar trails')
        self.radar_clock_action.triggered.connect(lambda: self.clock_change_event('radar'))
        self.radar_clock_action.setIcon(QtGui.QIcon(os.path.join("icons/", 'radar.png')))

        self.ball_clock_action = QtGui.QAction('&Ball (Filling)', self, checkable=True)
        self.ball_clock_action.triggered.connect(lambda: self.clock_change_event('ball'))
        self.ball_clock_action.setIcon(QtGui.QIcon(os.path.join("icons/", 'ball.png')))

        self.pacman_clock_action = QtGui.QAction('&Pac Man (Filling Pac Man)', self, checkable=True)
        self.pacman_clock_action.triggered.connect(lambda: self.clock_change_event('pac man'))
        self.pacman_clock_action.setIcon(QtGui.QIcon(os.path.join("icons/", 'pac_man.png')))

        self.bar_clock_action = QtGui.QAction('&Progress Bar', self, checkable=True)
        self.bar_clock_action.triggered.connect(lambda: self.clock_change_event('bar'))
        self.bar_clock_action.setIcon(QtGui.QIcon(os.path.join("icons/", 'bar.png')))

        # Font Menu Actions
        self.small_font_action = QtGui.QAction('&Small', self, checkable=True)
        self.small_font_action.triggered.connect(lambda: self.change_font_size('small'))

        self.med_font_action = QtGui.QAction('&Medium (Default)', self, checkable=True)
        self.med_font_action.triggered.connect(lambda: self.change_font_size('med'))

        self.large_font_action = QtGui.QAction('&Large', self, checkable=True)
        self.large_font_action.triggered.connect(lambda: self.change_font_size('large'))

        # Text Menu Actions
        self.auto_text_align_action = QtGui.QAction('&Auto (Recommended)', self, checkable=True)
        self.auto_text_align_action.triggered.connect(lambda: self.clock_text_align('auto'))

        self.tc_text_align_action = QtGui.QAction('&Top Center', self, checkable=True)
        self.tc_text_align_action.triggered.connect(lambda: self.clock_text_align('tc'))

        self.cl_text_align_action = QtGui.QAction('&Center Left', self, checkable=True)
        self.cl_text_align_action.triggered.connect(lambda: self.clock_text_align('cl'))

        self.cc_text_align_action = QtGui.QAction('&Center', self, checkable=True)
        self.cc_text_align_action.triggered.connect(lambda: self.clock_text_align('cc'))

        self.cr_text_align_action = QtGui.QAction('&Center Right', self, checkable=True)
        self.cr_text_align_action.triggered.connect(lambda: self.clock_text_align('cr'))

        self.bc_text_align_action = QtGui.QAction('&Bottom Center', self, checkable=True)
        self.bc_text_align_action.triggered.connect(lambda: self.clock_text_align('bc'))

        # Keyboard Layout Menu Actions
        self.default_layout_action = QtGui.QAction('&Alphabetical (Default)', self, checkable=True)
        self.default_layout_action.triggered.connect(lambda: self.layout_change_event('alphabetical'))

        self.qwerty_layout_action = QtGui.QAction('&QWERTY', self, checkable=True)
        self.qwerty_layout_action.triggered.connect(lambda: self.layout_change_event('qwerty'))

        # Word Count Action
        self.high_word_action = QtGui.QAction('&High (Default)', self, checkable=True)
        self.high_word_action.triggered.connect(lambda: self.word_change_event('high'))

        self.low_word_action = QtGui.QAction('&Low (5 Words)', self, checkable=True)
        self.low_word_action.triggered.connect(lambda: self.word_change_event('low'))

        self.off_word_action = QtGui.QAction('&Off', self, checkable=True)
        self.off_word_action.triggered.connect(lambda: self.word_change_event('off'))

        # Tools Menu Actions
        self.profanity_filter_action = QtGui.QAction('&Profanity Filter', self, checkable=True)
        self.profanity_filter_action.triggered.connect(self.profanity_filter_event)

        self.retrain_action = QtGui.QAction('&Retrain', self)
        self.retrain_action.triggered.connect(self.retrain_event)

        self.log_data_action = QtGui.QAction('&Data Logging', self, checkable=True)
        self.log_data_action.triggered.connect(self.log_data_event)


        # Help Menu Actions
        help_action = QtGui.QAction('&Help', self)
        help_action.setStatusTip('Nomon help')
        help_action.triggered.connect(self.help_event)

        about_action = QtGui.QAction('&About', self)
        about_action.setStatusTip('Application information')
        about_action.triggered.connect(self.about_event)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu('&View')
        view_menu.addAction(self.high_contrast_action)
        clock_menu = view_menu.addMenu('&Clocks')
        clock_menu.addAction(self.default_clock_action)
        clock_menu.addAction(self.radar_clock_action)
        clock_menu.addAction(self.ball_clock_action)
        clock_menu.addAction(self.pacman_clock_action)
        clock_menu.addAction(self.bar_clock_action)
        text_menu = view_menu.addMenu('&Text Alignment')
        text_menu.addAction(self.auto_text_align_action)
        center_text_menu = text_menu.addMenu('&Center')
        center_text_menu.addAction(self.cl_text_align_action)
        center_text_menu.addAction(self.cc_text_align_action)
        center_text_menu.addAction(self.cr_text_align_action)
        font_menu = view_menu.addMenu('&Font Size')
        font_menu.addAction(self.small_font_action)
        font_menu.addAction(self.med_font_action)
        font_menu.addAction(self.large_font_action)
        keyboard_menu = view_menu.addMenu('&Keyboard Layout')
        keyboard_menu.addAction(self.default_layout_action)
        keyboard_menu.addAction(self.qwerty_layout_action)
        # word prediction
        word_menu = view_menu.addMenu('&Word Prediction Frequency')
        word_menu.addAction(self.high_word_action)
        word_menu.addAction(self.low_word_action)
        word_menu.addAction(self.off_word_action)

        tools_menu = menubar.addMenu('&Tools')
        tools_menu.addAction(self.profanity_filter_action)
        tools_menu.addAction(self.log_data_action)
        tools_menu.addAction(self.retrain_action)

        help_menu = menubar.addMenu('&Help')
        help_menu.addAction(help_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)

        self.setWindowTitle('Nomon Keyboard')

        self.icon = QtGui.QIcon(os.path.join("icons/", 'nomon.png'))
        self.setWindowIcon(self.icon)
        self.setGeometry(self.screen_res[0] * 0.05, self.screen_res[1] * 0.0675, self.screen_res[0] * 0.9,
                         self.screen_res[1] * 0.85)
        self.show()

        self.check_filemenu()

    def check_filemenu(self):
        def switch(unit, mode):
            if mode == unit.isChecked():
                pass
            else:
                unit.toggle()
        # check clocks
        switch(self.default_clock_action, self.clock_type == 'default')
        switch(self.radar_clock_action, self.clock_type == 'radar')
        switch(self.ball_clock_action, self.clock_type == 'ball')
        switch(self.pacman_clock_action, self.clock_type == 'pac_man')
        switch(self.bar_clock_action, self.clock_type == 'bar')

        # check text alignment
        switch(self.cc_text_align_action, self.alignment == 'cc')
        switch(self.cl_text_align_action, self.alignment == 'cl')
        switch(self.cr_text_align_action, self.alignment == 'cr')
        switch(self.auto_text_align_action, self.mainWidgit.text_alignment == 'auto')

        # check profanity
        switch(self.profanity_filter_action, self.pf_preference == 'on')

        # check log data
        switch(self.log_data_action, self.is_write_data)

        # check font menu
        switch(self.small_font_action, self.font_scale == 0)
        switch(self.med_font_action, self.font_scale == 1)
        switch(self.large_font_action, self.font_scale == 2)

        # check high contrast
        switch(self.high_contrast_action, self.high_contrast)

        # check layout
        switch(self.default_layout_action, self.target_layout == kconfig.alpha_target_layout)
        switch(self.qwerty_layout_action, self.target_layout == kconfig.qwerty_target_layout)

        # check word count
        switch(self.high_word_action, self.word_pred_on == 2)
        switch(self.low_word_action, self.word_pred_on == 1)
        switch(self.off_word_action, self.word_pred_on == 0)

    def word_change_event(self, frequency):
        if frequency == 'high':
            self.word_pred_on = 2
        elif frequency == 'low':
            self.word_pred_on = 1

        elif frequency == 'off':
            self.word_pred_on = 0

        self.check_filemenu()

        self.mainWidgit.clocks = []

        self.mainWidgit.clear_layout(self.mainWidgit.keyboard_grid)
        self.mainWidgit.clear_layout(self.mainWidgit.words_hbox)
        self.mainWidgit.laid_out = False
        self.mainWidgit.clocks = []
        self.mainWidgit.words_hbox.deleteLater()
        self.mainWidgit.keyboard_grid.deleteLater()
        self.mainWidgit.generate_clocks()
        self.draw_words()
        self.mainWidgit.layout_clocks()

    def change_font_size(self, size):
        if size == 'small':
            size = 0
        elif size == 'med':
            size = 1
        elif size == 'large':
            size = 2
        self.font_scale = size
        self.up_handel.safe_save([self.clock_type, size, self.high_contrast, self.layout_preference, self.pf_preference,
                                  self.start_speed, self.is_write_data])

        self.mainWidgit.sldLabel.setFont(config.top_bar_font[size])
        self.mainWidgit.speed_slider_label.setFont(config.top_bar_font[size])
        self.mainWidgit.wpm_label.setFont(config.top_bar_font[size])
        self.mainWidgit.cb_talk.setFont(config.top_bar_font[size])
        self.mainWidgit.cb_learn.setFont(config.top_bar_font[size])
        self.mainWidgit.cb_pause.setFont(config.top_bar_font[size])
        self.mainWidgit.cb_sound.setFont(config.top_bar_font[size])
        self.mainWidgit.text_box.setFont(config.text_box_font[size])

        self.mainWidgit.wpm_label.repaint()
        self.mainWidgit.cb_talk.repaint()
        self.mainWidgit.cb_learn.repaint()
        self.mainWidgit.cb_pause.repaint()
        self.mainWidgit.sldLabel.repaint()
        self.mainWidgit.speed_slider_label.repaint()
        self.mainWidgit.text_box.repaint()

        self.check_filemenu()

    def high_contrast_event(self):

        if self.high_contrast:
            hc_status = False
        else:
            hc_status = True

        self.up_handel.safe_save(
            [self.clock_type, self.font_scale, hc_status, self.layout_preference, self.pf_preference, self.start_speed,
             self.is_write_data])
        self.high_contrast = hc_status
        self.mainWidgit.color_index = hc_status

    def clock_change_event(self, design):
        message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Clock Design", "This will change the clocks "
                                                                                         "to the <b>" + design + "</b"
                                                                                         "> design",
                                       QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        design = design.replace(' ', '_')
        message_box.setDefaultButton(QtGui.QMessageBox.Cancel)
        message_box.setIconPixmap(QtGui.QPixmap(os.path.join("icons/", design + '.png')))
        message_box.setWindowIcon(self.icon)

        self.clock_type = design
        self.up_handel.safe_save([design, self.font_scale, self.high_contrast, self.layout_preference,
                                  self.pf_preference, self.start_speed, self.is_write_data])
        self.check_filemenu()
        self.mainWidgit.wpm_label.setText("Selections/Min: "+"----")
        self.wpm_data = config.Stack(config.wpm_history_length)
        self.wpm_time = 0

        if self.mainWidgit.text_alignment == 'auto':
            self.clock_text_align('auto', message=False)
            self.check_filemenu()

        for clock in self.mainWidgit.clocks:
            clock.calculate_clock_size()
            self.update_clock_radii()


    def layout_change_event(self, layout):
        message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Keyboard Layout", "This will change the clock "
                                                                                         "layout to <b>" + layout + "</b"
                                                                                         "> order. <b>NOTICE:</b> You "
                                                                                         "will have to restart Nomon for"
                                                                                         " these changes to take effect",
                                       QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        message_box.setDefaultButton(QtGui.QMessageBox.Cancel)
        message_box.setWindowIcon(self.icon)

        self.up_handel = PickleUtil("user_preferences/user_preferences.p")
        if layout == 'alphabetical':
            self.up_handel.safe_save([self.clock_type, self.font_scale, self.high_contrast, 'alpha',
                                      self.pf_preference, self.start_speed, self.is_write_data])
            self.target_layout = kconfig.alpha_target_layout

        elif layout == 'qwerty':
            self.up_handel.safe_save([self.clock_type, self.font_scale, self.high_contrast, 'qwerty',
                                      self.pf_preference, self.start_speed, self.is_write_data])
            self.target_layout = kconfig.qwerty_target_layout

        self.layout_preference = layout
        self.check_filemenu()

        self.mainWidgit.clocks = []

        self.mainWidgit.clear_layout(self.mainWidgit.keyboard_grid)
        self.mainWidgit.clear_layout(self.mainWidgit.words_hbox)
        self.mainWidgit.words_hbox.deleteLater()
        self.mainWidgit.keyboard_grid.deleteLater()
        self.mainWidgit.generate_clocks()
        self.mainWidgit.layout_clocks()

    def clock_text_align(self, alignment, message=True):
        if alignment == "auto":
            self.mainWidgit.text_alignment = 'auto'
            message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Text Alignment", "The text will be <b>"
                                                                                               "Auto-Aligned</b> to "
                                                                                               "best suit the keyboard"
                                                                                               " layout. (recommended)",
                                           QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
            if self.clock_type == "bar":
                alignment = "cc"
            else:
                alignment = "cr"
        else:
            self.mainWidgit.text_alignment = alignment
            alignment_name = ""
            if alignment == "cr":
                alignment_name = 'Center Right'
            elif alignment == "cc":
                alignment_name = 'Center'
            elif alignment == "cl":
                alignment_name = 'Center Left'
            elif alignment == "bc":
                alignment_name = 'Bottom Center'
            elif alignment == "tc":
                alignment_name = 'Top Center'

            message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Text Alignment", "This will change the "
                                                                                               "text to be aligned on "
                                                                                               "the <b>"
                                            + alignment_name + "</b>  of the clocks",
                                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        self.alignment = alignment

        self.mainWidgit.alignment = alignment
        self.resize_clocks()
        if message:
            self.check_filemenu()
            for clock in self.mainWidgit.clocks:
                clock.calculate_clock_size()
                self.update_clock_radii()

    def resize_clocks(self):
        if self.alignment[0] == 'b' or self.mainWidgit.alignment[0] == 't':
            for clock in self.mainWidgit.clocks:
                clock.setMaximumHeight(clock.maxSize*2)
                clock.setMinimumSize(clock.minSize*2.1, clock.minSize*2.1)
        else:
            for clock in self.mainWidgit.clocks:
                clock.setMaximumHeight(clock.maxSize)
                clock.setMinimumSize(clock.minSize, clock.minSize)

    def log_data_event(self):
        message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Data Logging Consent", "We would like to save "
                                                                                           "some data regarding your "
                                                                                           "clicking time relative to "
                                                                                           "Noon to help us improve "
                                                                                           "Nomon. All data collected "
                                                                                           "is anonymous and only your "
                                                                                           "click times will be saved. "
                                                                                           "<b> Do you consent to "
                                                                                           "allowing us to log click "
                                                                                           "timing data locally?</b>"
                                                                                           " (Note: you can change your"
                                                                                           " preference anytime in the "
                                                                                           "Tools menu).")
        message_box.addButton(QtGui.QMessageBox.Yes)
        message_box.addButton(QtGui.QMessageBox.No)
        message_box.setDefaultButton(QtGui.QMessageBox.No)
        message_box.setWindowIcon(self.icon)

        reply = message_box.exec_()
        self.first_load = False
        self.up_handel = PickleUtil("user_preferences/user_preferences.p")
        if reply == QtGui.QMessageBox.No:
            self.up_handel.safe_save(
                [self.clock_type, self.font_scale, self.high_contrast, self.layout_preference, self.pf_preference,
                 self.start_speed, False])
            self.is_write_data = False
        elif reply == QtGui.QMessageBox.Yes:
            self.up_handel.safe_save(
                [self.clock_type, self.font_scale, self.high_contrast, self.layout_preference, self.pf_preference,
                 self.start_speed, True])
            self.is_write_data = True
        self.check_filemenu()

    def profanity_filter_event(self):
        profanity_status = self.pf_preference
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Profanity Filter Settings", "The profanity filter is"
                                                                                               " currently <b>"
                                       + self.pf_preference.upper() + "</b>. Please select your desired setting "
                                                                      "below. ")
        messageBox.addButton(QtGui.QPushButton('On'), QtGui.QMessageBox.YesRole)
        messageBox.addButton(QtGui.QPushButton('Off'), QtGui.QMessageBox.NoRole)
        messageBox.setIconPixmap(QtGui.QPixmap(os.path.join('icons/block.png')))

        messageBox.setDefaultButton(QtGui.QMessageBox.No)
        messageBox.setWindowIcon(self.icon)

        reply = messageBox.exec_()
        self.up_handel = PickleUtil("user_preferences/user_preferences.p")
        if reply == 1:
            self.up_handel.safe_save(
                [self.clock_type, self.font_scale, self.high_contrast, self.layout_preference, 'off', self.start_speed,
                 self.is_write_data])
            if profanity_status == 'on':
                train_handle = open(kconfig.train_file_name_default, 'r')
                self.pause_animation = True
                self.dt = dtree.DTree(train_handle, self)
            self.pf_preference = 'off'
        elif reply == 0:
            self.up_handel.safe_save(
                [self.clock_type, self.font_scale, self.high_contrast, self.layout_preference, 'on', self.start_speed,
                 self.is_write_data])
            if profanity_status == 'off':
                train_handle = open(kconfig.train_file_name_censored, 'r')
                self.pause_animation = True
                self.dt = dtree.DTree(train_handle, self)
            self.pf_preference = 'on'
        self.check_filemenu()

    def about_event(self):
        # noinspection PyTypeChecker
        QtGui.QMessageBox.question(self, 'About Nomon', "Copyright 2009 Tamara Broderick\n"
                                                        "This file is part of Nomon Keyboard.\n\n"

                                                        "Nomon Keyboard is free software: you can redistribute "
                                                        "it and/or modify the Free Software Foundation, either "
                                                        "version 3 of the License, or (at your option) any "
                                                        "later version.\n\n"

                                                        "Nomon Keyboard is distributed in the hope that it will"
                                                        " be useful, but WITHOUT ANY WARRANTY; without even the"
                                                        " implied warranty of MERCHANTABILITY or FITNESS FOR A "
                                                        "PARTICULAR PURPOSE.  See the GNU General Public "
                                                        "License for more details.\n\n"

                                                        "You should have received a copy of the GNU General "
                                                        "Public License along with Nomon Keyboard.  If not, see"
                                                        " <http://www.gnu.org/licenses/>.",
                                   QtGui.QMessageBox.Ok)

    def help_event(self):
        self.launch_help()

    def retrain_event(self):
        self.launch_retrain()


class MainKeyboardWidget(QtGui.QWidget):

    def __init__(self, parent, layout, screen_res):
        super(MainKeyboardWidget, self).__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.parent = parent
        self.layout = layout
        self.screen_res = screen_res
        self.size_factor = min(self.screen_res) / 1080.
        self.text_alignment = 'auto'
        self.alignment = 'cr'
        self.in_focus = True
        self.color_index = self.parent.high_contrast

    # noinspection PyUnresolvedReferences
    def init_ui(self):

        # generate slider for clock rotation speed
        self.speed_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.speed_slider.setRange(config.scale_min, config.scale_max)
        self.speed_slider.setValue(self.parent.start_speed)
        self.speed_slider_label = QtGui.QLabel('Clock Rotation Speed:')

        self.speed_slider_label.setFont(config.top_bar_font[self.parent.font_scale])
        self.sldLabel = QtGui.QLabel(str(self.speed_slider.value()))
        self.sldLabel.setFont(config.top_bar_font[self.parent.font_scale])

        # wpm label
        self.wpm_label = QtGui.QLabel("Selections/Min: "+"----")
        self.wpm_label.setFont(config.top_bar_font[self.parent.font_scale])

        # generate learn, speak, talk checkboxes
        self.cb_talk = QtGui.QCheckBox('Talk', self)
        self.cb_learn = QtGui.QCheckBox('Learn', self)
        self.cb_pause = QtGui.QCheckBox('Pause', self)
        self.cb_sound = QtGui.QCheckBox('Sound', self)
        self.cb_talk.toggle()
        self.cb_talk.setFont(config.top_bar_font[self.parent.font_scale])
        self.cb_learn.toggle()
        self.cb_learn.setFont(config.top_bar_font[self.parent.font_scale])
        self.cb_pause.toggle()
        self.cb_pause.setFont(config.top_bar_font[self.parent.font_scale])
        self.cb_sound.toggle()
        self.cb_sound.setFont(config.top_bar_font[self.parent.font_scale])

        # generate clocks from layout
        self.generate_clocks()

        self.text_box = QtGui.QTextEdit("", self)

        self.text_box.setFont(config.text_box_font[self.parent.font_scale])
        self.text_box.setMinimumSize(300, 100)
        self.text_box.setReadOnly(True)

        # generate histogram
        self.histogram = HistogramWidget(self)

        if __name__ != '__main__':
            self.speed_slider.valueChanged[int].connect(self.change_value)
            self.cb_learn.toggled[bool].connect(self.parent.toggle_learn_button)
            self.cb_pause.toggled[bool].connect(self.parent.toggle_pause_button)
            self.cb_talk.toggled[bool].connect(self.parent.toggle_talk_button)
            self.cb_sound.toggled[bool].connect(self.parent.toggle_sound_button)

        # layout slider and checkboxes
        top_hbox = QtGui.QHBoxLayout()
        top_hbox.addWidget(self.speed_slider_label, 1)
        top_hbox.addWidget(self.speed_slider, 16)
        top_hbox.addWidget(self.sldLabel, 1)
        top_hbox.addStretch(2)
        top_hbox.addWidget(self.wpm_label, 1)
        top_hbox.addStretch(2)

        top_hbox.addWidget(self.cb_talk, 1)
        top_hbox.addWidget(self.cb_learn, 1)
        top_hbox.addWidget(self.cb_pause, 1)
        top_hbox.addWidget(self.cb_sound, 1)
        top_hbox.addStretch(1)

        # stack layouts vertically
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.addLayout(top_hbox)
        self.vbox.addStretch(1)
        self.vbox.addWidget(HorizontalSeparator())

        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter1.addWidget(self.text_box)
        self.splitter1.addWidget(self.histogram)
        self.splitter1.setSizes([1, 1])
        self.histogram.setMaximumHeight(160 * self.size_factor)
        self.text_box.setMaximumHeight(160 * self.size_factor)

        self.vbox.addSpacing(5)
        self.vbox.addWidget(self.splitter1, 4)
        self.layout_clocks()
        self.setLayout(self.vbox)

        self.frame_timer = QtCore.QTimer()
        self.frame_timer.timeout.connect(self.parent.on_timer)
        self.frame_timer.start(config.ideal_wait_s * 1000)

        self.pause_timer = QtCore.QTimer()
        self.pause_timer.setSingleShot(True)
        self.pause_timer.timeout.connect(self.parent.end_pause)

        self.highlight_timer = QtCore.QTimer()
        self.highlight_timer.setSingleShot(True)
        self.highlight_timer.timeout.connect(self.parent.end_highlight)

        # Tool Tips
        # noinspection PyCallByClass
        QtGui.QToolTip.setFont(QtGui.QFont('Monospace', 12))
        self.setToolTip("This is the Nomon Keyboard. To select an option, \n "
                        "find the clock immediately to its left. Press the \n"
                        "spacebar when the moving hand is near noon.")
        self.speed_slider_label.setToolTip("This slider scales the speed of clock rotation. Higher \nvalues correspond "
                                           "to the clock hand moving faster.")
        self.speed_slider.setToolTip("This slider scales the speed of clock rotation. Higher \n"
                                     "values correspond to the clock hand moving faster.")
        self.cb_pause.setToolTip("If this button is checked, there will be a brief \n"
                                 "pause and minty screen flash after each selection \n"
                                 "you make.")
        self.cb_talk.setToolTip("If this button is checked and if you have festival \n"
                                "installed and working on your system, there will be \n"
                                "spoken feedback after each selection you make.")
        self.cb_learn.setToolTip("If this button is checked, the program will adapt \n"
                                 "to how you click around noon (illustrated in the \n"
                                 "histogram below).")
        self.histogram.setToolTip("This is Nomon's estimate of where you click relative \n"
                                  "to noon on the clocks. The thinner the distribution, \n"
                                  "the more precisely Nomon thinks you are clicking.")

    def paintEvent(self, e):
        if self.parent.pretrain or self.parent.pause_animation:
            qp = QtGui.QPainter()
            qp.begin(self)
            brush = qp.brush()
            brush.setColor(QtGui.QColor(0, 0, 0, 10))
            qp.setBrush(brush)
            qp.fillRect(0,0,self.geometry().width(),self.geometry().height(),QtGui.QColor(220,220,220))
            qp.end()
            self.text_box.setStyleSheet("background-color:#e6e6e6;")
            self.splitter1.setStyleSheet("background-color:#e0e0e0;")
            self.in_focus = False

    def change_value(self, value):  # Change clock speed
        self.sldLabel.setText(str(self.speed_slider.value()))
        self.parent.change_speed(value)
        self.parent.start_speed = value
        self.up_handel = PickleUtil("user_preferences/user_preferences.p")
        self.up_handel.safe_save([self.parent.clock_type, self.parent.font_scale, self.parent.high_contrast, self.parent.layout_preference,
                                  self.parent.pf_preference, self.parent.start_speed, self.parent.is_write_data])

    def get_words(self, char):  # Reformat word list into blueprint for GUI construction
        i = 0
        output = []
        for word in self.parent.word_list:
            index = len(self.parent.prefix)
            
            if word[index] == char:
                i += 1
                if i > 3:
                    break
                output += [word]
        return output

    def generate_clocks(self):  # Generate the clock widgets according to blueprint from self.get_words
        self.clocks = []
        for row in self.layout:
            for text in row:
                if text == kconfig.mybad_char:
                    text = "Undo"
                elif text == kconfig.back_char:
                    text = "Backspace"
                elif text == kconfig.clear_char:
                    text = "Clear"
                clock = ClockWidgit(text, self)
                words = self.get_words(clock.text.lower())
                
                word_clocks = ['' for i in range(kconfig.N_pred)]
                i = 0
                for word in words:
                    word_clocks[i] = ClockWidgit(word, self)
                    i += 1
                for n in range(i, 3):
                    word_clocks[n] = ClockWidgit('', self, filler_clock=True)
                self.clocks += word_clocks
                self.clocks += [clock]

    def update_clocks(self):  # Used to change text and turn off clocks after initialization
        index = 0
        word_clocks = []
        for row in self.layout:
            for text in row:
                if text == kconfig.mybad_char:
                    text = "Undo"
                elif text == kconfig.back_char:
                    text = "Backspace"
                elif text == kconfig.clear_char:
                    text = "Clear"
                words = self.get_words(text.lower())
                for word in words:
                    if self.parent.word_pred_on == 1:
                        word_clocks += [self.clocks[index]]
                    self.clocks[index].filler_clock = False
                    self.clocks[index].setText(word)
                    index += 1
                for i in range(len(words), 3):
                    self.clocks[index].setText('')
                    self.clocks[index].filler_clock = True
                    self.clocks[index].repaint()
                    index += 1
                self.clocks[index].setText(text)
                index += 1
        if self.parent.word_pred_on == 1:
            if self.laid_out:
                self.words_hbox.deleteLater()
                self.words_hbox = QtGui.QHBoxLayout()
                for clock in word_clocks:
                    self.words_hbox.addWidget(clock, 6)
                    self.words_hbox.addStretch(1)
                self.vbox.insertLayout(4, self.words_hbox, 4)
        for clock in self.clocks:
            clock.calculate_clock_size()
            self.parent.update_clock_radii()

    def layout_clocks(self):  # called after self.generate_clocks, arranges clocks in grid
        qwerty = (self.parent.layout_preference == 'qwerty')
        target_layout_list = [j for i in self.parent.target_layout for j in i]
        combine_back_clocks = 'BACKUNIT' in target_layout_list
        combine_break_clocks = 'BREAKUNIT' in target_layout_list
        # layout keyboard in grid
        self.keyboard_grid = QtGui.QGridLayout()
        self.punctuation_grid = QtGui.QGridLayout()
        self.back_clear_vbox = QtGui.QVBoxLayout()

        def make_grid_unit(main_clock, sub_clocks=False):
            key_grid = QtGui.QGridLayout()
            if self.parent.word_pred_on == 2:
                if sub_clocks != []:
                    if qwerty:
                        key_grid.addWidget(VerticalSeparator(), 0, 0, 6, 1)
                        key_grid.addWidget(VerticalSeparator(), 0, 2, 6, 1)
                        key_grid.addWidget(HorizontalSeparator(), 0, 0, 1, 2)
                        key_grid.addWidget(HorizontalSeparator(), 6, 0, 1, 2)
                        key_grid.addWidget(main_clock, 1, 1)
                        clock_index = 0
                        for sub_clock in sub_clocks:
                            key_grid.addWidget(sub_clock, 2 + clock_index, 1)
                            clock_index += 1
                    else:
                        key_grid.addWidget(VerticalSeparator(), 0, 0, 4, 1)
                        key_grid.addWidget(VerticalSeparator(), 0, 3, 4, 1)
                        key_grid.addWidget(HorizontalSeparator(), 0, 0, 1, 3)
                        key_grid.addWidget(HorizontalSeparator(), 4, 0, 1, 3)
                        key_grid.addWidget(main_clock, 1, 1, 3, 1)
                        clock_index = 0
                        for sub_clock in sub_clocks:
                            key_grid.addWidget(sub_clock, 1+clock_index, 2)
                            clock_index += 1
                        key_grid.setColumnStretch(1, 4)
                        key_grid.setColumnStretch(2, 5)
                else:
                    key_grid.addWidget(VerticalSeparator(), 0, 0, 4, 1)
                    key_grid.addWidget(VerticalSeparator(), 0, 3, 4, 1)
                    key_grid.addWidget(HorizontalSeparator(), 0, 0, 1, 3)
                    key_grid.addWidget(HorizontalSeparator(), 4, 0, 1, 3)
                    key_grid.addWidget(main_clock, 1, 1, 3, 2)
            else:
                key_grid.addWidget(VerticalSeparator(), 0, 0, 4, 1)
                key_grid.addWidget(VerticalSeparator(), 0, 3, 4, 1)
                key_grid.addWidget(HorizontalSeparator(), 0, 0, 1, 3)
                key_grid.addWidget(HorizontalSeparator(), 4, 0, 1, 3)
                key_grid.addWidget(main_clock, 1, 1, 3, 2)
                key_grid.setColumnStretch(1, 4)
                key_grid.setRowStretch(1, 4)
            return key_grid

        if self.parent.word_pred_on != 2:
                for clock in self.clocks:
                    clock.maxSize = round(80 * clock.size_factor)
                    clock.setMaximumHeight(clock.maxSize)
                    clock.calculate_clock_size()
                    self.parent.update_clock_radii()
                    clock.repaint()


        self.grid_units=[]
        clock_index = 0
        break_clocks=[]
        undo_clocks=[]
        word_clocks = []
        for key in self.parent.key_chars:
            if key in list(string.ascii_letters) + [kconfig.space_char]:
                main_clock = self.clocks[clock_index + kconfig.N_pred]
                sub_clocks = [self.clocks[clock_index + i] for i in range(kconfig.N_pred)]
                clock_index += kconfig.N_pred + 1
            elif key in kconfig.break_chars:
                if combine_break_clocks:
                    break_clocks += [self.clocks[clock_index + kconfig.N_pred]]
                else:
                    if key == '\'':
                        main_clock = self.clocks[clock_index + kconfig.N_pred]
                        sub_clocks = [self.clocks[clock_index + i] for i in range(kconfig.N_pred)]
                    else:
                        main_clock = self.clocks[clock_index + kconfig.N_pred]
                        sub_clocks = []
                clock_index += kconfig.N_pred + 1
            elif key == kconfig.mybad_char:
                undo_clocks += [self.clocks[clock_index + kconfig.N_pred]]
                clock_index += kconfig.N_pred + 1
            elif key in [kconfig.back_char, kconfig.clear_char]:
                if combine_back_clocks:
                    undo_clocks += [self.clocks[clock_index + kconfig.N_pred]]
                else:
                    main_clock = self.clocks[clock_index + kconfig.N_pred]
                    sub_clocks = []
                clock_index += kconfig.N_pred + 1
            else:
                main_clock = self.clocks[clock_index + kconfig.N_pred]
                sub_clocks = []
                clock_index += kconfig.N_pred + 1
            word_clocks+=[clock for clock in sub_clocks if clock.text != '']
            self.grid_units += [make_grid_unit(main_clock, sub_clocks)]

        # make break unit:
        if combine_break_clocks:
            sub_break_unit = QtGui.QGridLayout()
            i = 1
            for clock in break_clocks:
                if clock.text != '\'':
                    sub_break_unit.addWidget(VerticalSeparator(), 0, 0, 5, 1)
                    sub_break_unit.addWidget(VerticalSeparator(), 0, 2, 5, 1)
                    sub_break_unit.addWidget(HorizontalSeparator(), 0, 0, 1, 2)
                    sub_break_unit.addWidget(HorizontalSeparator(), 5, 0, 1, 2)
                    sub_break_unit.addWidget(clock, i, 1)
                    i+=1
                else:
                    main_clock = clock
                    clock_index = self.clocks.index(main_clock)-1-kconfig.N_pred
                    sub_clocks = [self.clocks[clock_index - i-1] for i in range(kconfig.N_pred)]
                    apostrophe_grid = make_grid_unit(main_clock, sub_clocks)
            break_unit = QtGui.QHBoxLayout()
            break_unit.addLayout(sub_break_unit, 1)
            break_unit.addLayout(apostrophe_grid, 3)

        # make undo unit
        undo_unit = QtGui.QGridLayout()
        self.undo_label = QtGui.QLabel(self.parent.previous_undo_text)
        undo_font = QtGui.QFont('Consolas', 20)
        undo_font.setStretch(80)
        self.undo_label.setFont(undo_font)

        undo_unit.addWidget(VerticalSeparator(), 0, 0, 3, 1)
        undo_unit.addWidget(VerticalSeparator(), 0, 2, 3, 1)
        undo_unit.addWidget(HorizontalSeparator(), 0, 0, 1, 2)
        undo_unit.addWidget(HorizontalSeparator(), 3, 0, 1, 2)
        if combine_back_clocks:
            undo_unit.addWidget(undo_clocks[2], 1, 1)
        else:
            undo_unit.addWidget(undo_clocks[0], 1, 1)
        undo_unit.addWidget(self.undo_label, 2, 1)

        # make back unit
        if combine_back_clocks:
            back_unit = QtGui.QGridLayout()
            back_unit.addWidget(VerticalSeparator(), 0, 0, 4, 1)
            back_unit.addWidget(VerticalSeparator(), 0, 2, 4, 1)
            back_unit.addWidget(HorizontalSeparator(), 0, 0, 1, 2)
            back_unit.addWidget(HorizontalSeparator(), 4, 0, 1, 2)
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(undo_clocks[0], 3)
            vbox.addStretch(1)
            vbox.addWidget(undo_clocks[1], 3)
            back_unit.addLayout(vbox, 2, 1)

        def layout_from_target(target_layout):
            row_num=0
            for row in target_layout:
                col_num=0
                for key in row:
                    if key in self.parent.key_chars:
                        if key == kconfig.back_char or key == kconfig.space_char:
                            if qwerty:
                                self.keyboard_grid.addLayout(self.grid_units[self.parent.key_chars.index(key)], row_num,
                                                             col_num,1,3)
                                col_num += 2
                            else:
                                self.keyboard_grid.addLayout(self.grid_units[self.parent.key_chars.index(key)], row_num,
                                                             col_num)
                        if key == kconfig.clear_char:
                            if qwerty:
                                self.keyboard_grid.addLayout(self.grid_units[self.parent.key_chars.index(key)], row_num,
                                                             col_num,1,2)
                                col_num += 1
                            else:
                                self.keyboard_grid.addLayout(self.grid_units[self.parent.key_chars.index(key)], row_num,
                                                             col_num)
                        else:
                            self.keyboard_grid.addLayout(self.grid_units[self.parent.key_chars.index(key)], row_num,
                                                         col_num)
                    elif key == 'BREAKUNIT':
                        self.keyboard_grid.addLayout(break_unit, row_num, col_num)
                    elif key == 'UNDOUNIT':
                        if qwerty:
                            self.keyboard_grid.addLayout(undo_unit, row_num, col_num, 1, 2)
                            col_num += 1
                        else:
                            self.keyboard_grid.addLayout(undo_unit, row_num, col_num)
                    elif key == 'BACKUNIT':
                        self.keyboard_grid.addLayout(back_unit, row_num, col_num)
                    col_num += 1
                self.keyboard_grid.setRowStretch(row_num, 1)
                row_num += 1
        layout_from_target(self.parent.target_layout)
        self.vbox.insertLayout(3, self.keyboard_grid, 25)  # add keyboard grid to place in main layout
        self.words_hbox = QtGui.QHBoxLayout()
        if self.parent.word_pred_on == 1:
            for clock in word_clocks:
                self.words_hbox.addWidget(clock, 6)
                self.words_hbox.addStretch(1)
            self.vbox.insertLayout(4, self.words_hbox, 4)
        self.laid_out = True

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child)
