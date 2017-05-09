---
layout: post
title:  "使用WindowsAPI播放PCM音频"
date:   2014-08-17 16:29 +0800
categories: Windows声音
tag:    Windows声音
from:   http://www.cnblogs.com/qiusuo/p/3917910.html
---
<p>这一篇文章同上一篇《<a id="cb_post_title_url" href="http://www.cnblogs.com/qiusuo/p/3917617.html">使用WindowsAPI获取录音音频</a>》原理具有相似之处，不再详细介绍函数与结构体的参数</p>
<p>1. waveOutGetNumDevs</p>
<p>2. waveOutGetDevCaps</p>
<p>3. waveOutOpen</p>
<p>&nbsp;&nbsp;&nbsp; 回调函数</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">void</span> CALLBACK PlayCallback(HWAVEOUT hwaveout, UINT uMsg, DWORD dwInstance, DWORD dwParam1, DWORD dwParam2);</pre>
</div>
<p>4. waveOutPrepareHeader</p>
<p>5. waveOutWrite：执行后立即开始播放，当前缓冲区播放完成会调用回调函数</p>
<p>&nbsp;</p>
<p>注意：</p>
<p>为了能够连续播放，在第4部准备两个及以上播放数据</p>
<p>&nbsp;</p>
