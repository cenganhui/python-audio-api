import os
import wave

import pyaudio

# 录音文件名
input_filename = 'input.wav'
input_filepath = os.getcwd() + '/wav/'
# 录音文件路径
in_path = input_filepath + input_filename

'''
录音
'''


# 执行录音
def get_audio(filepath):
    aa = str(input('是否开始录音？（是/否）\n'))
    if aa == str('是'):
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = filepath
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print('*' * 10, '开始录音：请在5秒内输入语音')
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print('*' * 10, '录音结束\n')

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str('否'):
        exit()
    else:
        print('无效输入，请重新选择')
        get_audio(in_path)


if __name__ == '__main__':
    get_audio(in_path)
