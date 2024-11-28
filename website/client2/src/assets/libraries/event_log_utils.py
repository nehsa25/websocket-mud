from winevt import EventLog
import iso8601
from xml.etree.cElementTree import Element

# from script utils
from log_utils import LogUtils

class EventLogUtils:
	@staticmethod
	def query_windows_events(log_to_query, query, test_start_time):
		# Re-query event log for errors
		LabListener_events = EventLog.Query(log_to_query, query, direction="backward")

		event_cnt = 0
		err_events = []
		for event in LabListener_events:
			event_data = {}
			event_cnt += 1
			event_element = Element(event.System)
			event_time_created = iso8601.parse_date(event_element.tag.TimeCreated['SystemTime'])
			event_record_id = event_element.tag.EventRecordID.cdata

			# stop if we're looking at events older than when the test started
			if event_time_created < test_start_time:
				break

			event_data['EventChannel'] = event_element.tag.Channel.cdata
			event_data['EventProvider'] = event_element.tag.Provider['Name']

			event_data['EventRecordID'] = event_record_id
			# this event has multiple data elements inside it
			if type(event.EventData.Data) == list:
				string_event_data = ''
				for x in range(len(event.EventData.Data)):
					string_event_data += '  {}: {}'.format(x, event.EventData.Data[x].cdata)

				event_data['Event_Data'] = string_event_data
			else:
				event_data['EventRecordID'] = event_record_id
				event_data['Event_Data'] = event.EventData.Data.cdata

			# add to our list
			err_events.append(event_data)

		return err_events

	@staticmethod
	def check_lablistener_events(test_start_time, logger=None):
		# Look for new error or critical events in the LabListener event log
		LabListener_log = 'LabListener'
		LabListener_events_query = 'Event/System[Level<=2]'
		return EventLogUtils.query_windows_events(LabListener_log, LabListener_events_query, test_start_time)
