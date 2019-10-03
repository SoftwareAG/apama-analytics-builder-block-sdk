#
#  $Copyright (c) 2019 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or its subsidiaries and/or its affiliates and/or their licensors.$
#   This file is licensed under the Apache 2.0 license - see https://www.apache.org/licenses/LICENSE-2.0
#

from pysys.constants import *
from apamax.analyticsbuilder.basetest import AnalyticsBuilderBaseTest

class PySysTest(AnalyticsBuilderBaseTest):
	def execute(self):
		correlator = self.startAnalyticsBuilderCorrelator(blockSourceDir=f'{self.project.SOURCE}/blocks/')
		

		# Deploying a new model with correct parameter.
		self.createTestModel(['apamax.analyticsbuilder.samples.TimeWindow', 
				'apamax.analyticsbuilder.samples.Percentile',
				'apamax.analyticsbuilder.samples.Percentile',
				'apamax.analyticsbuilder.samples.Percentile'
				], {
				'0:durationSecs':10, 
				'1:percentile':15.0, 
				'2:percentile':50.0, 
				'3:percentile':80.0
			}, wiring=[
				'0:windowContents:1:window',
				'0:windowContents:2:window',
				'0:windowContents:3:window',
			]
		)
		
		# this window is 2 for 4 seconds, 1 for 1 seconds,  4 for 1 seconds, 3 for 4 seconds, then 5 for 5 seconds, 6 for 5 seconds.
		# at time 10, window is duration 8; 1 for 1s; 2 for 4s; 3 for 2s; 4 for 1s.  percentiles are 0-12.5=1; 12.5-62.5=2; 62.5-87.2=3, 87.5-100 = 4
		# at time 20, window is duration 10; 3 for 2s; 5 for 5s; 6 for 3s. Percentiles are 0-20=3; 20-70=5; 70-100=6
		self.sendEventStrings(correlator,
		                      self.timestamp(1.9),
		                      self.inputEvent('0:value', 2),
		                      self.timestamp(5.9),
		                      self.inputEvent('0:value', 1),
		                      self.timestamp(6.9),
		                      self.inputEvent('0:value', 4),
		                      self.timestamp(7.9),
		                      self.inputEvent('0:value', 3),
		                      self.timestamp(11.9),
							  self.inputEvent('0:value', 5),
		                      self.timestamp(16.9),
							  self.inputEvent('0:value', 6),
							  )
		self.assertGrep('output.evt', expr=self.outputExpr('1:output', 2)) # percentile 15
		self.assertGrep('output.evt', expr=self.outputExpr('2:output', 2)) # percentile 50
		self.assertGrep('output.evt', expr=self.outputExpr('3:output', 3)) # percentile 80
		self.sendEventStrings(correlator,
		                      self.timestamp(22),
							  )

		

	def validate(self):
		# Verifying that there are no errors in log file.
		self.checkLogs()
		
		self.assertGrep('output.evt', expr=self.outputExpr('1:output', 3)) # percentile 15
		self.assertGrep('output.evt', expr=self.outputExpr('2:output', 5)) # percentile 50
		self.assertGrep('output.evt', expr=self.outputExpr('3:output', 6)) # percentile 80
