import ConfigParser
import base64function

#default config
version = '2.02'
secret_id = "111AAA222BBB"
default_read_data_time = 30
default_server_enable = 1
default_report_time = 60
default_server_url = "http://ioe.zcu.cz/th.php?id="+secret_id+"&temperature={t2}&humidity={h2}"
default_owm_enable = 1
default_owm_location_id = "3063307"
default_owm_appid = "44db6a862fba0b067b1930da0d769e98"
default_email_enable = 1
default_email_name = "example@gmail.com"
default_email_password = "12345"
default_email_smtp = "smtp.gmail.com:587"

#variables
read_data_time = default_read_data_time
server_enable = default_server_enable
report_time = default_report_time
server_url = default_server_url
owm_enable = default_owm_enable
owm_location_id = default_owm_location_id
owm_appid = default_owm_appid
email_enable = default_email_enable
email_name = default_email_name
email_password = default_email_password
email_smtp = default_email_smtp

#load config from ini file
try:
	config = ConfigParser.SafeConfigParser()
	config.read('meteo.ini')
	read_data_time = int(config.get('main', 'read_data_time'))
	server_enable = int(config.get('main', 'server_enable'))
	report_time = int(config.get('main', 'report_time'))
	server_url = base64function.fromBase64(config.get('main', 'server_url'))
	owm_enable = int(config.get('main', 'owm_enable'))
	owm_location_id = config.get('main', 'owm_location_id')
	owm_appid = config.get('main', 'owm_appid')
	email_enable = int(config.get('main', 'email_enable'))
	email_name = config.get('main', 'email_name')
	email_password = base64function.fromBase64(config.get('main', 'email_password'))
	email_smtp = config.get('main', 'email_smtp')
except:
	pass

def load_config_to_GUI(self):
	global read_data_time,server_enable,report_time,server_url,owm_enable,owm_location_id,owm_appid,email_enable,email_name,email_password,email_smtp
	self.builder.get_object("spinbutton1").set_value(read_data_time)
	self.builder.get_object("switch1").set_active(server_enable)
	self.builder.get_object("spinbutton2").set_value(report_time)
	self.builder.get_object("textview1").get_buffer().set_text(server_url)
	self.builder.get_object("switch3").set_active(owm_enable)
	self.builder.get_object("entry3").set_text(owm_location_id)
	self.builder.get_object("entry1").set_text(owm_appid)
	self.builder.get_object("email_switch").set_active(email_enable)
	self.builder.get_object("email_name_entry").set_text(email_name)
	self.builder.get_object("email_password_entry").set_text(email_password)
	self.builder.get_object("email_smtp_entry").set_text(email_smtp)
	

def save_config(self):
	global read_data_time,server_enable,report_time,server_url,owm_enable,owm_location_id,owm_appid,email_enable,email_name,email_password,email_smtp
	#update config variable
	read_data_time = int(self.builder.get_object("spinbutton1").get_value())
	server_enable = int(self.builder.get_object("switch1").get_active())
	report_time = int(self.builder.get_object("spinbutton2").get_value())
	textbuffer =  self.builder.get_object("textview1").get_buffer()
	startiter, enditer = textbuffer.get_bounds() 
	server_url = str(textbuffer.get_text(startiter, enditer,1))
	owm_enable = int(self.builder.get_object("switch3").get_active())
	owm_location_id = str(self.builder.get_object("entry3").get_text())
	owm_appid = str(self.builder.get_object("entry1").get_text())
	email_enable = int(self.builder.get_object("email_switch").get_active())
	email_name = str(self.builder.get_object("email_name_entry").get_text())
	email_password = str(self.builder.get_object("email_password_entry").get_text())
	email_smtp = str(self.builder.get_object("email_smtp_entry").get_text())
	#enable/disable owm
	self.builder.get_object("label22").set_visible(owm_enable)
	self.builder.get_object("label25").set_visible(owm_enable)
	self.builder.get_object("label26").set_visible(owm_enable)
	self.builder.get_object("image4").set_visible(owm_enable)
	self.builder.get_object("label34").set_visible(owm_enable)
	self.builder.get_object("label35").set_visible(owm_enable)
	self.builder.get_object("label36").set_visible(owm_enable)
	self.builder.get_object("label37").set_visible(owm_enable)
	#save to config
	config = ConfigParser.SafeConfigParser()
	config.add_section('main')
	config.set('main', 'read_data_time', str(read_data_time))
	config.set('main', 'server_enable', str(server_enable))
	config.set('main', 'report_time', str(report_time))
	config.set('main', 'server_url', base64function.toBase64(server_url))
	config.set('main', 'owm_enable', str(owm_enable))
	config.set('main', 'owm_location_id', str(owm_location_id))
	config.set('main', 'owm_appid', str(owm_appid))
	config.set('main', 'email_enable', str(email_enable))
	config.set('main', 'email_name', str(email_name))
	config.set('main', 'email_password', base64function.toBase64(email_password))
	config.set('main', 'email_smtp', str(email_smtp))
	with open('meteo.ini', 'w') as f:
		config.write(f)
	
def default_config(self):
	global read_data_time,server_enable,report_time,server_url,owm_enable,owm_location_id,owm_appid,email_enable,email_name,email_password,email_smtp
	global defa1ult_read_data_time,default_server_enable,default_report_time,default_server_url,default_owm_enable,default_owm_location_id,default_owm_appid,default_email_enable,default_email_name,default_email_password,default_email_smtp
	read_data_time = default_read_data_time
	server_enable = default_server_enable
	report_time = default_report_time
	server_url = default_server_url
	owm_enable = default_owm_enable
	owm_location_id = default_owm_location_id
	owm_appid = default_owm_appid
	email_enable = default_email_enable
	email_name = default_email_name
	email_password = default_email_password
	email_smtp = default_email_smtp
	load_config_to_GUI(self)





