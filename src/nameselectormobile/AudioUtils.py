import librosa
import numpy as np
import pyaudio


# 加载音频文件
i = 0
def playSound(audio_path):
    global i
    i = 0
    audio, sr = librosa.load(audio_path, sr=None)
    def callback(in_data, frame_count, time_info, status):
        global i
        # 从音频数据中截取一部分
        audio_data = audio[frame_count * i:frame_count * (i + 1)]
        i += 1
        return (audio_data.tobytes(), pyaudio.paContinue)

    # 初始化PyAudio
    p = pyaudio.PyAudio()

    # 打开一个音频流
    stream = p.open(format=pyaudio.paFloat32,
                    channels=len(audio.shape),
                    rate=sr,
                    output=True,
                    stream_callback=callback)

    

    # 开始播放
    stream.start_stream()

    while stream.is_active():
        pass

    # 停止和关闭流
    stream.stop_stream()
    stream.close()

    # 终止PyAudio对象
    p.terminate()

if __name__ == '__main__':
    playSound(r"C:\Users\16928\Downloads\output.mp3")