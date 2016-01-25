#!/usr/bin/env python
# encoding: utf-8

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# --> let me know if you have ideas for improving
# --> Mark Froemberg aka DeutschMark @ GitHub
# --> www.markfromberg.com
#
# - ToDo
#	- 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import objc
# from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowNextMaster ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			self.masterDirection = 1
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "* Next Master"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

	def setNextMaser(self):
		self.masterDirection = 1
		

	def setPreviousMaser(self):
		self.masterDirection = -1

	def addMenuItemsForEvent_toMenu_(self, event, contextMenu):
		try:
			newMenuItemA = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Show Next Master", "setNextMaser", "")
			newMenuItemB = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Show Previous Master", "setPreviousMaser", "")
			newMenuItemA.setTarget_(self)
			newMenuItemB.setTarget_(self)
			contextMenu.addItem_(newMenuItemA)
			contextMenu.addItem_(newMenuItemB)
		except:
			self.logError(traceback.format_exc())

	
	def drawNextMaster( self, Layer ):

		Glyph = Layer.parent
		Font = Glyph.parent
		thisMaster = Font.selectedFontMaster
		masters = Font.masters

		activeMasterIndex = masters.index(thisMaster)

		if not "Original".lower() in thisMaster.name.lower():

			lastMasterInList = False

			if self.masterDirection == 1:
				if activeMasterIndex < len(masters) - 1:
					activeMasterIndex = activeMasterIndex
				else:
					activeMasterIndex = activeMasterIndex -1
					lastMasterInList = True
			if self.masterDirection == -1:
				if activeMasterIndex == 0:
					activeMasterIndex = activeMasterIndex +1
					lastMasterInList = True


			nextLayer = Layer.parent.layers[activeMasterIndex + self.masterDirection]
			
			if not lastMasterInList:
				drawingColor = 0.1, 0.5, 0.6, 0.45
			else:
				drawingColor = 0.1, 0.5, 0.6, 0.15
			

			# draw path AND components:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( *drawingColor ).set()
			try:
				thisBezierPathWithComponent = nextLayer.copyDecomposedLayer().bezierPath()
			except:
				thisBezierPathWithComponent = nextLayer.copyDecomposedLayer().bezierPath
			
			if thisBezierPathWithComponent:
				thisBezierPathWithComponent.fill()

		if "Original".lower() in thisMaster.name.lower():
			drawingColor = 1, 0, 0, 0.65 ### For Meta Science
			NSColor.colorWithCalibratedRed_green_blue_alpha_( *drawingColor ).set()
			try:
				thisBezierPathWithComponent = Layer.copyDecomposedLayer().bezierPath()
			except:
				thisBezierPathWithComponent = Layer.copyDecomposedLayer().bezierPath
			if thisBezierPathWithComponent:
				thisBezierPathWithComponent.fill()


	def drawBackgroundForLayer_( self, Layer ):
		try:
			# NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.drawNextMaster( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )

	def drawBackgroundForInactiveLayer_( self, Layer ):
		try:
			#pass
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.drawNextMaster( Layer )			
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def drawTextAtPoint( self, text, textPosition, fontSize=14.0, fontColor=NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.2, 0.0, 0.3 ) ):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	def getHandleSize( self ):
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except Exception as e:
			self.logToConsole( "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e) )
			return 7.0

	def getScale( self ):
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
