What is Force.com for Google App Engine?

Force.com for Google App Engine is a Python library and test harness that lets you access the Force.com Web services API from within Google App Engine applications. Once it is installed in your Google App Engine application, that application can start to seamless make callouts to the Force.com Web services API. This API lets you query and manipulate data in your Force.com environment - effectively letting you tap into the Force.com platform from within the application.

Currently, the toolkit supports many of the key Force.com Web Services APIs, allowing Google App Engine developers to create apps with direct access access to powerful Force.com functions. Some of the methods covered by the toolkit include Create , Update, Query, describeGlobal, and more.

For example, the following piece of Python code shows how easy it is to create a new Account record on Force.com from within an App Engine application:
```
sobjects = [] 
new_acc = { 'type': 'Account', 'name' : 'My New Account' } 
sobjects.append(new_acc) 
results = client.create(sobjects)
```
To get started, simply install the toolkit and then check out the User Guide (see Links)