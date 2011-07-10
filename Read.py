import serial
import time
import sys
from os import system


class JoystickReader():
	
	def __init__(self):
		try :
			if sys.platform == "linux2":
				self.ser = serial.Serial('/dev/ttyUSB0', 9600)
			elif sys.platform == "darwin":
				self.ser = serial.Serial('/dev/tty.usbserial-A7005O9d', 9600) #Uncomment for OS X
			
		except : 
			print "Not able to find handcontroller"
			exit()
		self.command = OSInterface()
		if sys.platform == "linux2":
			self.command = OSInterfaceLinux()
		elif sys.platform == "darwin":
			self.command = OSInterfaceOSX()
		# Fix start pos
		#inp = self.ser.readline()
		self.startValueX = 529 #int(inp[5:9])
		self.xMax = 1023.0 - self.startValueX
		self.startValueY = 525 #int(inp[9:13])
		self.yMax = 1025.0 - self.startValueY
		self.clickDown = False
		

	def start(self):
		while 1:
			self.readInput()
	
	def readInput(self):
		inp = self.ser.readline()
		print inp	
		if len(inp) == 16:
			l = inp[1:2] #Button left
			if l == '0' :
				print "Key Left: "+l+" \n"
			r = inp[2:3] #Button right 
			if r == '0' and not self.clickDown: 
				print "Key Right: "+r+" \n"
				self.command.rightClick()
				self.clickDown = True
			if r == '1' and self.clickDown:
				self.clickDown = False
			u = inp[3:4] #Button up
			if u == '0': 
				print "Key Up: "+u+"\n"
			d = inp[4:5] #Button down
			if d == '0': 
				print "Key Down: "+d+"\n"
			
			#Horizontal joystick
			pushHorizontalPos = inp[5:9]
			procentageHorizontal = int(pushHorizontalPos) - self.startValueX 
			if procentageHorizontal != 0:
				procentageHorizontal = procentageHorizontal / self.xMax
				self.command.moveMouseX(procentageHorizontal)
			print str(procentageHorizontal) + "\n"
			
			#Vertical joystic
			pushVerticalPos = inp[9:13] 
			procentageVertical = int(pushVerticalPos) - self.startValueY
			if procentageVertical != 0:
				procentageVertical = procentageVertical/ self.yMax
				self.command.moveMouseY(procentageVertical)
			print str(procentageVertical) + "\n"
			
			
		else:
			print "length error \n"

class OSInterface():
	"""Only an interface should not be called"""
	def rightClick(self):
		raise NotImplementedError, "This is an interface and should not be called"
	def moveMouseY(self, speed):
		raise NotImplementedError, "This is an interface and should not be called"
	def moveMouseX(self, speed):
		raise NotImplementedError, "This is an interface and should not be called"

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
	
class OSInterfaceOSX(OSInterface):
	"""OS X specific wrapper for controlling the mouse/keyboard"""
	SENSITIVITY = 14
	def __init__(self):
		self.X = 0
		self.Y = 0
		self._mouseMove(self.X, self.Y)
		
	def rightClick(self):
		self._mouseclick(self.X, self.Y)
		
	def moveMouseY(self, speed):
		speed = -speed * OSInterfaceOSX.SENSITIVITY
		self.Y += speed
		self._mouseMove(self.X, self.Y)

	def moveMouseX(self, speed):
		speed = speed * OSInterfaceOSX.SENSITIVITY
		self.X +=speed
		self._mouseMove(self.X, self.Y)

	def _mouseEvent(self,type, posx, posy):
		theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
		CGEventPost(kCGHIDEventTap, theEvent)
	
	def _mouseMove(self, posx, posy):
		print "X: " + str(posx) + " Y: " + str(posy)
		self._mouseEvent(kCGEventMouseMoved, posx,posy)
		
	def _mouseclick(self, posx, posy):
		self._mouseEvent(kCGEventLeftMouseDown, posx,posy)
		self._mouseEvent(kCGEventLeftMouseUp, posx,posy)

class OSInterfaceLinux(OSInterface):
	"""Linux specific wrapper for controlling mouse/keyboard"""
	def rightClick(self):
		system("xte -x :0.0 'mouseclick 1'")

	def moveMouseY(self, speed):
		speed = -speed * 20
		system("xte -x :0.0 'mousermove 0 "+ str(int(speed)) +"'")

	def moveMouseX(self, speed):
		speed = speed * 20
		system("xte -x :0.0 'mousermove "+ str(int(speed)) +" 0'")
		

