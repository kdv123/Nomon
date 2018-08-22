import sys
import os
import string
import config
import time
import dtree
import pickle
from pickle_util import *

from widgets import *


class MainWindow(QtGui.QMainWindow):
    def __init__(self, screen_res):
        super(MainWindow, self).__init__()

        self.screen_res = screen_res
        # Load User Preferences

    def initUI(self):
        self.mainWidgit = MainKeyboardWidget(self, self.key_chars, self.screen_res)
        self.mainWidgit.initUI()
        self.setCentralWidget(self.mainWidgit)
        self.clockTextAlign('auto', message=False)


        # File Menu Actions
        restartAction = QtGui.QAction('&Restart', self)
        restartAction.setShortcut('Ctrl+R')
        restartAction.setStatusTip('Restart application')
        restartAction.triggered.connect(self.restartEvent)

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(QtGui.qApp.quit)
        exitAction.triggered.connect(self.closeEvent)

        # Clock Menu Actions
        self.highContrastAction = QtGui.QAction('&High Contrast Mode', self, checkable=True)
        self.highContrastAction.triggered.connect(lambda: self.highContrastEvent())

        self.defaultClockAction = QtGui.QAction('&Default (Clock)', self, checkable=True)
        self.defaultClockAction.setStatusTip('Regular Nomon clock with sweeping minute hand')
        self.defaultClockAction.triggered.connect(lambda: self.clockChangeEvent('default'))
        self.defaultClockAction.setIcon(QtGui.QIcon(os.path.join("icons/", 'default.png')))

        self.radarClockAction = QtGui.QAction('&Radar (Clock)', self, checkable=True)
        self.radarClockAction.setStatusTip('Nomon clock with sweeping minute hand and radar trails')
        self.radarClockAction.triggered.connect(lambda: self.clockChangeEvent('radar'))
        self.radarClockAction.setIcon(QtGui.QIcon(os.path.join("icons/", 'radar.png')))

        self.ballClockAction = QtGui.QAction('&Ball (Filling)', self, checkable=True)
        self.ballClockAction.triggered.connect(lambda: self.clockChangeEvent('ball'))
        self.ballClockAction.setIcon(QtGui.QIcon(os.path.join("icons/", 'ball.png')))

        self.pacmanClockAction = QtGui.QAction('&Pac Man (Filling Pac Man)', self, checkable=True)
        self.pacmanClockAction.triggered.connect(lambda: self.clockChangeEvent('pac man'))
        self.pacmanClockAction.setIcon(QtGui.QIcon(os.path.join("icons/", 'pac_man.png')))

        self.barClockAction = QtGui.QAction('&Progress Bar', self, checkable=True)
        self.barClockAction.triggered.connect(lambda: self.clockChangeEvent('bar'))
        self.barClockAction.setIcon(QtGui.QIcon(os.path.join("icons/", 'bar.png')))

        # Font Menu Actions
        self.smallFontAction = QtGui.QAction('&Small', self, checkable=True)
        self.smallFontAction.triggered.connect(lambda: self.changeFontSize('small'))

        self.medFontAction = QtGui.QAction('&Medium (Default)', self, checkable=True)
        self.medFontAction.triggered.connect(lambda: self.changeFontSize('med'))

        self.largeFontAction = QtGui.QAction('&Large', self, checkable=True)
        self.largeFontAction.triggered.connect(lambda: self.changeFontSize('large'))

        # Text Menu Actions
        self.autoTextalignAction = QtGui.QAction('&Auto (Recommended)', self, checkable=True)
        self.autoTextalignAction.triggered.connect(lambda: self.clockTextAlign('auto'))

        self.tcTextalignAction = QtGui.QAction('&Top Center', self, checkable=True)
        self.tcTextalignAction.triggered.connect(lambda: self.clockTextAlign('tc'))

        self.clTextalignAction = QtGui.QAction('&Center Left', self, checkable=True)
        self.clTextalignAction.triggered.connect(lambda: self.clockTextAlign('cl'))

        self.ccTextalignAction = QtGui.QAction('&Center', self, checkable=True)
        self.ccTextalignAction.triggered.connect(lambda: self.clockTextAlign('cc'))

        self.crTextalignAction = QtGui.QAction('&Center Right', self, checkable=True)
        self.crTextalignAction.triggered.connect(lambda: self.clockTextAlign('cr'))

        self.bcTextalignAction = QtGui.QAction('&Bottom Center', self, checkable=True)
        self.bcTextalignAction.triggered.connect(lambda: self.clockTextAlign('bc'))

        # Keyboard Layout Menu Actions
        self.defaultLayoutAction = QtGui.QAction('&Alphabetical (Default)', self, checkable=True)
        self.defaultLayoutAction.triggered.connect(lambda: self.layoutChangeEvent('alphabetical'))

        self.qwertyLayoutAction = QtGui.QAction('&QWERTY', self, checkable=True)
        self.qwertyLayoutAction.triggered.connect(lambda: self.layoutChangeEvent('qwerty'))

        # Word Count Action
        self.highWordAction = QtGui.QAction('&High (Default)', self, checkable=True)
        self.highWordAction.triggered.connect(lambda: self.wordChangeEvent('high'))

        self.lowWordAction = QtGui.QAction('&Low (5 Words)', self, checkable=True)
        self.lowWordAction.triggered.connect(lambda: self.wordChangeEvent('low'))

        self.offWordAction = QtGui.QAction('&Off', self, checkable=True)
        self.offWordAction.triggered.connect(lambda: self.wordChangeEvent('off'))


        # Tools Menu Actions
        self.profanityFilterAction = QtGui.QAction('&Profanity Filter', self, checkable=True)
        self.profanityFilterAction.triggered.connect(self.profanityFilterEvent)

        self.retrainAction = QtGui.QAction('&Retrain', self)
        self.retrainAction.triggered.connect(self.retrainEvent)

        self.logDataAction = QtGui.QAction('&Data Logging', self, checkable=True)
        self.logDataAction.triggered.connect(self.logDataEvent)


        # Help Menu Actions
        helpAction = QtGui.QAction('&Help', self)
        helpAction.setStatusTip('Nomon help')
        helpAction.triggered.connect(self.helpEvent)

        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setStatusTip('Application information')
        aboutAction.triggered.connect(self.aboutEvent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        # fileMenu.addAction(restartAction)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(self.highContrastAction)
        clockMenu = viewMenu.addMenu('&Clocks')
        clockMenu.addAction(self.defaultClockAction)
        clockMenu.addAction(self.radarClockAction)
        clockMenu.addAction(self.ballClockAction)
        clockMenu.addAction(self.pacmanClockAction)
        clockMenu.addAction(self.barClockAction)
        textMenu = viewMenu.addMenu('&Text Alignment')
        textMenu.addAction(self.autoTextalignAction)
        # textMenu.addAction(self.tcTextalignAction)
        centerTextMenu = textMenu.addMenu('&Center')
        centerTextMenu.addAction(self.clTextalignAction)
        centerTextMenu.addAction(self.ccTextalignAction)
        centerTextMenu.addAction(self.crTextalignAction)
        fontMenu = viewMenu.addMenu('&Font Size')
        fontMenu.addAction(self.smallFontAction)
        fontMenu.addAction(self.medFontAction)
        fontMenu.addAction(self.largeFontAction)
        # textMenu.addAction(self.bcTextalignAction)
        keyboardMenu = viewMenu.addMenu('&Keyboard Layout')
        keyboardMenu.addAction(self.defaultLayoutAction)
        keyboardMenu.addAction(self.qwertyLayoutAction)
        # word prediction
        wordMenu = viewMenu.addMenu('&Word Prediction Frequency')
        wordMenu.addAction(self.highWordAction)
        wordMenu.addAction(self.lowWordAction)
        wordMenu.addAction(self.offWordAction)


        toolsMenu = menubar.addMenu('&Tools')
        toolsMenu.addAction(self.profanityFilterAction)
        toolsMenu.addAction(self.logDataAction)
        toolsMenu.addAction(self.retrainAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)

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
        switch(self.defaultClockAction, self.clock_type == 'default')
        switch(self.radarClockAction, self.clock_type == 'radar')
        switch(self.ballClockAction, self.clock_type == 'ball')
        switch(self.pacmanClockAction, self.clock_type == 'pac_man')
        switch(self.barClockAction, self.clock_type == 'bar')

        # check text alignment
        switch(self.ccTextalignAction, self.alignment == 'cc')
        switch(self.clTextalignAction, self.alignment == 'cl')
        switch(self.crTextalignAction, self.alignment == 'cr')
        switch(self.autoTextalignAction, self.mainWidgit.text_alignment == 'auto')

        # check profanity
        switch(self.profanityFilterAction, self.pf_preference == 'on')

        # check log data
        switch(self.logDataAction, self.is_write_data)

        # check font menu
        switch(self.smallFontAction, self.font_scale == 0)
        switch(self.medFontAction, self.font_scale == 1)
        switch(self.largeFontAction, self.font_scale == 2)

        # check high contrast
        switch(self.highContrastAction, self.high_contrast)

        # check layout
        switch(self.defaultLayoutAction, self.target_layout == kconfig.alpha_target_layout)
        switch(self.qwertyLayoutAction, self.target_layout == kconfig.qwerty_target_layout)

        # check word count
        switch(self.highWordAction, self.word_pred_on == 2)
        switch(self.lowWordAction, self.word_pred_on == 1)
        switch(self.offWordAction, self.word_pred_on == 0)

    def wordChangeEvent(self, frequency):
        if frequency == 'high':
            self.word_pred_on = 2
        elif frequency == 'low':
            self.word_pred_on = 1

        elif frequency == 'off':
            self.word_pred_on = 0

        self.check_filemenu()

        self.mainWidgit.clocks = []


        self.mainWidgit.clearLayout(self.mainWidgit.keyboard_grid)
        self.mainWidgit.clearLayout(self.mainWidgit.words_hbox)
        self.mainWidgit.layed_out=False
        self.mainWidgit.clocks = []
        self.mainWidgit.words_hbox.deleteLater()
        self.mainWidgit.keyboard_grid.deleteLater()
        self.mainWidgit.generateClocks()
        self.draw_words()
        self.mainWidgit.layoutClocks()


    def changeFontSize(self, size):
        if size == 'small':
            size = 0
        elif size == 'med':
            size = 1
        elif size == 'large':
            size = 2
        self.font_scale = size
        self.up_handel.safe_save([self.clock_type, size, self.high_contrast, self.layout_preference, self.pf_preference,
                                  self.start_speed, self.is_write_data])

        self.mainWidgit.sldLabel.setFont(top_bar_font[size])
        self.mainWidgit.speed_slider_label.setFont(top_bar_font[size])
        self.mainWidgit.wpm_label.setFont(top_bar_font[size])
        self.mainWidgit.cb_talk.setFont(top_bar_font[size])
        self.mainWidgit.cb_learn.setFont(top_bar_font[size])
        self.mainWidgit.cb_pause.setFont(top_bar_font[size])
        self.mainWidgit.cb_sound.setFont(top_bar_font[size])
        self.mainWidgit.text_box.setFont(text_box_font[size])

        self.mainWidgit.wpm_label.repaint()
        self.mainWidgit.cb_talk.repaint()
        self.mainWidgit.cb_learn.repaint()
        self.mainWidgit.cb_pause.repaint()
        self.mainWidgit.sldLabel.repaint()
        self.mainWidgit.speed_slider_label.repaint()
        self.mainWidgit.text_box.repaint()

        self.check_filemenu()

    def highContrastEvent(self):

        if self.high_contrast:
            hc_status = False
        else:
            hc_status = True

        self.up_handel.safe_save(
            [self.clock_type, self.font_scale, hc_status, self.layout_preference, self.pf_preference, self.start_speed,
             self.is_write_data])
        self.high_contrast = hc_status
        self.mainWidgit.color_index = hc_status

    def clockChangeEvent(self, design):
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Clock Design", "This will change the clocks "
                                                                                         "to the <b>" + design + "</b"
                                                                                         "> design",
                                       QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        design = design.replace(' ', '_')
        messageBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        messageBox.setIconPixmap(QtGui.QPixmap(os.path.join("icons/", design + '.png')))
        messageBox.setWindowIcon(self.icon)

        self.clock_type = design
        self.up_handel.safe_save([design, self.font_scale, self.high_contrast, self.layout_preference,
                                  self.pf_preference, self.start_speed, self.is_write_data])
        self.check_filemenu()
        self.mainWidgit.wpm_label.setText("Selections/Min: "+"----")
        self.wpm_data = config.Stack(config.wpm_history_length)
        self.wpm_time = 0

        if self.mainWidgit.text_alignment == 'auto':
            self.clockTextAlign('auto', message=False)
            self.check_filemenu()

        for clock in self.mainWidgit.clocks:
            clock.calcClockSize()

    def layoutChangeEvent(self, layout):
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Keyboard Layout", "This will change the clock "
                                                                                         "layout to <b>" + layout + "</b"
                                                                                         "> order. <b>NOTICE:</b> You "
                                                                                         "will have to restart Nomon for"
                                                                                         " these changes to take effect",
                                       QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        messageBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        messageBox.setWindowIcon(self.icon)

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


        self.mainWidgit.clearLayout(self.mainWidgit.keyboard_grid)
        self.mainWidgit.clearLayout(self.mainWidgit.words_hbox)
        self.mainWidgit.words_hbox.deleteLater()
        self.mainWidgit.keyboard_grid.deleteLater()
        self.mainWidgit.generateClocks()
        self.mainWidgit.layoutClocks()



    def clockTextAlign(self, alignment, message=True):
        if alignment == "auto":
            self.mainWidgit.text_alignment = 'auto'
            messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Text Alignment", "The text will be <b>"
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

            messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Change Text Alignment", "This will change the "
                                                                                               "text to be aligned on "
                                                                                               "the <b>"
                                           + alignment_name + "</b>  of the clocks",
                                           QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        self.alignment = alignment

        self.mainWidgit.alignment = alignment
        self.resizeClocks()
        if message:
            self.check_filemenu()
            for clock in self.mainWidgit.clocks:
                clock.calcClockSize()



    def resizeClocks(self):
        if self.alignment[0] == 'b' or self.mainWidgit.alignment[0] == 't':
            for clock in self.mainWidgit.clocks:
                clock.setMaximumHeight(clock.maxSize*2)
                clock.setMinimumSize(clock.minSize*2.1, clock.minSize*2.1)
        else:
            for clock in self.mainWidgit.clocks:
                clock.setMaximumHeight(clock.maxSize)
                clock.setMinimumSize(clock.minSize, clock.minSize)

    def logDataEvent(self):
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Data Logging Consent", "We would like to save "
                                                                                          "some data regarding your "
                                                                                          "clicking time relative to "
                                                                                          "Noon to help us improve "
                                                                                          "Nomon. All data collected is"
                                                                                          " anonymous and only your "
                                                                                          "click times will be saved. "
                                                                                          "<b> Do you consent to "
                                                                                          "allowing us to log click "
                                                                                          "timing data locally?</b>"
                                                                                          " (Note: you can change your"
                                                                                          " preference anytime in the "
                                                                                          "Tools menu).")
        messageBox.addButton(QtGui.QMessageBox.Yes)
        messageBox.addButton(QtGui.QMessageBox.No)
        messageBox.setDefaultButton(QtGui.QMessageBox.No)
        messageBox.setWindowIcon(self.icon)

        reply = messageBox.exec_()
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

    def profanityFilterEvent(self):
        profanity_status = self.pf_preference
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Profanity Filter Settings", "The profanity filter is "
                                                                                             "currently <b>"
                                       + self.pf_preference.upper() + "</b>. Please select your desired setting below. ")
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


    def aboutEvent(self):
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

    def helpEvent(self):
        self.launch_help()

    def retrainEvent(self):
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

    def initUI(self):

        # generate slider for clock rotation speed
        self.speed_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.speed_slider.setRange(config.scale_min, config.scale_max)
        self.speed_slider.setValue(self.parent.start_speed)
        self.speed_slider_label = QtGui.QLabel('Clock Rotation Speed:')

        self.speed_slider_label.setFont(top_bar_font[self.parent.font_scale])
        self.sldLabel = QtGui.QLabel(str(self.speed_slider.value()))
        self.sldLabel.setFont(top_bar_font[self.parent.font_scale])

        # wpm label
        self.wpm_label = QtGui.QLabel("Selections/Min: "+"----")
        self.wpm_label.setFont(top_bar_font[self.parent.font_scale])


        # generate learn, speak, talk checkboxes
        self.cb_talk = QtGui.QCheckBox('Talk', self)
        self.cb_learn = QtGui.QCheckBox('Learn', self)
        self.cb_pause = QtGui.QCheckBox('Pause', self)
        self.cb_sound = QtGui.QCheckBox('Sound', self)
        self.cb_talk.toggle()
        self.cb_talk.setFont(top_bar_font[self.parent.font_scale])
        self.cb_learn.toggle()
        self.cb_learn.setFont(top_bar_font[self.parent.font_scale])
        self.cb_pause.toggle()
        self.cb_pause.setFont(top_bar_font[self.parent.font_scale])
        self.cb_sound.toggle()
        self.cb_sound.setFont(top_bar_font[self.parent.font_scale])

        # generate clocks from layout
        self.generateClocks()

        self.text_box = QtGui.QTextEdit("", self)

        self.text_box.setFont(text_box_font[self.parent.font_scale])
        self.text_box.setMinimumSize(300, 100)
        self.text_box.setReadOnly(True)

        # generate histogram
        self.histogram = HistogramWidget(self)

        if __name__ != '__main__':
            self.speed_slider.valueChanged[int].connect(self.changeValue)
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
        self.layoutClocks()
        self.setLayout(self.vbox)


        if __name__ != '__main__':  # remove inheritance dependent timers for sole GUI run
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
        QtGui.QToolTip.setFont(QtGui.QFont('Monospace', 12))
        self.setToolTip("This is the Nomon Keyboard. To select an option, \n "
                        "find the clock immediately to its left. Press the \n"
                        "spacebar when the moving hand is near noon.")
        self.speed_slider_label.setToolTip("This slider scales the speed of clock rotation. Higher \n"
                                "values correspond to the clock hand moving faster.")
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

    def changeValue(self, value):  # Change clock speed
        self.sldLabel.setText(str(self.speed_slider.value()))
        self.parent.change_speed(value)
        self.parent.start_speed = value
        self.up_handel = PickleUtil("user_preferences/user_preferences.p")
        self.up_handel.safe_save([self.parent.clock_type, self.parent.font_scale, self.parent.high_contrast, self.parent.layout_preference,
                                  self.parent.pf_preference, self.parent.start_speed, self.parent.is_write_data])

    def getWords(self, char):  # Reformat word list into blueprint for GUI construction
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

    def generateClocks(self):  # Generate the clock widgets according to blueprint from self.getWords
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
                words = self.getWords(clock.text.lower())
                
                word_clocks = ['' for i in range(kconfig.N_pred)]
                i = 0
                for word in words:
                    word_clocks[i] = ClockWidgit(word, self)
                    i += 1
                for n in range(i, 3):
                    word_clocks[n] = ClockWidgit('', self, filler_clock=True)
                self.clocks += word_clocks
                self.clocks += [clock]

    def updateClocks(self):  # Used to change text and turn off clocks after initialization
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
                words = self.getWords(text.lower())
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
            if self.layed_out:
                self.words_hbox.deleteLater()
                self.words_hbox = QtGui.QHBoxLayout()
                for clock in word_clocks:
                    self.words_hbox.addWidget(clock, 6)
                    self.words_hbox.addStretch(1)
                self.vbox.insertLayout(4, self.words_hbox, 4)

        for clock in self.clocks:
            clock.calcClockSize()

    def layoutClocks(self):  # called after self.generateClocks, arranges clocks in grid
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
                    clock.calcClockSize()
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

        ####### make break unit:
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

        ####### make undo unit
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

        ####### make back unit
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
        self.layed_out = True

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child)


def main():  # set up 'dummy' keyboard instance to allow for pure GUI layout debugging

    currentExitCode = MainWindow.EXIT_CODE_REBOOT
    while currentExitCode == MainWindow.EXIT_CODE_REBOOT:
        app = QtGui.QApplication(sys.argv)
        screen_res = (app.desktop().screenGeometry().width(), app.desktop().screenGeometry().height())
        ex = MainWindow(screen_res)
        word_list = open('word_list.txt', 'r')
        words = word_list.read()
        words = words.split()
        word_list.close()
        ex.word_list = []
        for letter in string.ascii_lowercase:
            i = 0
            for word in words:
                if word[0] == letter and i < kconfig.N_pred:
                    i += 1
                    ex.word_list += [word]
        ex.prefix = ''
        ex.bars = kconfig.bars
        ex.previous_undo_text = ''
        ex.initUI()

        currentExitCode = app.exec_()
        app = None  # delete the QApplication object


if __name__ == '__main__':
    main()
