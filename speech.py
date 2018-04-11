from chess import Move

class SpeechInput(object):
    def __init__(self, inputSource="/dev/somewhere"):
        # Launch a thread and stuff
        pass

    def getCommand(self):
        """

        :return: Chess-formatted string of the most recent command recieved from the microphone
        :rtype: None|Move
        """
        # move = Move.from_uci(input("UCI move:"))
        # print(move)
        return input("UCI move: ")
