from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests

class EmployeeDetails(Action):
	def name(self):
		return 'API_action'
		
	def run(self, dispatcher, tracker, domain):
		
		id = tracker.get_slot('empID')
		request = tracker.get_slot('request')
		print("Employee ID: ",id)
		print("User Request: ",request)
		if request == 'details' or request == 'Details':
			Api = "http://easygoprod.us-e2.cloudhub.io/api/employee?id={}"
			resp = requests.get(Api.format(id))
			print(resp)
			if resp.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /tasks/ {}'.format(resp.status_code))
			else:
				json_data = resp.json()
				#print(json_data)
				fullName = json_data[0]['ownerName']
				emailID = json_data[0]['Email ID']
				department = json_data[0]['Department']
				dateOfJoinning = json_data[0]['Date of joining']
				mobNo = json_data[0]['Mobile Phone']
				reportingManager = json_data[0]['Reporting To']
				response = "Employee Details:\nEmployee_Name: {}\nEmailID: {}\nDepartment: {}\nDateOfJoinning: {}\nMobileNo: {}\nReportingManager: {}".format(fullName,emailID,department,dateOfJoinning,mobNo,reportingManager)
				dispatcher.utter_message(response)			
		elif request == 'timesheet' or request == 'Timesheet':
			Api = "http://easygoprod.us-e2.cloudhub.io/api/employee/timesheet?userid={}&sheetstatus=approved"
			resp = requests.get(Api.format(id))
			print(resp)
			if resp.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /tasks/ {}'.format(resp.status_code))
			else:
				json_data = resp.json()
				json_response = json_data['response']
				json_result = json_response['result']
				str1 = ""
				for each in json_result:
					str1=str1+"WeeksLog: "+each['timesheetName']+" TotalHours: "+each['totalHours']+" ApprovedTotalHours: "+each['approvedTotalHours']+" Status: "+each['status']+"\n"
				dispatcher.utter_message(str1)
		elif request == 'leaves' or request == 'Leaves':
			Api = "http://easygoprod.us-e2.cloudhub.io/api/employee/leaves?userid={}"
			resp = requests.get(Api.format(id))
			print(resp)
			if resp.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /tasks/ {}'.format(resp.status_code))
			else:
				json_data = resp.json()
				json_response = json_data['response']
				json_result = json_response['result']
				str2 = ""
				for each in json_result:
					str2=str2+"LeaveName: "+each['Name']+" TotalLeaves: "+str(each['PermittedCount'])+" UsedLeaves: "+str(each['AvailedCount'])+" BalanceLeave: "+str(each['BalanceCount'])+"\n"
				dispatcher.utter_message(str2)
		else:
			dispatcher.utter_message('Else Condition is working')
		

