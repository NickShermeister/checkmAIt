#!/usr/bin/env python

from __future__ import division
import re
import sys
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# A nonzero amount of this is from the Google Cloud Services docs.
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.




    responses : Audio stream
    returns : strings constructed in chess notation
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            string_attempt = attempt_command_string(transcript)
            if string_attempt:
                return string_attempt
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
            num_chars_printed = 0



def attempt_command_string(feed):
    """
    Tries to create a command string for chess based on the input. 
    To be used with the text stream
    """
    # Make an informed guess on what the command is.
    pieces = ["knight", "queen", "king", "pawn", "bishop", "rook", "work", \
              "night", "Night", "brooke"]      
    rows = ["1", "2", "3", "4", "5", "6", "7", "8"]                             
    cols = ["B", "C", "D", "F", "G", "H", "A", "E", "b", "c", "a", "d", "e", "f"]
    command_string = ""
    feed = feed.encode('ascii','ignore')
    feed = feed.strip()
    feed_list = feed.split(" ")
    

    # Go through the feedlist, converting to chess notation
    command_string += ""
    if len(feed_list) < 2:
        return
    
    # Empirically found common mistakes revealed through testing with 
    # logitech webcam microphone.
    if feed_list[0].lower() in pieces:
        piece = feed_list[0].lower()
        # print(piece)
        if piece == "knight" or piece == "Knight" or \
           piece == "night" or piece == "Night":
            command_string += "N"
        elif piece == "work" or piece == "brooke":
            command_string += "R"
        else:
            command_string += piece[0].upper()

    if feed_list[1] == "from": 
        command_string += make_string(feed_list[2],rows, cols)
        command_string += make_string(feed_list[-1],rows, cols)

    else:
        command_string += make_string(feed_list[-1],rows, cols)
  
    # Hardcoding in whether or not this is chess notation. Can be changed.
    if len(command_string) not in [3, 5]:
        print("Failed.")
        return    

    # print(command_string)
    return command_string

def make_string(string, rows, cols):
    """
    Finds rows and columns in given string or substring.
    """
    command_string = "" 
    for row in rows:                                                        
        if row in string:                                                     
            command_string += row 
            break                                          
    for col in cols:                                                        
        if col in string: 
            command_string += col.lower()  
            break
    return command_string
    
def  main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        return listen_print_loop(responses)

if __name__ == '__main__':
    main()
