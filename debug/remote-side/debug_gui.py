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
## Class MIDistCompAPIDebugGUIForRemote
###########################################################################

class MIDistCompAPIDebugGUIForRemote ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 620,430 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		#self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"MI Distribution Computing API Debug GUI For Remote", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer4.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"遠隔計算機側" ), wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 11, 3, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText29 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		fgSizer2.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText30 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"入力値", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		fgSizer2.Add( self.m_staticText30, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText31 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer2.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		self.m_buttonCalcRequest = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"calc-request", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCalcRequest, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText14 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		fgSizer2.Add( self.m_staticText14, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText13 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer2.Add( self.m_staticText13, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonCalcParams = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"calc-params", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCalcParams, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_textCtrlCalcParams = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlCalcParams, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText15 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		fgSizer2.Add( self.m_staticText15, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonCalcParamsComplete = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"calc-params-complete", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCalcParamsComplete, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_textCtrlCalcParamsComplete = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlCalcParamsComplete, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText16 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		fgSizer2.Add( self.m_staticText16, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonCalcStart = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"calc-start", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCalcStart, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_textCtrlCalcStart = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlCalcStart, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText17 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer2.Add( self.m_staticText17, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonCalcEnd = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"calc-end", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCalcEnd, 0, wx.RIGHT|wx.LEFT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrlCalcEnd = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlCalcEnd, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText18 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer2.Add( self.m_staticText18, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonSendResult = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"send-result", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonSendResult, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlSendResult = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlSendResult, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText19 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer2.Add( self.m_staticText19, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonEndSend = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"end-send", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonEndSend, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textCtrlEndSend = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.m_textCtrlEndSend, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText20 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		fgSizer2.Add( self.m_staticText20, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText22 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		fgSizer2.Add( self.m_staticText22, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText23 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		fgSizer2.Add( self.m_staticText23, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonClear = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonClear, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonGetInfo = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonGetInfo, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText25 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		fgSizer2.Add( self.m_staticText25, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText26 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		fgSizer2.Add( self.m_staticText26, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonSaveFiles = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Save Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonSaveFiles, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.LEFT, 5 )
		
		
		sbSizer2.Add( fgSizer2, 0, 0, 5 )
		
		
		bSizer5.Add( sbSizer2, 0, 0, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonCalcRequest.Bind( wx.EVT_BUTTON, self.m_buttonCalcRequestOnButtonClick )
		self.m_buttonCalcParams.Bind( wx.EVT_BUTTON, self.m_buttonCalcParamsOnButtonClick )
		self.m_buttonCalcParamsComplete.Bind( wx.EVT_BUTTON, self.m_buttonCalcParamsCompleteOnButtonClick )
		self.m_buttonCalcStart.Bind( wx.EVT_BUTTON, self.m_buttonCalcStartOnButtonClick )
		self.m_buttonCalcEnd.Bind( wx.EVT_BUTTON, self.m_buttonCalcEndOnButtonClick )
		self.m_buttonSendResult.Bind( wx.EVT_BUTTON, self.m_buttonSendResultOnButtonClick )
		self.m_buttonEndSend.Bind( wx.EVT_BUTTON, self.m_buttonEndSendOnButtonClick )
		self.m_buttonClear.Bind( wx.EVT_BUTTON, self.m_buttonClearOnButtonClick )
		self.m_buttonGetInfo.Bind( wx.EVT_BUTTON, self.m_buttonGetInfoOnButtonClick )
		self.m_buttonSaveFiles.Bind( wx.EVT_BUTTON, self.m_buttonSaveFilesOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_buttonCalcRequestOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonCalcParamsOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonCalcParamsCompleteOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonCalcStartOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonCalcEndOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonSendResultOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonEndSendOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonClearOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonGetInfoOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonSaveFilesOnButtonClick( self, event ):
		event.Skip()
	

