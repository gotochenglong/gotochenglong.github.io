---
layout: post
title:  "使用WindowsAPI获取录音音频"
date:   2014-08-17 14:11 +0800
category: Windows
tags:   Windows声音
from:   http://www.cnblogs.com/qiusuo/p/3917617.html
---
<p><span style="line-height: 1.5;">介绍使用winmm.h进行音频流的获取</span></p>
<p>&nbsp;</p>
<p>首先需要包含以下引用对象</p>
<p>#include &lt;Windows.h&gt;<br />#include "mmsystem.h"<br />#pragma comment(lib, "winmm.lib")</p>
<p>音频的获取需要调用7个函数</p>
<p>1. waveInGetNumDevs：返回系统中就绪的波形声音输入设备的数量</p>
<div class="cnblogs_code">
<pre>UINT waveInGetNumDevs(VOID);</pre>
</div>
<p>2. waveInGetDevCaps：检查指定波形输入设备的特性</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MMRESULT waveInGetDevCaps( 
  UINT_PTR     uDeviceID,  
  LPWAVEINCAPS pwic,       
  UINT         cbwic       
);
</span><span style="color: #008000;">//</span><span style="color: #008000;">uDeviceID 音频输入设备标识,也可以为一个打开的音频输入设备的句柄.
</span><span style="color: #008000;">//</span><span style="color: #008000;">    个人认为如果上一步获得了多个设备，可以用索引标识每一个设备.
</span><span style="color: #008000;">//</span>    
<span style="color: #008000;">//</span><span style="color: #008000;">pwic 对WAVEINCAPS结构体的一个指针,包含设备的音频特性.
</span><span style="color: #008000;">//</span>
<span style="color: #008000;">//</span><span style="color: #008000;">cbwic WAVEINCAPS结构体的大小,使用sizeof即可.
</span><span style="color: #008000;">//</span>
<span style="color: #008000;">//</span><span style="color: #008000;">MMRESULT 函数执行的结果
</span><span style="color: #008000;">//</span><span style="color: #008000;">    MMSYSERR_NOERROR 表示执行成功
</span><span style="color: #008000;">//</span><span style="color: #008000;">    MMSYSERR_BADDEVICEID 索引越界 
</span><span style="color: #008000;">//</span><span style="color: #008000;">    MMSYSERR_NODRIVER 没有就绪的设备 
</span><span style="color: #008000;">//</span><span style="color: #008000;">    MMSYSERR_NOMEM 不能分配或者锁定内存</span></pre>
</div>
<p>&nbsp;介绍WAVEINCAPS结构体的含义</p>
<div class="cnblogs_code">
<pre>typedef <span style="color: #0000ff;">struct</span><span style="color: #000000;"> { 
    WORD      wMid;                </span><span style="color: #008000;">//</span><span style="color: #008000;">音频设备制造商定义的驱动程序标识</span>
    WORD      wPid;                <span style="color: #008000;">//</span><span style="color: #008000;">音频输入设备的产品标识</span>
    MMVERSION vDriverVersion;        <span style="color: #008000;">//</span><span style="color: #008000;">驱动程序版本号</span>
    TCHAR     szPname[MAXPNAMELEN];<span style="color: #008000;">//</span><span style="color: #008000;">制造商名称</span>
    DWORD     dwFormats;            <span style="color: #008000;">//</span><span style="color: #008000;">支持的格式,参见MSDN</span>
    WORD      wChannels;            <span style="color: #008000;">//</span><span style="color: #008000;">支持的声道数</span>
    WORD      wReserved1;            <span style="color: #008000;">//</span><span style="color: #008000;">保留参数</span>
} WAVEINCAPS;</pre>
</div>
<p>3. waveInOpen：打开指定的音频输入设备，进行录音</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MMRESULT waveInOpen(
  LPHWAVEIN       phwi,                </span><span style="color: #008000;">//</span><span style="color: #008000;">接收打开的音频输入设备标识的HWAVEIN结构的指针</span>
  UINT_PTR       uDeviceID,            <span style="color: #008000;">//</span><span style="color: #008000;">指定一个需要打开的设备标识.可以使用WAVE_MAPPER选择一个按指定录音格式录音的设备</span>
  LPWAVEFORMATEX pwfx,                <span style="color: #008000;">//</span><span style="color: #008000;">一个所需的格式进行录音的WAVEFORMATEX结构的指针 </span>
  DWORD_PTR      dwCallback,        <span style="color: #008000;">//</span><span style="color: #008000;">指向一个回调函数、事件句柄、窗口句柄、线程标识,对录音事件进行处理.</span>
  DWORD_PTR      dwCallbackInstance, <span style="color: #008000;">//</span><span style="color: #008000;">传给回调机制的参数</span>
  DWORD          fdwOpen            <span style="color: #008000;">//</span><span style="color: #008000;">打开设备的方法标识,指定回调的类型.参见CSDN</span>
);</pre>
</div>
<p>介绍WAVEFORMATEX结构体的含义</p>
<div class="cnblogs_code">
<pre>typedef <span style="color: #0000ff;">struct</span><span style="color: #000000;"> { 
    WORD  wFormatTag;        </span><span style="color: #008000;">//</span><span style="color: #008000;">波形声音的格式,单声道双声道使用WAVE_FORMAT_PCM.当包含在WAVEFORMATEXTENSIBLE结构中时,使用WAVE_FORMAT_EXTENSIBLE.</span>
    WORD  nChannels;        <span style="color: #008000;">//</span><span style="color: #008000;">声道数量</span>
    DWORD nSamplesPerSec;    <span style="color: #008000;">//</span><span style="color: #008000;">采样率.wFormatTag为WAVE_FORMAT_PCM时,有8.0kHz,11.025kHz,22.05kHz,和44.1kHz.</span>
    DWORD nAvgBytesPerSec;    <span style="color: #008000;">//</span><span style="color: #008000;">每秒的采样字节数.通过nSamplesPerSec * nChannels * wBitsPerSample / 8计算</span>
    WORD  nBlockAlign;        <span style="color: #008000;">//</span><span style="color: #008000;">每次采样的字节数.通过nChannels * wBitsPerSample / 8计算</span>
    WORD  wBitsPerSample;    <span style="color: #008000;">//</span><span style="color: #008000;">采样位数.wFormatTag为WAVE_FORMAT_PCM时,为8或者16</span>
    WORD  cbSize;            <span style="color: #008000;">//</span><span style="color: #008000;">wFormatTag为WAVE_FORMAT_PCM时,忽略此参数</span>
} WAVEFORMATEX;</pre>
</div>
<p>介绍dwCallback回调函数格式</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">void</span><span style="color: #000000;"> CALLBACK waveInProc(
  HWAVEIN hwi,          </span><span style="color: #008000;">//</span><span style="color: #008000;">回调此函数的设备句柄</span>
  UINT uMsg,            <span style="color: #008000;">//</span><span style="color: #008000;">波形声音输入信息,标识关闭(WIM_CLOSE)、缓冲区满(WIM_DATA)、打开(WIM_OPEN).</span>
  DWORD_PTR dwInstance, <span style="color: #008000;">//</span><span style="color: #008000;">用户在waveInOpen指定的数据</span>
<span style="color: #000000;">  DWORD_PTR dwParam1,   <span style="color: #008000;">//(LPWAVEHDR)dwParam1,用户指定的缓冲区</span>
  DWORD_PTR dwParam2     
);</span></pre>
</div>
<p>4. waveInPrepareHeader：为音频输入设备准备一个缓冲区</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MMRESULT waveInPrepareHeader(
  HWAVEIN hwi,    </span><span style="color: #008000;">//</span><span style="color: #008000;">音频输入设备句柄</span>
  LPWAVEHDR pwh,<span style="color: #008000;">//</span><span style="color: #008000;">指向WAVEHDR结构的指针,标识准备的缓冲区</span>
  UINT cbwh        <span style="color: #008000;">//</span><span style="color: #008000;">WAVEHDR结构的大小,使用sizeof即可</span>
);</pre>
</div>
<p><br />介绍WAVEHDR结构</p>
<div class="cnblogs_code">
<pre>typedef <span style="color: #0000ff;">struct</span><span style="color: #000000;"> wavehdr_tag { 
    LPSTR      lpData;          </span><span style="color: #008000;">//</span><span style="color: #008000;">指向波形格式的缓冲区</span>
    DWORD      dwBufferLength;  <span style="color: #008000;">//</span><span style="color: #008000;">缓冲区的大小</span>
    DWORD      dwBytesRecorded; <span style="color: #008000;">//</span><span style="color: #008000;">当前存储了多少数据</span>
    DWORD_PTR  dwUser;          <span style="color: #008000;">//</span><span style="color: #008000;">用户数据</span>
    DWORD      dwFlags;            <span style="color: #008000;">//</span><span style="color: #008000;">为缓冲区提供的信息,在waveInPrepareHeader函数中使用WHDR_PREPARED</span>
    DWORD      dwLoops;         <span style="color: #008000;">//</span><span style="color: #008000;">输出时使用,标识播放次数</span>
    <span style="color: #0000ff;">struct</span> wavehdr_tag * lpNext;<span style="color: #008000;">//</span><span style="color: #008000;">reserved</span>
    DWORD_PTR reserved;         <span style="color: #008000;">//</span><span style="color: #008000;">reserved</span>
} WAVEHDR, *LPWAVEHDR; </pre>
</div>
<p>5. waveInAddBuffer：将缓冲区发送给设备，若缓冲区填满，则不起作用。（参数同上）</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MMRESULT waveInAddBuffer(
  HWAVEIN hwi, 
  LPWAVEHDR pwh, 
  UINT cbwh 
); </span></pre>
</div>
<p>6. waveInStart：开始进行录制</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MMRESULT waveInStart(
  HWAVEIN hwi  </span><span style="color: #008000;">//设备句柄
</span>);</pre>
</div>
<p>7. waveInClose：关闭设备</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">MRESULT waveInClose(
  HWAVEIN hwi  </span><span style="color: #008000;">//设备句柄
</span>);</pre>
</div>
<p>&nbsp;如下示例：</p>
<p><a href="http://download.csdn.net/detail/long7782/7771019">http://download.csdn.net/detail/long7782/7771019</a></p>
<p>&nbsp;</p>
