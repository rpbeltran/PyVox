import audio as AudioTools
import processcommand
import speechandtext
import thirdparty
import calculator
import random

microphone = AudioTools.Microphone()

print "Calibrating..."

microphone.getSampleVolume(3)

SWITCH_MODE_COMMAND = ["switch to mode", "which to mode", "switch mode",'which mode', 'switch to', 'which to']

modes = ['sendkeys','command','talk', 'calculate','calculator']
mode = "talk"
#sendkeys
#command
#talk
while True:

    print "\nCurrent Mode: %s"%mode
    print random.choice(('Speak to me your greatest desire:',
                         'Secrete commands verbally for eventual processing:',
                         'Release sounds for our thourough examination:',
                         'You know the drill: ', 'Speak friend, and enter:',
                         'Vomit up some juicy voice commands: '))

    listen = microphone.continuousListening()

    if listen == "long":

        print "That was too long for me I'm out"

    elif listen != "short":

        audioFile = listen

        text = SpeechAndText.speech_to_text(audioFile)
        print "You said: %s"%text

        if text:

            switched = False
            if text == 'recalibrate':
                    print "Calibrating..."
                    microphone.getSampleVolume(3)
                    switched = True
            for smc in SWITCH_MODE_COMMAND:     
                if text.startswith(smc):

                    if text[len(smc):].strip() in modes:
                        
                        mode = text[len(smc):].strip()
                        switched = True
                    else:
                        print 'unknown mode%s'%text[len(smc):]
            if switched:
                continue
            if mode == "sendkeys":

                ProcessCommand.sendkeys(text)

                result = False

            if mode == "command":

                result = ProcessCommand.run_command(text)

            if mode == "talk":

                result = thirdParty.askCleverBot(text)

            if mode == "calculate" or mode == "calculator":

                result = calculator.calculate(text)  
    
            
            SpeechAndText.text_to_speech(result)

            print '%s'%result
