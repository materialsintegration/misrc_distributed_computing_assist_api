# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MIDistCompAPIDebugGUI
###########################################################################

class MIDistCompAPIDebugGUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 614,430 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		#self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"MI Distribution Computing API Debug GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"MIシステム側" ), wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 8, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"テストURL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"入力値", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText3 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonAddCalc = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"add-calc", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonAddCalc, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlAddCalc = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer1.Add( self.m_textCtrlAddCalc, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText4 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonAllowWaitCalc = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"allow-wait-calc", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonAllowWaitCalc, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlAllowWaitCalc = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer1.Add( self.m_textCtrlAllowWaitCalc, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_buttonCancelWaitCalc = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"cancel-wait-calc", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonCancelWaitCalc, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlCancelWaitCalc = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer1.Add( self.m_textCtrlCancelWaitCalc, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText7 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer1.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_buttonGetCalcInfo = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"get-calc-info", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonGetCalcInfo, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText8 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText9 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer1.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_buttonStatus = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"status", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonStatus, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlStatus = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer1.Add( self.m_textCtrlStatus, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText10 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.m_buttonGetCalcResult = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"get-calc-result", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonGetCalcResult, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlGetCalcResult = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer1.Add( self.m_textCtrlGetCalcResult, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText11 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		fgSizer1.Add( self.m_staticText23, 0, wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		fgSizer1.Add( self.m_staticText24, 0, wx.ALL, 5 )
		
		self.m_buttonClear = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_buttonClear, 0, wx.ALL, 5 )
		
		
		sbSizer1.Add( fgSizer1, 0, wx.EXPAND, 5 )
		
		
		bSizer3.Add( sbSizer1, 0, 0, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonAddCalc.Bind( wx.EVT_BUTTON, self.m_buttonAddCalcOnButtonClick )
		self.m_buttonAllowWaitCalc.Bind( wx.EVT_BUTTON, self.m_buttonAllowWaitCalcOnButtonClick )
		self.m_buttonCancelWaitCalc.Bind( wx.EVT_BUTTON, self.m_buttonCancelWaitCalcOnButtonClick )
		self.m_buttonGetCalcInfo.Bind( wx.EVT_BUTTON, self.m_buttonGetCalcInfoOnButtonClick )
		self.m_buttonStatus.Bind( wx.EVT_BUTTON, self.m_buttonStatusOnButtonClick )
		self.m_buttonGetCalcResult.Bind( wx.EVT_BUTTON, self.m_buttonGetCalcResultOnButtonClick )
		self.m_buttonClear.Bind( wx.EVT_BUTTON, self.m_buttonClearOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_buttonAddCalcOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonAllowWaitCalcOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonCancelWaitCalcOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonGetCalcInfoOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonStatusOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonGetCalcResultOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonClearOnButtonClick( self, event ):
		event.Skip()
	

