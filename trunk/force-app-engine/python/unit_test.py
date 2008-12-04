# unit_test.py

import os
import beatbox

import logging
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler

class UnitTestHandler(RequestHandler):
	def get(self):
		op = self.request.get('op')
		if (op == '' ):
			self.redirect('/static/unit_test_login.html')
	
		client = Client()
		
		if (op == 'query'): 
			soql = 'select name from Account limit 12'
			self.response.out.write('<b>'+soql+'</b>')   
			qr = client.query( soql )
			logging.info( qr )
			records = qr['records']
			for r in records : 	self.response.out.write('<li>' + r['Name'] )   
		
		
	def post(self):
		# Retrieve username and password from post data
		login_result = verifyLogin(self)
		if ( login_result == None ):
			# render a failed login
			path = os.path.join(os.path.dirname(__file__), 'templates/test_login_failed.html')
			self.response.out.write(template.render(path, 
				{'errorCode': memcache.get('errorCode'), 
			     'errorString': memcache.get('errorString') }))
			return
		
		# login was ok
		template_values = {'user_id': login_result['userId'],
			               'server_url': login_result['serverUrl'],
			               'session_id': login_result['sessionId']};
		# Render the output
		path = os.path.join(os.path.dirname(__file__), 'templates/unit_test.html')
		self.response.out.write(template.render(path, template_values))
		
		
def Client():
    bbox = beatbox.PythonClient()
    bbox.useSession(memcache.get('sessionId'), memcache.get('serverUrl'))
    return bbox
   		
def verifyLogin(self):
    """
    Insure that we have a session id or have a login username and can use it
    store our session info in memcache
    """
    username = self.request.get('uid')
    password = self.request.get('pwd')
    self.sforce = beatbox.PythonClient()
    login_result = None
    try:
	    login_result = self.sforce.login(username, password)
    except beatbox.SoapFaultError, errorInfo:
		memcache.set_multi( {'errorCode': errorInfo.faultCode, 
                             'errorString': errorInfo.faultString})
		
    else:
    	# caution: this method of storing session id is not viable for multiple users
    	# of this application since all users will have access to the same session id and concurrent
    	# users will overwrite this info. this method will work for a single user at a time 
        memcache.set_multi({ 
						   	'sessionId': login_result['sessionId'], 
			                'serverUrl': login_result['serverUrl'],
			                'metadataServerUrl' : login_result['metadataServerUrl'],
			                'userInfo': login_result['userInfo']} , time=3600)       
  
    logging.info( memcache.get("sessionId") )
    logging.info( memcache.get("serverUrl") )
    logging.info( memcache.get("metadataServerUrl") )
    logging.info( memcache.get("userInfo") )
    
    return login_result
	