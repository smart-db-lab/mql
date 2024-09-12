import TextArea from "antd/es/input/TextArea";
import React, { useEffect } from "react";
import { FaMicrophone, FaStop } from "react-icons/fa";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
function AudioInput({audioTranscript, setAudioTranscript}) {
  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  useEffect(() => {
    if(transcript) {
        setAudioTranscript(transcript)
    }
  }, [transcript])

  return (
    <div className="mt-8">
      <div className="flex items-center gap-4 font-secondary justify-center">
        <h1>Click the button to record audio: </h1>
        <div>
          {listening ? (
            <button
              className="bg-orange-400 text-white p-3 rounded-full shadow-lg"
              onClick={SpeechRecognition.stopListening}
            >
              <FaStop size={20} />
            </button>
          ) : (
            <button
              className="bg-orange-400 text-white p-3 rounded-full shadow-lg"
              onClick={() => {
                resetTranscript();
                SpeechRecognition.startListening();
              }}
            >
              <FaMicrophone size={20} />
            </button>
          )}
        </div>
      </div>
      <div className="mt-6 text-right">
        <TextArea
          value={audioTranscript}
          onChange={(e) => setAudioTranscript(e.target.value)}
          rows={5}
          className="font-secondary text-gray-800"
        />
        <button className="mt-4 bg-blue-500 rounded text-white p-2 px-4 font-secondary font-semibold">
          Convert To DL
        </button>
      </div>
    </div>
  );
}

export default AudioInput;
