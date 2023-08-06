from operator import methodcaller
from computeAudioQuality.mainProcess import computeAudioQuality
from ctypes import  *

def compute_audio_quality(metrics,testFile=None,refFile=None,cleFile=None,samplerate=16000,bitwidth=2,channel=1,refOffset=0,testOffset=0,maxComNLevel=-48.0,speechPauseLevel=-35.0):
    """
            self.maxComNLevel = c_double(kwargs['maxComNLevel'])
        self.speechPauseLevel = c_double(kwargs['speechPauseLevel'])
    :param metrics: G160/P563/POLQA/PESQ/STOI/STI/PEAQ/SDR/SII/LOUDNESS，必选项
    # G160 无采样率限制；  WAV/PCM输入 ；三端输入: clean、ref、test；无时间长度要求；
    # P563 8000hz(其他采样率会强制转换到8khz)；  WAV/PCM输入 ；单端输入: test；时长 < 20s；
    # POLQA 窄带模式  8k  超宽带模式 48k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # PESQ 窄带模式  8k   宽带模式 16k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # STOI 无采样率限制; 双端输入：ref、test；无时间长度要求；
    # STI >8k(实际会计算8khz的频谱)； WAV/PCM输入 ；双端输入：ref、test；时长 > 20s
    # PEAQ 无采样率限制；WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # SDR 无采样率限制; WAV/PCM输入 ; 双端输入：ref、test；无时间长度要求；
    不同指标输入有不同的采样率要求，如果传入的文件不符合该指标的要求，会自动变采样到合法的区间
    :param testFile: 被测文件，必选项
    :param refFile:  参考文件，可选项，全参考指标必选，比如POLQA/PESQ/PEAQ
    :param cleFile:  干净语音文件，可选项，三端输入必选，G160
    :param samplerate: 采样率，可选项，pcm文件需要 default = 16000
    :param bitwidth: 比特位宽度，可选项，pcm文件需要 default = 2
    :param channel: 通道数，可选项，pcm文件需要 default = 1
    :param refOffset: ref文件的样点偏移，可选项，指标G160需要
    :param testOffset: test文件的样点偏移，可选项，指标G160需要
    :return:
    """
    paraDicts = {
        'metrics':metrics,
        'testFile':testFile,
        'refFile':refFile,
        'cleFile':cleFile,
        'samplerate':samplerate,
        'bitwidth':bitwidth,
        'channel':channel,
        'refOffset':refOffset,
        'testOffset':testOffset,
        'maxComNLevel':maxComNLevel,
        "speechPauseLevel":speechPauseLevel
    }
    comAuQUA = computeAudioQuality(**paraDicts)
    return methodcaller(metrics)(comAuQUA)

if __name__ == '__main__':
    src = r'E:\martin\files\out16000.wav'
    dst = r'E:\files\result.pcm'
    ref = r'E:\04_git_clone\audiotestalgorithm\algorithmLib\wavin\noisySignal\16K\20dB\instrument_guzheng_short_20dB_Stationary_WhiteNoise.wav'
    test = r'E:\04_git_clone\audiotestalgorithm\algorithmLib\wavin\noisySignal\16K\20dB\MusicProtect\Protect_instrument_guzheng_short_20dB_Stationary_WhiteNoise.wav'
    cle = r'E:\04_git_clone\audiotestalgorithm\algorithmLib\wavin\clean\16K\music\instrument_guzheng_short.wav'
    print(compute_audio_quality('POLQA',testFile=test,refFile=cle))
    #print(compute_audio_quality('G160', testFile=src,refFile=src,samplerate=16000))


    pass