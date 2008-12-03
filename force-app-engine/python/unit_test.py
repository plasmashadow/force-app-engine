# unit_test.py

import os
import beatbox

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler

class UnitTestHandler(RequestHandler):
	def get(self):
		self.redirect('/static/unit_test_login.html')
	
	def post(self):
		# Retrieve username and password from post data
		username = self.request.get('uid')
		password = self.request.get('pwd')
		
		# Attempt a login
		self.sforce = beatbox.PythonClient()
		try:
			login_result = self.sforce.login(username, password)
		except beatbox.SoapFaultError, errorInfo:
			path = os.path.join(os.path.dirname(__file__), 'templates/test_login_failed.html')
			self.response.out.write(template.render(path, {'errorCode': errorInfo.faultCode, 
			                                               'errorString': errorInfo.faultString}))
		else:
			# Grab the resulting session id
			template_values = {'user_id': login_result['userId'],
			                   'server_url': login_result['serverUrl'],
			                   'session_id': login_result['sessionId']};
		
			# Render the output
			path = os.path.join(os.path.dirname(__file__), 'templates/unit_test.html')
			self.response.out.write(template.render(path, template_values))
		