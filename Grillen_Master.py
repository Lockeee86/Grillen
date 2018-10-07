#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Grill-Thermometer
============

'''
import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.image import Image 
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, OptionProperty, ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.settings import SettingsWithNoMenu
from settingsjson import settings_json
from kivy.clock import Clock
#from Adafruit_IO import *
from ConfigParser import ConfigParser

import serial
import datetime 
import time
import struct
from time import strftime


Builder.load_string("""

<Grillen>:
    size: (800,480)
    background_color:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    do_default_tab: False
    tab_pos: 'top_left'
    tab_height: 60
    font_name: 'Antonio-Regular.ttf'

    TabbedPanelItem:
        text: 'Main'
        FloatLayout:
            Label:
                id: Datum
                text: root.date
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 1.04, 'center_x': 0.92}
                font_size: '20sp'
            Label:
                id: Uhrzeit
                text: root.time
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 1, 0.9
                pos_hint: {'center_y': 1.11, 'center_x': 0.95}
                font_size: '40sp'
            Button:
                id:'close'
                text: 'close'
                on_press: root.popup_close()
                size_hint: 0.45, 0.15
                #size_hint: 0.15, 0.15
                pos_hint: {'bottom':0.95, 'center_x':0.25}
                #pos_hint: {'x':0.85, 'y':1}
                background_color: 1, 0, 0, 1
            Button:
                id: 'Datenbank'
                text: 'settings'
                size_hint: 0.45, 0.15
                #size_hint: 0.15, 0.15
                pos_hint: {'bottom':0.95, 'center_x':0.75}
                #pos_hint: {'x':0.7, 'y':1}
                background_color: 0, 1, 0, 1
                on_release: app.open_settings()
            Image:
                size_hint: 0.9, 0.9
                pos_hint: {'top':1, 'center_x':0.5}
                source: 'Bild/Logo_Grillen.png'
                color: 0.8,0.8,0.8,0.8
                
    TabbedPanelItem:
        text: 'live data'
        FloatLayout:
            Label:
                id: Datum
                text: root.date
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 1.04, 'center_x': 0.92}
                font_size: '20sp'
            Label:
                id: Uhrzeit
                text: root.time
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 1, 0.9
                pos_hint: {'center_y': 1.11, 'center_x': 0.95}
                font_size: '40sp'
            GridLayout:
                cols: 3
                rows: 2
                spacing: 25
                padding: 50
                Image:
                    source: 'Bild/grill.png'
                Image:
                    source: 'Bild/fleisch.png'
                Image:
                    source: 'Bild/wetter.png'
                Label:
                    id: 'temp_grill'
                    font_size: '70sp'
                    font_name: 'Font/DS-DIGIB.ttf'
                    text: root.grill_temp + ' C'
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        id: 'temp_fleisch'
                        font_name: 'Font/DS-DIGIB.ttf'
                        font_size: '60sp'
                        text: root.fleisch_temp + ' C'
                    Label:
                        id: 'temp_fleisch2'
                        font_size: '60sp'
                        font_name: 'Font/DS-DIGIB.ttf'
                        text: root.fleisch2_temp + ' C'
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        id: 'temp_wetter'
                        font_size: '60sp'
                        font_name: 'Font/DS-DIGIB.ttf'
                        text: root.digit_temp + ' C'
                    Label:
                        id: 'humi_wetter'
                        font_size: '60sp'
                        font_name: 'Font/DS-DIGIB.ttf'
                        text: root.humi_temp + ' %'
                

    TabbedPanelItem:
        text: 'Adafruit.io'
        FloatLayout:
            Label:
                id: Datum
                text: root.date
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 1.04, 'center_x': 0.92}
                font_size: '20sp'
            Label:
                id: Uhrzeit
                text: root.time
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 1, 0.9
                pos_hint: {'center_y': 1.11, 'center_x': 0.95}
                font_size: '40sp'
            Label:
                id: 'Adafruit_link'
                font_size: '25sp'
                pos_hint: {'x':0, 'y':0.4}
                text: 'Adafruit.io link zu Daten'
            Image:
                size_hint: 0.9, 0.9
                pos_hint: {'top':0.9, 'center_x':0.5}
                source: 'Bild/iot_link.png'

    TabbedPanelItem:
        text: 'Grillzeit'
        #time_prop: stopwatch
        FloatLayout:
            Label:
                id: Datum
                text: root.date
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 1.04, 'center_x': 0.92}
                font_size: '20sp'
            Label:
                id: Uhrzeit
                text: root.time
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 1, 0.9
                pos_hint: {'center_y': 1.11, 'center_x': 0.95}
                font_size: '40sp'

            Button:
                id: start_stop
                text: 'Start'
                on_press: root.start_stop()
                size_hint: 0.45, 0.15
                pos_hint: {'bottom':0.95, 'center_x':0.25}
                background_color: 0, 1, 0, 1
            Button:
                id: reset
                text: 'Reset'
                on_press: root.reset()
                size_hint: 0.45, 0.15
                pos_hint: {'bottom':0.95, 'center_x':0.75}
                background_color: 1, 0, 0, 1
            Label:
                id: stopwatch
                text: '00:00[size=100]:00[/size]'
                markup: True
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 0.5, 'center_x': 0.5}
                font_size: '170sp'

    TabbedPanelItem:
        text: 'Impressum'
        FloatLayout:
            Label:
                id: Datum
                text: root.date
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 0.9, 0.9
                pos_hint: {'center_y': 1.04, 'center_x': 0.92}
                font_size: '20sp'
            Label:
                id: Uhrzeit
                text: root.time
                font_name: 'Font/DS-DIGIB.ttf'
                size_hint: 1, 0.9
                pos_hint: {'center_y': 1.11, 'center_x': 0.95}
                font_size: '40sp'
            Image:
                size_hint: 0.9, 0.9
                pos_hint: {'top':1, 'center_x':0.5}
                source: 'Bild/Logo_Grillen.png'
                color: 0.7,0.7,0.7,0.7
                
            BoxLayout:
                spacing: 5
                padding: 50
                orientation: 'vertical'
                Label:
                    id: 'Imp0'
                    font_size: '25sp'
                    text: 'Grillen | ... wenn Männer kochen \xc2\xae'
                Label:
                    id: 'Imp2'
                    text: 'Herzlichen dank an meinen Bruder Hannes, meinen Cousin Henrik'
                Label:
                    id: 'Imp3'
                    text: 'und alle die bei diesem Projekt geholfen haben.'
                Label:
                    id: 'Imp4'
                    text: 'Copyright \xa9 2017 Steffen Burmeister'

<fail_usb>:
    size: (800,480)
    background_color:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    font_name: 'Antonio-Regular.ttf'
    Label:
        text:'Hello World'


""")  

class fail_usb(Label):
    background_color = ListProperty((0.22, 0.22, 0.22, 0.5))

class Grillen(TabbedPanel):
    background_color = ListProperty((0.22, 0.22, 0.22, 0.5))
    
    grill_temp = StringProperty()
    fleisch_temp = StringProperty()
    fleisch2_temp = StringProperty()     
    digit_temp = StringProperty()    
    humi_temp = StringProperty() 

    date = StringProperty()
    time = StringProperty()

    #time_prop = ObjectProperty(None)
    sw_started = False
    sw_seconds = 0



    def __init__(self, **kwargs):
        super(Grillen, self).__init__(**kwargs)
#       Set the timer for redrawing the screen        
        refresh_time = 0.05
        Clock.schedule_interval(self.timer, refresh_time)
        refresh_time_db = 30
        #Clock.schedule_interval(self.database, refresh_time_db)
        #Clock.schedule_interval(self.update_time, 0.016)
        Clock.schedule_interval(self.update, 0.016)
        Clock.schedule_interval(self.update_time, 0)

    def update(self, *args):
        self.date = str(time.strftime("%a, %d %b %Y"))
        self.time = str(time.strftime("%H:%M")) 

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
            mm, ss = divmod(self.sw_seconds, 60)
            hh, mm = divmod(mm, 60)
            #minutes, seconds = divmod(self.sw_seconds, 60)
            self.ids.stopwatch.text = (
                '%02d:%02d[size=100]:%02d[/size]' %
                (int(hh), int(mm), int(ss))) 

    def start_stop(self):
        self.ids.start_stop.text = ('Start'
            if self.sw_started else 'Stop')
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.ids.start_stop.text = 'Start'
            self.sw_started = False
        self.sw_seconds = 0 
        self.ids.stopwatch.text = ('00:00[size=100]:00[/size]')
    
    def timer(self, dt):
        # Read from Arduino
        tmp_line = arduinoData.readline()
        temp_array = tmp_line.rstrip().split(", ")
        
        # if temp_array a valide string
        if len(temp_array) == 5: 
            self.grill_temp = temp_array[0] 
            self.fleisch_temp = temp_array[1]
            self.fleisch2_temp = temp_array[2]
            self.digit_temp = temp_array[3]
            self.humi_temp = temp_array[4]  
            # if data from Arduino set Array to "n/a"       
            if self.grill_temp == str(0):
                self.grill_temp = "n/a"
            if self.fleisch_temp == str(0):
                self.fleisch_temp = "n/a"
            if self.fleisch2_temp == str(0):
                self.fleisch2_temp = "n/a"
            if self.digit_temp == str(0):
                self.digit_temp = "n/a"
            if self.humi_temp == str(0):
                self.humi_temp = "n/a"

        # else print n/a to Datascreen
        else:
            self.grill_temp = "n/a" 
            self.fleisch_temp = "n/a"
            self.fleisch2_temp = "n/a"
            self.digit_temp = "n/a"
            self.humi_temp = "n/a"

        # settings
        config = ConfigParser()
        config.read('grillen.ini')
        self.sett_db = config.get('grillen', 'datenbank')
        self.sett_time = config.get('grillen', 'datenbank2')
        if self.sett_time == '10 Sekunden':
            sett_time_callback = 10
        elif self.sett_time == '30 Sekunden':
            sett_time_callback = 30
        elif self.sett_time == '1 Minute':
            sett_time_callback = 60
        else:
            pass

        # self.sett_file_callback = int(self.sett_file)
        # if self.sett_file_callback == 1:
        #     aio = Client('df2d4865170649e9af4c417f325e4397')
        # delete data ------

    #def database(self, dt):
        #self.sett_db_callback = int(self.sett_db)
        # aio = Client('df2d4865170649e9af4c417f325e4397')
        
        # # if set send to Database in settings on
        # if self.sett_db_callback == 1:

        #     adafruit_grill = self.grill_temp
        #     adafruit_fleisch = self.fleisch_temp
        #     adafruit_fleisch2 = self.fleisch2_temp
        #     adafruit_digit_temp = self.digit_temp
        #     adafruit_humi_temp = self.humi_temp

        #     # Send to Adafruit.io
        #     aio.send('grill', adafruit_grill)
        #     aio.send('fleisch', adafruit_fleisch)
        #     aio.send('fleisch2', adafruit_fleisch2)
        #     aio.send('aussen', adafruit_digit_temp)
        #     aio.send('luft', adafruit_humi_temp) 
        # else:
        #     pass   

    def popup_close(self):
        self.box=FloatLayout()
        
        self.lab=(Label(text="Willst du die App wirklich verlassen?\n\n\nDoch nicht?\nklick einfach neben das Fenster ",font_size=15,
            size_hint=(None,None),pos_hint={'x':0.25,'y':0.4}))
        self.box.add_widget(self.lab)
        
        # self.but=(Button(text="close",size_hint=(None,None),
        #     width=150,height=40,pos_hint={'x':0,'y':0}))
        # self.box.add_widget(self.but)
        
        self.but2=(Button(text="exit",size_hint=(None,None),
            width=325,height=40,pos_hint={'x':0.0,'y':0}))
        self.box.add_widget(self.but2)
       
        self.main_pop = Popup(title="Grillen | ... wenn Männer kochen",content=self.box,
            size_hint=(None,None),size=(350,250),title_size=20)
            
        # self.but.bind(on_press=self.main_pop.dismiss)
        self.but2.bind(on_press=GrillenApp.quit)

        self.main_pop.open()

class GrillenApp(App):
    
    settings_popup = ObjectProperty(None, allownone=True)

    def build(self):
        self.settings_cls = SettingsWithNoMenu
        self.use_kivy_settings = False
        config = self.config
        return Grillen()
        
#   settings data in config.
    def build_config(self, config):
        config.setdefaults('grillen',{
            'datenbank': False,
            'datenbank2': '30 sekunden',
            'led': False
            })

#   display the settings in Popup.    
    def display_settings(self, settings):
        p = self.settings_popup
        if p is None:
            self.settings_popup = p = Popup(content=settings,
                                                title='Grillen | ...wenn Männer kochen Settings',
                                                size_hint=(0.8, 0.8))
        else:
            pass

        if p.content is not settings:
            p.content = settings
        else:
            pass
        p.open()

#   build manual settings Grillen.
    def build_settings(self, settings):
        settings.add_json_panel('Grillen',
                                self.config,
                                data=settings_json)

#   handle with setting states.
    def on_config_change(self, config, section,
                        key, value):
        if config is self.config:
            token = (section, key)
            if token == ('grillen', 'led'):
                arduinoData.write(value)

    def quit(self):
        App.get_running_app().stop()

    def on_start(self):
        print("open the app")

    def on_stop(self):
        print("close the app")
           
if __name__ == '__main__':

    try:    
        #arduinoData = serial.Serial('/dev/ttyACM0', 115200) # USB Raspberry
        arduinoData = serial.Serial('/dev/cu.usbmodem1421', 115200) # USB Mac
        #arduinoData.timeout = 1
    except:
        print "Failed to connect to serial port"
        return fail_usb()

    GrillenApp().run()

    arduinoData.close()
    #db.close()
    

