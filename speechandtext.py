

#tts
ttsReady = False
ttsSetupFailed = False
SAPI_VOICE_MODULE = None

def text_to_speech(string):
    global ttsReady, ttsSetupFailed, SAPI_VOICE_MODULE
    if (not ttsReady) and (not ttsSetupFailed):
        #SAPI_VOICE_MODULE.Speak(string)
        try:
            import win32com.client
            SAPI_VOICE_MODULE = win32com.client.Dispatch("SAPI.SpVoice")
            ttsReady = True
        except:
            ttsReady = False
            ttsSetupFailed = True
            print "NO TTS!!!!!!!!!!!!!!!!!"

    if ttsReady:
        SAPI_VOICE_MODULE.Speak(string)
    else:
        return 'not tts ready'
#stt
import urllib2
def nth_index(string, substring, n, offset=0):

    if n > 0:

        return nth_index(string, substring, n - 1, string.find(substring, offset) + len(substring))

    return string.find(substring, offset)

def get_json_response_value(response, key, count):

    NAME_DELIMETER = '"'

    ASSOCIATOR = ':'
    
    PAIR_BEGIN_DELIMETER = '{'
    PAIR_END_DELIMETER = '}'

    BLOCK_BEGIN_DELIMETER = '['
    BLOCK_END_DELIMETER = ']'

    if count + 1 > response.count(key):

        return '%0|%0'

    value_offset = nth_index(response, key, count)
    slice_begin = value_offset + len(key + NAME_DELIMETER)

    slice_length = 0
    slice_skip = 0
    
    nest_level = 0
    in_value = False 

    for character in response[slice_begin:]:

        if character in (PAIR_BEGIN_DELIMETER, BLOCK_BEGIN_DELIMETER):

            nest_level += 1

            slice_skip += 1

        elif character in (PAIR_END_DELIMETER, BLOCK_END_DELIMETER):

            nest_level -= 1

        elif character in (ASSOCIATOR): 

            slice_skip += 1

            continue

        #Assumes no quote nesting
        elif character == NAME_DELIMETER:

            in_value = not in_value

            if in_value:

                slice_skip += 1

                nest_level += 1

            else:

                nest_level -= 1

        if nest_level == 0:

            break

        slice_length += 1

    return response[slice_begin + slice_skip : slice_begin + slice_length + 1]

def add_query_argument(key, value):

    return '&' + key + '=' + value

def speech_to_text(file_path):
               
    API_URL = 'https://www.google.com/speech-api/v2/recognize?'

    API_URL += add_query_argument('lang', 'en')
    API_URL += add_query_argument('key', 'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw')

    audio_data = open(file_path, 'rb').read()
    
    headers = {'Content-Type' : 'audio/x-flac; rate=16000',
               'User-Agent' : 'Mozilla/5.0'}
    
    request = urllib2.Request(API_URL, data=audio_data, headers=headers)
    response = urllib2.urlopen(request, timeout=40)
    
    speech_to_text_data = response.read()
    
    text = get_json_response_value(speech_to_text_data, "transcript", 0)
    
    if text != '%0|%0':
        return text
    else:
        return None



