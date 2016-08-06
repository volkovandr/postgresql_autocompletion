#todo: reload settings if settings file is changed

import sublime_plugin
import sublime
import os
import json
import psycopg2
import re
from time import time


debug = True
settings_file = os.path.dirname(os.path.abspath(__file__)) + "\\postgresql_autocomplete.sublime-settings"
database="z"
port=""
user=""
host=""

class db_talker:

	def __del__(self):
		if self.ready:
			self.databaseDisconnect()

	def __init__(self):
		self.ready = False
		try:
			self.loadSettings()
			self.databaseConnect()
			print("PostgreSQL autocolmete started and ready")
		except Exception as e:
			print(e.args)
			print("PostgreSQL autocolmete can not initialize")

	def checkConnection(self):
		if debug: print("Checking if DB connection is still active")
		try:
			self.cur.execute("SELECT 1")
			if debug: print("DB connection is still active. user=" + user + ", host=" + host + ", port=" + port + ", database=" + database)
			return True
		except:
			self.ready = False
		try:
			print("DB connection lost. Trying to reconnect")
			self.databaseConnect()
			return True
		except Exception as e:
			print(e.args)
			return False

	def getSchemas(self):
		if debug: print("Retrieving shemas")
		schemas_info = []
		self.cur.execute("select oid, nspname from pg_namespace")
		for schemas_rows in self.cur:
			schemas_info.append((schemas_rows[0],schemas_rows[1]))
		if debug: print("Got schemas info about "+str(len(schemas_info)) + " schemas")
		return schemas_info

	def databaseDisconnect(self):
		if debug: print("Disconnecting from the database")
		self.cur.close()
		self.db.close()
		if debug: print("Disconnected from the database")

	def databaseConnect(self):
		if debug: print("Checking if it makes sense to try to connect")
		if 'failure_time' in locals() and time()-failure_time<60:
			if debug: print("Not now...")
			raise Exception("Less than a minute passed since last failure. Does not make sense to try again yet.")
		if debug: print("Connecting to the database")
		try:
			self.db = psycopg2.connect(user = user, host = host, port = port, database = database, connect_timeout = 1)
			for attempt in range (10):
				if self.db.poll() == psycopg2.extensions.POLL_OK:
					break
				if attempt == 10:
					raise Exception("Timeout connecting to the database")
				time.sleep(1)
		except Exception as e:
			print (e.args)
			# Failed to connect to the DB. Let us remember the time when that happened
			failure_time = time()
			raise Exception("Error connecting to the database")
		self.cur = self.db.cursor()
		self.cur.execute("SELECT 1")
		if self.cur.fetchone()[0] != 1: raise Exception("Connected to the database but can not execute a query")
		self.ready = True
		if debug: print("Connected to the database")

	def loadSettings(self):
		if debug: print ("Loading settings")
		self.checkFileExists()
		if debug: print ("Open JSON file")
		json_file = open(settings_file)
		if debug: print ("Parse JSON file")
		json_data = json.load(json_file)
		json_file.close()
		if debug: print(json_data)
		try:
			global host
			global database
			global port
			global user
			global backward_search
			global forward_search
			host = json_data["data_dictionary"]["host"]
			database = json_data["data_dictionary"]["database"]
			port = json_data["data_dictionary"]["port"]
			user = json_data["data_dictionary"]["user"]
		except KeyError:
			raise Exception("Can not find expected keys in the file")
		if debug: print("Settings loaded")

	def checkFileExists(self):
		if debug: print ("Check if settings file exists")
		if not os.path.exists(settings_file):
			raise Exception("Can not find settings file " + settings_file)
		if not os.path.isfile(settings_file):
			raise Exception("Can not find settings file " + settings_file)
		if debug: print ("Settings file does exist")

	def getRelations(self, schema_id):
		if debug: print("Retrieving relations for schema_id=" + str(schema_id))
		relations = []
		self.cur.execute("SELECT oid, relname, CASE relkind WHEN 'v' THEN 'view' WHEN 'r' THEN 'table' END AS relkind FROM pg_class WHERE relnamespace=%(oid)s AND relkind IN ('v','r')",{'oid': schema_id})
		for relations_rows in self.cur:
			relations.append((relations_rows[0],relations_rows[1],relations_rows[2]))
		if debug: print("Got info about "+str(len(relations)) + " relations")
		return relations

	def getFunctions(self, schema_id):
		if debug: print("Retrieving functions for schema_id=" + str(schema_id))
		functions = []
		self.cur.execute("SELECT oid, proname, 'function' AS relkind FROM pg_proc WHERE pronamespace = %(oid)s AND prorettype <> (SELECT oid FROM pg_type WHERE typname = 'trigger')", {'oid': schema_id})
		for function_rows in self.cur:
			functions.append((function_rows[0], function_rows[1], function_rows[2]))
		if debug: print("Got info about " + str(len(functions)) + " functions")
		return functions

	def getAttributes(self, relation_id):
		if debug: print("Retrieving attributes for relation_id=" + str(relation_id))
		attributes = []
		self.cur.execute("SELECT row_number() over(), attname, t.typname FROM pg_attribute a INNER JOIN pg_type t ON a.atttypid=t.oid WHERE attnum>0 AND NOT a.attisdropped AND a.attrelid = %(attrelid)s", {'attrelid': relation_id})
		for attribute_row in self.cur:
			attributes.append((attribute_row[0],attribute_row[1],attribute_row[2]))
		if debug: print("Got the info about "+str(len(attributes)) + " attributes")
		return attributes

DBTalker = db_talker()

class data_dictionary_autocomplete(sublime_plugin.EventListener):

	def on_query_completions(self, view, prefix, locations):
		#self.printsomestuff(view, prefix, locations)
		if not self.checkSyntax(view): return
		if not DBTalker.checkConnection(): return
		result = []
		schemas = DBTalker.getSchemas()
		previous_word = self.getPreviousWord(view, prefix)
		if previous_word == "":
			if debug: print("previous word is empty. Adding schemas to the autocolmetion list")
			for si in schemas: result.append((si[1]+"\tschema",si[1]+"."))
		else:
			in_schema = False
			# Check if the previous word is a schema-name. Then add tables and functions of that schema into autocolmetion list
			for schema_info in schemas:
				if schema_info[1] == previous_word:
					if debug: print("'" + previous_word + "'' is a schema name. Adding tables to the autocolmetion list")
					in_schema = True
					relations = DBTalker.getRelations(schema_info[0])
					for relation_info in relations: result.append((relation_info[1]+"\t"+relation_info[2] + " in " + schema_info[1],relation_info[1]))
					functions = DBTalker.getFunctions(schema_info[0])
					for function_info in functions: result.append((function_info[1]+"\t"+function_info[2] + " in " + schema_info[1],function_info[1]))
			if not in_schema:
				# the previous word is not a schema name. We suggest it is a table alias, and will return the list of its attributes
				if debug: print("'" + previous_word + "' is not a schema name. Trying to resolve table alias")
				renamed_objects = self.resolveAlias(view, previous_word, schemas)
				if debug: print("alias resolved to " + "; ".join(map(str, renamed_objects)))
				for renamed_object in renamed_objects:
					relations = DBTalker.getRelations(renamed_object[0])
					for relation in relations:
						if renamed_object[1] == relation[1]:
							attributes = DBTalker.getAttributes(relation[0])
							for attribute in attributes:
								result.append((attribute[1]+" "+attribute[2]+"\t"+renamed_object[2]+"."+relation[1],attribute[1]))
		result = list(set(result))
		return result

	def getQueryText(self, view):
		if debug: print("Trying to get the text of the whole query where the cursor is")
		#searching backwards until the beginning of the file or until semicolon
		beg = view.sel()[0].begin()-1
		while view.substr(beg)!=";" and beg>0:
			beg = beg - 1
		if view.substr(beg) == ";": beg=beg+2
		#searching forwards until the end of the file or until semicolon
		end = view.sel()[0].begin()
		while view.substr(end)!=";" and end<view.size():
			end=end+1
		query_text = view.substr(view.word(sublime.Region(beg, end))).strip() + "\n"
		#removing comments
		query_text = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", query_text)
		query_text = re.sub(re.compile("--.*?\n", re.DOTALL), "", query_text)
		if debug: print("The query: " + query_text)
		return query_text

	def resolveAlias(self, view, alias, schemas):
		text_buffer = self.getQueryText(view)
		result = []
		for schema_info in schemas:
			for match in re.finditer("\W"+schema_info[1]+"\.\w+\s+"+alias+"\W", text_buffer):
				ss = match.group(0).strip()[len(schema_info[1])+1:]
				m = re.match("^\w+", ss)
				result.append((schema_info[0],m.group(0),schema_info[1]))
			for match in re.finditer("\W"+schema_info[1]+"\."+alias+"\W", text_buffer):
				ss = match.group(0).strip()[len(schema_info[1])+1:]
				m = re.match("^\w+", ss)
				result.append((schema_info[0],m.group(0),schema_info[1]))
		return result

	def getPreviousWord(self, view, prefix):
		previous_word = ""
		point = view.sel()[0].begin()
		line = view.substr(view.line(point))
		col = view.rowcol(point)[1]
		what_is_before_prefix = "" if col == len(prefix) else line[col-len(prefix)-1]
		if what_is_before_prefix == ".":
			for c in reversed(line[0:col-len(prefix)-1]):
				if not re.match("\w",c): break
				previous_word = c + previous_word
		if debug: print("previous_word: " + previous_word)
		return previous_word

	def printsomestuff(self, view, prefix, Locations):
		print("prefix: " + prefix)
		region = view.sel()[0]
		point = region.begin()
		word = view.substr(view.word(point))
		line = view.substr(view.line(point))
		row = view.rowcol(point)[0]
		col = view.rowcol(point)[1]
		print("region: " + str(region))
		print("point: " + str(point))
		print("row: " + str(row) + " col: " + str(col))
		print("word: " + word)
		print("line: " + line)
		what_is_before_prefix = "" if col == len(prefix) else line[col-len(prefix)-1]
		print("what_is_before_prefix: " + what_is_before_prefix)
		if what_is_before_prefix == ".":
			previous_word = ""
			for c in reversed(line[0:col-len(prefix)-1]):
				if not re.match("\w",c): break
				previous_word = c + previous_word
			print("previous_word: " + previous_word)

	def checkSyntax(self, view):
		if debug: print("Checking syntax")
		if debug: print(view.settings().get('syntax'))
		if "PostgreSQL" in view.settings().get('syntax'):
			if debug: print("Syntax is PostgreSQL")
			return True
		else:
			if debug: print("Syntax is not PostgreSQL")
			return False

	def on_post_save(self, view):
		if os.path.basename(view.file_name()) == "postgresql_autocomplete.sublime-settings":
			DBTalker = db_talker()




