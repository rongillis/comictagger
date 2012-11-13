"""
A python class to manage communication with Comic Vine's REST API
"""

"""
Copyright 2012  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import json
from pprint import pprint 
import urllib2, urllib 
import math 
import re

from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtCore import QUrl, pyqtSignal, QObject, QByteArray

import utils
from settings import ComicTaggerSettings
from comicvinecacher import ComicVineCacher
from genericmetadata import GenericMetadata


class ComicVineTalker(QObject):

	def __init__(self, api_key):
		QObject.__init__(self)

		self.api_key = api_key


	def testKey( self ):
	
		test_url = "http://api.comicvine.com/issue/1/?api_key=" + self.api_key + "&format=json&field_list=name"
		resp = urllib2.urlopen( test_url ) 
		content = resp.read()
	
		cv_response = json.loads( content )

		# Bogus request, but if the key is wrong, you get error 100: "Invalid API Key"
		return cv_response[ 'status_code' ] != 100


	def searchForSeries( self, series_name , callback=None, refresh_cache=False ):
		
		# before we search online, look in our cache, since we might have
		# done this same search recently
		cvc = ComicVineCacher( ComicTaggerSettings.getSettingsFolder() )
		if not refresh_cache:
			cached_search_results = cvc.get_search_results( series_name )
			
			if len (cached_search_results) > 0:
				return cached_search_results
		
		original_series_name = series_name
	
		series_name = urllib.quote_plus(str(series_name))
		search_url = "http://api.comicvine.com/search/?api_key=" + self.api_key + "&format=json&resources=volume&query=" + series_name + "&field_list=name,id,start_year,publisher,image,description,count_of_issues&sort=start_year"

		resp = urllib2.urlopen(search_url) 
		content = resp.read()
	
		cv_response = json.loads(content)
	
		if cv_response[ 'status_code' ] != 1:
			print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
			return None

		search_results = list()
			
		# see http://api.comicvine.com/documentation/#handling_responses		

		limit = cv_response['limit']
		current_result_count = cv_response['number_of_page_results']
		total_result_count = cv_response['number_of_total_results']
		
		print ("Found {0} of {1} results".format( cv_response['number_of_page_results'], cv_response['number_of_total_results']))
		search_results.extend( cv_response['results'])
		offset = 0
		
		if callback is not None:
			callback( current_result_count, total_result_count )
			
		# see if we need to keep asking for more pages...
		while ( current_result_count < total_result_count ):
			print ("getting another page of results {0} of {1}...".format( current_result_count, total_result_count))
			offset += limit
			resp = urllib2.urlopen( search_url + "&offset="+str(offset) ) 
			content = resp.read()
		
			cv_response = json.loads(content)
		
			if cv_response[ 'status_code' ] != 1:
				print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
				return None
			search_results.extend( cv_response['results'])
			current_result_count += cv_response['number_of_page_results']
			
			if callback is not None:
				callback( current_result_count, total_result_count )

	
		#for record in search_results: 
		#	print( "{0}: {1} ({2})".format(record['id'], smart_str(record['name']) , record['start_year'] ) )
		#	print( "{0}: {1} ({2})".format(record['id'], record['name'] , record['start_year'] ) )
		
		#print "{0}: {1} ({2})".format(search_results['results'][0]['id'], smart_str(search_results['results'][0]['name']) , search_results['results'][0]['start_year'] ) 
	
		# cache these search results
		cvc.add_search_results( original_series_name, search_results )

		return search_results

	def fetchVolumeData( self, series_id ):
		
		# before we search online, look in our cache, since we might already
		# have this info
		cvc = ComicVineCacher( ComicTaggerSettings.getSettingsFolder() )
		cached_volume_result = cvc.get_volume_info( series_id )
		
		if cached_volume_result is not None:
			return cached_volume_result

	
		volume_url = "http://api.comicvine.com/volume/" + str(series_id) + "/?api_key=" + self.api_key + "&format=json"
		#print "search_url = : ", volume_url 

		resp = urllib2.urlopen(volume_url) 
		content = resp.read()
	
		cv_response = json.loads(content)

		if cv_response[ 'status_code' ] != 1:
			print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
			return None

		volume_results = cv_response['results']
	
		cvc.add_volume_info( volume_results )

		return volume_results
				

	def fetchIssueData( self, series_id, issue_number ):

		volume_results = self.fetchVolumeData( series_id )
	
		found = False
		for record in volume_results['issues']: 
			if float(record['issue_number']) == float(issue_number):
				found = True
				break
			
		if (found):
			issue_url = "http://api.comicvine.com/issue/" + str(record['id']) + "/?api_key=" + self.api_key + "&format=json"
			resp = urllib2.urlopen(issue_url) 
			content = resp.read()
			cv_response = json.loads(content)
			if cv_response[ 'status_code' ] != 1:
				print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
				return None
			issue_results = cv_response['results']

		else:
			return None
		
		# now, map the comicvine data to generic metadata
		metadata = GenericMetadata()
		
		metadata.series = issue_results['volume']['name']
		
		# format the issue number string nicely, since it's usually something like "2.00"
		num_f = float(issue_results['issue_number'])
		num_s = str( int(math.floor(num_f)) )
		if math.floor(num_f) != num_f:
			num_s = str( num_f )
			
		metadata.issueNumber = num_s
		metadata.title = issue_results['name']
		metadata.publisher = volume_results['publisher']['name']
		metadata.publicationMonth = issue_results['publish_month']
		metadata.publicationYear = issue_results['publish_year']
		metadata.issueCount = volume_results['count_of_issues']
		metadata.comments = self.cleanup_html(issue_results['description'])

		metadata.notes   = "Tagged with ComicTagger using info from Comic Vine:\n" 
		metadata.notes  += issue_results['site_detail_url']  
		
		metadata.webLink = issue_results['site_detail_url']  
		
		person_credits = issue_results['person_credits']
		for person in person_credits: 
			for role in person['roles']:
				# can we determine 'primary' from CV??
				role_name = role['role'].title()
				metadata.addCredit( person['name'], role['role'].title(), False )

		character_credits = issue_results['character_credits']
		character_list = list()
		for character in character_credits: 
			character_list.append( character['name'] )
		metadata.characters = utils.listToString( character_list )
	
		team_credits = issue_results['team_credits']
		team_list = list()
		for team in team_credits: 
			team_list.append( team['name'] )
		metadata.teams = utils.listToString( team_list )
	
		location_credits = issue_results['location_credits']
		location_list = list()
		for location in location_credits: 
			location_list.append( location['name'] )
		metadata.locations = utils.listToString( location_list )
	
		story_arc_credits = issue_results['story_arc_credits']
		for arc in story_arc_credits: 
			metadata.storyArc =  arc['name']
			#just use the first one, if at all
			break
	
		return metadata
	
	def cleanup_html( self, string):
			p = re.compile(r'<[^<]*?>')

			newstring = p.sub('',string)

			newstring = newstring.replace('&nbsp;',' ')
			newstring = newstring.replace('&amp;','&')
			
			return newstring

	
	def fetchIssueCoverURLs( self, issue_id ):

		cached_image_url,cached_thumb_url = self.fetchCachedIssueCoverURLs( issue_id )
		if cached_image_url is not None:
			return cached_image_url,cached_thumb_url

		issue_url = "http://api.comicvine.com/issue/" + str(issue_id) + "/?api_key=" + self.api_key + "&format=json&field_list=image"
		resp = urllib2.urlopen(issue_url) 
		content = resp.read()
		cv_response = json.loads(content)
		if cv_response[ 'status_code' ] != 1:
			print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
			return None, None
		
		image_url = cv_response['results']['image']['super_url']
		thumb_url = cv_response['results']['image']['thumb_url']
				
		if image_url is not None:
			self.cacheIssueCoverURLs( issue_id, image_url,thumb_url )
		return image_url,thumb_url
		
	def fetchCachedIssueCoverURLs( self, issue_id ):

		# before we search online, look in our cache, since we might already
		# have this info
		cvc = ComicVineCacher( ComicTaggerSettings.getSettingsFolder() )
		return  cvc.get_issue_image_url( issue_id )

	def cacheIssueCoverURLs( self, issue_id, image_url,thumb_url ):
		cvc = ComicVineCacher( ComicTaggerSettings.getSettingsFolder() )
		cvc.add_issue_image_url( issue_id, image_url, thumb_url )
		
		
#---------------------------------------------------------------------------
	urlFetchComplete = pyqtSignal( str , str, int)

	def asyncFetchIssueCoverURLs( self, issue_id ):
		
		self.issue_id = issue_id
		cached_image_url,cached_thumb_url = self.fetchCachedIssueCoverURLs( issue_id )
		if cached_image_url is not None:
			self.urlFetchComplete.emit( cached_image_url,cached_thumb_url, self.issue_id )
			return

		issue_url = "http://api.comicvine.com/issue/" + str(issue_id) + "/?api_key=" + self.api_key + "&format=json&field_list=image"
		self.nam = QNetworkAccessManager()
		self.nam.finished.connect( self.asyncFetchIssueCoverURLComplete )
		self.nam.get(QNetworkRequest(QUrl(issue_url)))

	def asyncFetchIssueCoverURLComplete( self, reply ):

		# read in the response
		data = reply.readAll()
		cv_response = json.loads(str(data))
		if cv_response[ 'status_code' ] != 1:
			print ( "Comic Vine query failed with error:  [{0}]. ".format( cv_response[ 'error' ] ))
			return 
		
		image_url = cv_response['results']['image']['super_url']
		thumb_url = cv_response['results']['image']['thumb_url']

		self.cacheIssueCoverURLs(  self.issue_id, image_url, thumb_url )

		self.urlFetchComplete.emit( image_url, thumb_url, self.issue_id ) 

