from chess import Move
from speech_recogniton.speech_recognition import setup_and_run
class SpeechInput(object):
    def __init__(self, inputSource="/dev/somewhere"):
        # Launch a thread and stuff
        pass

    def speechCommand(self):
    	return setup_and_run()    
    def getCommand(self):
        """

        :return: Chess-formatted string of the most recent command recieved from the microphone
        :rtype: None|Move
        """
        # move = Move.from_uci(input("UCI move:"))
        # print(move)
        return input("UCI move: ")
