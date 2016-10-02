from control import *
import time as t
from Alfie import *
import RPi.GPIO as GPIO

class Path:
	""" Path class for navigating alfie around the place """

	def __init__ (self):

		self.t1 = 0.05		#straight out gate
		self.v1 = 60	# % power

		self.t2 = 1			#turn left
		self.a2 = 55	#degrees (sort of)


		self.t3 = 0.7			#go straight

		self.t4 = 1		#turn left
		self.a4 = 55	#degrees (sort of)
	

		## t5 = True		actuate !! no longer used !!

		self.t6 = 15			#crossing ravine

		self.t7 = True		#release
		self.v7 = 60	# % power on restart

		self.t8 = 1.3			#turn right
		self.a8 = 2	#degrees (sort of)

		self.t9 = 1			#go straight

		self.t10 = 1		#stop

	def run(self, alfie):
		try:
			alfie.stage1(self.t1, self.v1)
			alfie.stage2(self.t2,self.a2)
			alfie.stage3(self.t3)
			alfie.stage4(self.t4,self.a4)
			alfie.stage6(self.t6)
			alfie.stage7(self.t7,self.v7)
			alfie.stage8(self.t8,self.a8)
			alfie.stage9(self.t9)
			alfie.stage10(self.t10)
		except KeyboardInterrupt:
			alfie.stage10(self.t10)
			print "\n--> Run stopped by user!"



alfie = Alfie()
