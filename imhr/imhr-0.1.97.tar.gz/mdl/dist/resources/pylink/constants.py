DONE_TRIAL=   0
TRIAL_OK  =   0
REPEAT_TRIAL= 1
SKIP_TRIAL  = 2
ABORT_EXPT  = 3
TRIAL_ERROR = -1 

RECORD_FILE_SAMPLES  = 1
RECORD_FILE_EVENTS   = 2
RECORD_LINK_SAMPLES  = 4
RECORD_LINK_EVENTS   = 8




STARTPARSE	=	1	
ENDPARSE	=	2	
STARTBLINK	=	3	#Pupil disappeared, time only
ENDBLINK	=	4	#Pupil reappeared (duration data)
STARTSACC	=	5	#Start of saccade (with time only)
ENDSACC		=	6	#End of saccade (with summary data)
STARTFIX	=	7	#Start of fixation (with time only)
ENDFIX		=	8	#End of fixation (with summary data)
FIXUPDATE	=	9	#Update within fixation, summary data for interval
BREAKPARSE	=	10	
STARTSAMPLES	=	15	
ENDSAMPLES	=	16	
STARTEVENTS	=	17	
ENDEVENTS	=	18	
MESSAGEEVENT	=	24	#User-definable text (IMESSAGE structure)
BUTTONEVENT	=	25	#Button state change (IOEVENT structure)
INPUTEVENT 	=	28	#Change of input port (IOEVENT structure)
SAMPLE_TYPE	=	200	#Event flags gap in data stream

#Event Type Flags
#The following specifies what types of events were written by tracker.
LEFTEYE_EVENTS	=	0x8000	#Has left eye events
RIGHTEYE_EVENTS	=	0x4000	#Has right eye events
BLINK_EVENTS	=	0x2000	#Has blink events
FIXATION_EVENTS	=	0x1000	#Has fixation events
FIXUPDATE_EVENTS=	0x0800	#Has fixation updates
SACCADE_EVENTS	=	0x0400	#Has saccade events
MESSAGE_EVENTS	=	0x0200	#Has message events
BUTTON_EVENTS	=	0x0040	#Has button events
INPUT_EVENTS	=	0x0020	#Has input port events

#Event Data Flags
#The following specifies what types of data were included in events by tracker.
EVENT_VELOCITY	=	0x8000	#Has velocity data
EVENT_PUPILSIZE	=	0x4000	#Has pupil size data
EVENT_GAZERES	=	0x2000	#Has gaze resolution
EVENT_STATUS	=	0x1000	#Has status flags
EVENT_GAZEXY	=	0x0400	#Has gaze x, y position
EVENT_HREFXY	=	0x0200	#Has head-ref x, y position
EVENT_PUPILXY	=	0x0100	#Has pupil x, y position
FIX_AVG_ONLY	=	0x0008	#Only average data to fixation events
START_TIME_ONLY	=	0x0004	#Only start-time in start events
PARSEDBY_GAZE	=	0x00C0	#Events were generated by GAZE data
PARSEDBY_HREF	=	0x0080	#Events were generated by HREF data
PARSEDBY_PUPIL	=	0x0040	#Events were generated by PUPIL data


#Some useful keys.
KB_BUTTON =0xFF00

F1_KEY    =0x3B00    
F2_KEY    =0x3C00
F3_KEY    =0x3D00
F4_KEY    =0x3E00
F5_KEY    =0x3F00
F6_KEY    =0x4000
F7_KEY    =0x4100
F8_KEY    =0x4200
F9_KEY    =0x4300
F10_KEY   =0x4400

PAGE_UP   = 0x4900
PAGE_DOWN = 0x5100
CURS_UP   = 0x4800
CURS_DOWN = 0x5000
CURS_LEFT = 0x4B00
CURS_RIGHT= 0x4D00

ESC_KEY   =0x001B
ENTER_KEY =0x000D
TERMINATE_KEY = 0x7FFF
JUNK_KEY  = 1


#Set of bit flags that mark mode function:
IN_DISCONNECT_MODE = 16384 # disconnected 
IN_UNKNOWN_MODE    = 0     # mode fits no class (i.e setup menu) 
IN_IDLE_MODE       = 1     # off-line 
IN_SETUP_MODE      = 2     # setup or cal/val/dcorr 
IN_RECORD_MODE     = 4     # data flowing 
IN_TARGET_MODE     = 8     # some mode that needs fixation targets 
IN_DRIFTCORR_MODE  = 16    # drift correction 
IN_IMAGE_MODE      = 32    # image-display mode 
IN_USER_MENU       = 64    # user menu 
IN_PLAYBACK_MODE   = 256 


EL_IDLE_MODE         =1
EL_IMAGE_MODE        =2
EL_SETUP_MENU_MODE   =3
EL_USER_MENU_1       =5
EL_USER_MENU_2       =6
EL_USER_MENU_3       =7
EL_OPTIONS_MENU_MODE =8  
EL_OUTPUT_MENU_MODE  =9
EL_DEMO_MENU_MODE    =10
EL_CALIBRATE_MODE    =11
EL_VALIDATE_MODE     =12
EL_DRIFT_CORR_MODE   =13
EL_RECORD_MODE       =14


KB_PRESS   =10
KB_RELEASE =-1
KB_REPEAT  =1






PUPIL_DIA_FLAG     =0x0001  # set if pupil is diameter (else area) 
HAVE_SAMPLES_FLAG  =0x0002  # set if we have samples 
HAVE_EVENTS_FLAG   =0x0004  # set if we have events 

HAVE_LEFT_FLAG     =0x8000  # set if we have left-eye data 
HAVE_RIGHT_FLAG    =0x4000  # set if we have right-eye data 

	# dropped events or samples preceding a read item 
	# are reported using these flag bits in "last_data_gap_types" 
	# Dropped control events are used to update 
	# the link state prior to discarding. 
DROPPED_SAMPLE  =0x8000
DROPPED_EVENT   =0x4000
DROPPED_CONTROL =0x2000

		# <link_dstatus> FLAGS 
DFILE_IS_OPEN    =0x80      # disk file active 
DFILE_EVENTS_ON  =0x40	   # disk file writing events 
DFILE_SAMPLES_ON =0x20      # disk file writing samples 
DLINK_EVENTS_ON  =0x08      # link sending events 
DLINK_SAMPLES_ON =0x04      # link sending samples 
DRECORD_ACTIVE   =0x01      # in active recording mode 

		# <link_flags> flags 
COMMAND_FULL_WARN =0x01     # too many commands: pause 
MESSAGE_FULL_WARN =0x02     # too many messages: pause 
LINK_FULL_WARN    =0x04     # link, command, or message load 
FULL_WARN         =0x0F     # test mask for any warning 

LINK_CONNECTED    =0x10     # link is connected 
LINK_BROADCAST    =0x20     # link is broadcasting 
LINK_IS_TCPIP     =0x40     # link is TCP/IP (else packet) 


#*********** STATUS FLAGS (samples and events) ***************

LED_TOP_WARNING       =0x0080    # marker is in border of image
LED_BOT_WARNING       =0x0040
LED_LEFT_WARNING      =0x0020
LED_RIGHT_WARNING     =0x0010
HEAD_POSITION_WARNING =0x00F0    # head too far from calibr???

LED_EXTRA_WARNING     =0x0008    # glitch or extra markers
LED_MISSING_WARNING   =0x0004    # <2 good data points in last 100 msec)
HEAD_VELOCITY_WARNING =0x0001    # head moving too fast

CALIBRATION_AREA_WARNING =0x0002  # pupil out of good mapping area

MATH_ERROR_WARNING   =0x2000  # math error in proc. sample

# THESE CODES ONLY VALID FOR EYELINK II 

            # this sample interpolated to preserve sample rate
            # usually because speed dropped due to missing pupil
			 
INTERP_SAMPLE_WARNING =0x1000
             
				#pupil interpolated this sample
				#usually means pupil loss or
				#500 Hz sample with CR but no pupil
			
INTERP_PUPIL_WARNING  =0x8000

            # all CR-related errors 
CR_WARNING       =0x0F00
CR_LEFT_WARNING  =0x0500
CR_RIGHT_WARNING =0x0A00

            # CR is actually lost 
CR_LOST_WARNING        =0x0300
CR_LOST_LEFT_WARNING   =0x0100
CR_LOST_RIGHT_WARNING  =0x0200

            # this sample has interpolated/held CR 
CR_RECOV_WARNING       =0x0C00
CR_RECOV_LEFT_WARNING  =0x0400
CR_RECOV_RIGHT_WARNING =0x0800



SAMPLE_LEFT      = 0x8000  # data for these eye(s) 
SAMPLE_RIGHT     = 0x4000
SAMPLE_TIMESTAMP = 0x2000  # always for link, used to compress files 
SAMPLE_PUPILXY   = 0x1000  # pupil x,y pair 
SAMPLE_HREFXY    = 0x0800  # head-referenced x,y pair 
SAMPLE_GAZEXY    = 0x0400  # gaze x,y pair 
SAMPLE_GAZERES   = 0x0200  # gaze res (x,y pixels per degree) pair 
SAMPLE_PUPILSIZE = 0x0100  # pupil size 
SAMPLE_STATUS    = 0x0080  # error flags 
SAMPLE_INPUTS    = 0x0040  # input data port 
SAMPLE_BUTTONS   = 0x0020  # button state: LSBy state, MSBy changes 
SAMPLE_HEADPOS   = 0x0010  # head-position: byte tells # words 
SAMPLE_TAGGED    = 0x0008  # reserved variable-length tagged 
SAMPLE_UTAGGED   = 0x0004  # user-defineabe variable-length tagged 

MISSING_DATA = -32768


BX_AVERAGE     =0   # average combined pixels                          
BX_DARKEN      =1   # choose darkest (keep thin dark lines)          
BX_LIGHTEN     =2   # choose darkest (keep thin white lines)         
BX_MAXCONTRAST =4   # stretch contrast to black->white               
BX_NODITHER    =8   # No dither, just quantize                       
BX_GRAYSCALE   =16  

SV_NOREPLACE   =1   # do not replace if the file already exists      
SV_MAKEPATH    =2   # make destination path if does not already exists


#sample model for velocity and acceleration calculation
FIVE_SAMPLE_MODEL =1
NINE_SAMPLE_MODEL =2
SEVENTEEN_SAMPLE_MODEL =3
EL1000_TRACKER_MODEL =4

#EYELINK constant
EYELINK= None


#constants used for cross hair
CR_HAIR_COLOR=1
PUPIL_HAIR_COLOR=2
PUPIL_BOX_COLOR=3
SEARCH_LIMIT_BOX_COLOR=4
MOUSE_CURSOR_COLOR=5

#constants used for beep
CAL_ERR_BEEP   =-1
DC_ERR_BEEP    =-2
CAL_GOOD_BEEP  = 0
CAL_TARG_BEEP  = 1
DC_GOOD_BEEP   = 2
DC_TARG_BEEP   = 3


# SAMPLE STATUS BITS:
# These are for eye or target at edges
HPOS_TOP_WARNING       =0x0080    # marker is in border of image
HPOS_BOT_WARNING       =0x0040
HPOS_LEFT_WARNING      =0x0020
HPOS_RIGHT_WARNING     =0x0010
HEAD_POSITION_WARNING  =0x00F0    # head too far from calibr???
#
# These flag target conditions:
#                                #
HPOS_ANGLE_WARNING     =0x0008   # target at too great an angle for accuracy
HPOS_MISSING_WARNING   =0x0004   # target is missing
HPOS_DISTANCE_WARNING  =0x0001   # too close or too far


# TARGET STATUS FLAGS:
# These are available through the HTARGET data type
# ( htype==0xB4, hdata = tx, ty, distance, flags
#   where tx, ty range from 0 to 10000
#   distance = 10*mm
#
#  TARGET WARNINGS
TFLAG_MISSING   =0x4000    # missing
TFLAG_ANGLE     =0x2000    # extreme target angle
TFLAG_NEAREYE   =0x1000    # target near eye so windows overlapping
#  DISTANCE WARNINGS (limits set by remote_distance_warn_range command)
TFLAG_CLOSE     =0x0800    # distance vs. limits
TFLAG_FAR       =0x0400
# TARGET TO CAMERA EDGE  (margin set by remote_edge_warn_pixels command)
TFLAG_T_TSIDE   =0x0080    # target near edge of image (left, right, top, bottom)
TFLAG_T_BSIDE   =0x0040
TFLAG_T_LSIDE   =0x0020
TFLAG_T_RSIDE   =0x0010
# EYE TO CAMERA EDGE  (margin set by remote_edge_warn_pixels command)
TFLAG_E_TSIDE   =0x0008    # eye near edge of image (left, right, top, bottom)
TFLAG_E_BSIDE   =0x0004
TFLAG_E_LSIDE   =0x0002
TFLAG_E_RSIDE   =0x0001

#external device control
EXTERNAL_DEV_NONE  =0
EXTERNAL_DEV_CEDRUS = 1
EXTERNAL_DEV_SYS_KEYBOARD = 2