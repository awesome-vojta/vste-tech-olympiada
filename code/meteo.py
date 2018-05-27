#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository.GdkPixbuf import Pixbuf 
from gi.repository import Gio 
from gi.repository import GObject 
from gi.repository import GLib
import urllib2, json, datetime, time, os, sys, threading
import meteo_function
from meteo_function import *
import meteo_config
from meteo_config import *
import meteo_gpio
from meteo_gpio import *

isFullscreen = True

class Meteostation:
	def onDeleteWindow(self, object, data=None):
		gtk.main_quit()

	def on_gtk_quit_activate(self, menuitem, data=None):
		gtk.main_quit()

	def onclock_time(self):
		global time_to_next_read_data, time_to_next_report, time_to_next_owm
		try:
			now = datetime.datetime.now()
			#datum
			self.builder.get_object("label39").set_text(now.strftime('%d.%m.%Y'))
			#cas
			self.builder.get_object("label40").set_text(now.strftime('%H:%M:%S'))
			#cast dne
			cast_dne = ""
			hodina = int(now.strftime('%H'))
			if 6 <= hodina < 10:
				cast_dne = "ráno"
			elif 10 <= hodina < 12:
				cast_dne = "dopoledne"
			elif hodina == 12:
				cast_dne = "poledne"
			elif 13 <= hodina < 18:
				cast_dne = "odpoledne"
			elif 18 <= hodina < 22:
				cast_dne = "večer"
			else:
				cast_dne = "noc"
			self.builder.get_object("label14").set_text(cast_dne)
			#den v tydnu
			self.builder.get_object("label13").set_text(denTydne(int(now.strftime('%d')),int(now.strftime('%m')),int(now.strftime('%Y'))))
			#mesic
			self.builder.get_object("label20").set_text(mesicNazev(int(now.strftime('%m'))))
			#svatek
			self.builder.get_object("label32").set_text(dnes_svatek(int(now.strftime('%m')),int(now.strftime('%d'))))
			#den v roce
			self.builder.get_object("label18").set_text(str(now.timetuple().tm_yday))
			#cislo tydne
			#self.builder.get_object("label20").set_text(now.strftime('%U'))
			cislo_tydne = str(now.isocalendar()[1])
			if int(cislo_tydne) % 2 == 0:
				cislo_tydne += " (sudý)"
			else:
				cislo_tydne += " (lichý)"
			self.builder.get_object("label33").set_text(cislo_tydne)
			#cas do dalsi aktualizace
			if time_to_next_read_data>0:
				time_to_next_read_data -= 1
			if time_to_next_report>0:
				time_to_next_report -= 1
			if time_to_next_owm>0:
				time_to_next_owm -= 1
			self.builder.get_object("time_remaining_label").set_text(str(datetime.datetime.now().strftime("%H:%M")))
		finally:
			return True

	def onclock_read_data(self):
		#print "clock_read_data "+str(datetime.datetime.now().strftime("%H:%S"))
		try:
			#TEMP, HUM IN
			if meteo_gpio.readTemperatureIN():
				self.builder.get_object("temperature_in_label").set_text(str(meteo_gpio.temperature1)+ " °C")
				self.builder.get_object("humidity_in_label").set_text(str(meteo_gpio.humidity1)+ " %")
			else:
				self.addRecord("DHT11 - neúspěšné měření VNITRNI TEPLOTY A VLHKOSTI", True)
			#TEMP-OUT
			if meteo_gpio.readTemperatureOUT():
				self.builder.get_object("temperature_out_label").set_text(str(meteo_gpio.temperature2)+ " °C")
			else:
				self.addRecord("DS18 - neúspěšné měření VENKOVNI TEPLOTY ", True)
			#HUM-OUT,DHT22
			if meteo_gpio.readHumidityOUT():
				self.builder.get_object("humidity_out_label").set_text(str(meteo_gpio.humidity2)+ " %")
			else:
				self.addRecord("DHT22 - neúspěšné měřeni VENKOVNI VLHKOSTI", True)
			#ESP
			if meteo_gpio.readEsp():
				self.builder.get_object("temperature_esp_label").set_text(str(meteo_gpio.teplotaEsp)+ " °C")
			else:
				self.addRecord("Esp - neodpovida", True)
			#BAROMETER
			#TLAK
			if meteo_gpio.readPress():
				self.builder.get_object("press_label").set_text(str(meteo_gpio.pressure)+ " Pa")
			else:
				self.addRecord("BMP - neúspěšné měření tlaku", True)
			#VYSKA
			if meteo_gpio.readAltitude():
				self.builder.get_object("altitude_label").set_text(str(meteo_gpio.altitude)+ m")
			else:
				self.addRecord("BMP - neuspesne zmerena vyska", True)
			#LIGHT
			if meteo_gpio.readLight():
				self.builder.get_object("label42").set_text(str(meteo_gpio.light)+ " lx")
				self.builder.get_object("levelbar1").set_value(float(meteo_gpio.light)/2000)
			else:
				self.addRecord("Světlo - neúspěšné měření", True)
			#info
			self.builder.get_object("label10").set_text(str(datetime.datetime.now().strftime("%H:%M:%S")))
			self.addRecord('Údaje senzorů aktualizovány')
		finally:
			return True

	def onclock_owm(self, enforce=False):
		try:
			if meteo_config.owm_enable or enforce:
				#print "clock_owm "+str(datetime.datetime.now().strftime("%H:%S"))
				response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id='+meteo_config.owm_location_id+'&appid='+meteo_config.owm_appid+'&units=metric&mode=json')
				data = json.loads(response.read())
				response.close()
				temperature = float(data['main']['temp'])
				humidity = float(data['main']['humidity']) 
				self.builder.get_object("label25").set_text(str(temperature)+ " °C")
				self.builder.get_object("label26").set_text(str(humidity)+ " %")
				#slunce vychazi
				self.builder.get_object("label35").set_text(datetime.datetime.fromtimestamp(int(data['sys']['sunrise'])).strftime('%H:%M'))
				#slunce zapada
				self.builder.get_object("label37").set_text(datetime.datetime.fromtimestamp(int(data['sys']['sunset'])).strftime('%H:%M'))
				#weather icon
				filename = data['weather'][0]['icon']
				if len(filename)>0:
					filename = filename + ".png"
					if not os.path.exists(filename):
						os.popen("wget http://openweathermap.org/img/w/"+filename)
					self.builder.get_object("image4").set_from_file(filename)
					self.builder.get_object("image4").show()
				#aktualizovano
				self.builder.get_object("label10").set_text(str(datetime.datetime.now().strftime("%H:%M:%S")))
				self.addRecord('OWM aktualizováno')
		except:
			self.addRecord('OWM chyba aktualizace',True)
		finally:	
			if enforce:
				return False
			return True
	
	def onclock_report(self, enforce=False):
		try:
			if meteo_config.server_enable or enforce:
				#print "clock_report "+str(datetime.datetime.now().strftime("%H:%S"))
				#self.builder.get_object("spinner1").set_visible(True)
				#self.pending_all()
				report_error = False
				textbuffer =  self.builder.get_object("textview1").get_buffer() 
				startiter, enditer = textbuffer.get_bounds() 
				urls_list = textbuffer.get_text(startiter, enditer,1).split('\n')
				for url in urls_list:
				  try:
					f = urllib2.urlopen(url.replace("{t1}",str(meteo_gpio.temperature1)).replace("{h1}",str(meteo_gpio.humidity1)).replace("{t2}",str(meteo_gpio.temperature2)).replace("{h2}",str(meteo_gpio.humidity2)).replace("{l}",str(meteo_gpio.light)))
					result_data = f.read().rstrip()
					f.close()
				  except:
					self.addRecord("Chyba odesílání dat na "+url, True)
					report_error = True
				self.addRecord("Data odeslána")
		finally:
			if enforce:
				return False
			return True

	def pending_all(self=None):
		try:
			while gtk.events_pending():
				gtk.main_iteration_do(True)
		finally:
			return True
	
	def addRecord(self,text,error=False):
		try:
			if error:
				text = 'ERROR! ' + text
			text = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S - ')+text+"\n"+self.builder.get_object("labellog").get_text()
			self.builder.get_object("labellog").set_text(text)
		except:
			pass
		try:
			if error and meteo_config.email_enable:
				s = meteo_config.email_smtp.split(':')
				smtp_server = s[0]
				smtp_port = s[1] 
				send_email(meteo_config.email_name, meteo_config.email_password, meteo_config.email_name, "METEOSTANICE", "ERROR - FULL LOG \n\n"+text, smtp_server, smtp_port)
		except:
			pass

	def menu_quit_onclick(self, button):
		gtk.main_quit()
	
	def menu_update_sensors_onclick(self, button):
		self.onclock_read_data()  

	def menu_send_report_onclick(self, button):
		self.onclock_report(True)  
  
	def menu_update_owm_onclick(self, button):
		self.onclock_owm(True)
	
	def menu_fullscreen_onclick(self, button):
		if isFullscreen:
			self.window.unfullscreen()
		else:
			self.window.fullscreen()
		
	def on_window1_state_event(self, widget, event, data=None):
		global isFullscreen
		isFullscreen = int(widget.get_window().get_state()) == 144
	
	def menu_about_onclick(self, button):
		# Create AboutDialog object
		dialog = gtk.AboutDialog.new()
		dialog.set_transient_for(button.get_parent().get_parent())
		dialog.set_program_name("Meteostanice")
		dialog.set_version(meteo_config.version)
		dialog.add_credit_section("Authors:", ['30-HellTech (github.com/HellTech/NAG_IoE_2016)', 'SOŠ strojní a elektrotechnická Velešín (www.sosvel.cz)'])
		dialog.set_license_type(gtk.License.GPL_3_0)
		dialog.set_copyright('(c) SOŠ Velešín')
		dialog.set_website("https://github.com/HellTech/NAG_IoE_2016/tree/master/30_HellTech_1602_1/08_Meteostanice_GUI_v2")
		dialog.set_website_label("Github page")
		dialog.set_comments("Tato aplikace vznikla v rámci projektu Meteostanice.")
		dialog.set_logo(Pixbuf.new_from_file('meteo_logo.png'))
		dialog.run()
		dialog.destroy()
	
	def on_report_switch_state_set(self, user_data, state):
		print state
		print user_data
		self.builder.get_object("spinbutton2").set_sensitive(state)
		self.builder.get_object("textview1").set_sensitive(state)
		
	def on_owm_switch_state_set(self, user_data, state):
		self.builder.get_object("entry3").set_sensitive(state)
		self.builder.get_object("entry1").set_sensitive(state)
		
	def on_email_switch_state_set(self, user_data, state):
		self.builder.get_object("email_name_entry").set_sensitive(state)
		self.builder.get_object("email_password_entry").set_sensitive(state)
		self.builder.get_object("email_smtp_entry").set_sensitive(state)
	
	def default_config_onclick(self, button):
		meteo_config.default_config(self)
		
	def save_config_onclick(self, button):
		meteo_config.save_config(self)

	def first_update(self):
		#owm
		self.onclock_owm()
		GLib.timeout_add_seconds(meteo_config.read_data_time, self.onclock_owm)
		#self.pending_all()
		#read sensors
		self.onclock_read_data()
		GLib.timeout_add_seconds(meteo_config.read_data_time, self.onclock_read_data)
		#self.pending_all()
		#report data
		self.onclock_report()
		GLib.timeout_add_seconds(meteo_config.report_time, self.onclock_report)
		return False

	def on_window1_show(self, window):
		#time
		GLib.timeout_add_seconds(1, self.onclock_time)
		GLib.timeout_add_seconds(2,self.first_update)
	
	def __init__(self):
		#prepare window
		self.gladefile = "meteo.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		#load config to GUI
		meteo_config.load_config_to_GUI(self)
		#spinnbutton fix
		adj = gtk.Adjustment(meteo_config.read_data_time, 1, 1000000, 1, 1, 1)
		spinBtn = self.builder.get_object("spinbutton1")
		spinBtn.configure(adj, 1, 0)
		adj2 = gtk.Adjustment(meteo_config.report_time, 1, 1000000, 1, 1, 1)
		spinBtn2 = self.builder.get_object("spinbutton2")
		spinBtn2.configure(adj2, 1, 0)
		#scrollwindow fix
		self.builder.get_object("textview1").set_wrap_mode(gtk.WrapMode.NONE)
		#show
		self.addRecord("start Meteostanice")
		self.window.show()
		#self.window.maximize()
		#self.window.fullscreen()
		

if __name__ == "__main__":
	try:
		main = Meteostation()
		gtk.main()
	except KeyboardInterrupt:
		#gtk.main_quit()
		#sys.exit(0)
		print
		pass
	finally:
		#GPIO.setwarnings(False)
		#GPIO.cleanup()
		#sys.exit(0)
		print
