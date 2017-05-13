---
layout: post
title:  "Android Studio使用JNI和NDK进行开发"
date:   2016-07-10 22:41 +0800
category: 移动设计
tags:   Android
from:   http://www.cnblogs.com/qiusuo/p/5656625.html
---
<p><span style="line-height: 1.5;">想要学习一下在Android Studio中进行JNI的开发，文章挺多的，但是几乎没有一个完整的说明的，中间总是有一两步漏掉。分享技术就应该完整的让读者学会，藏着掖着不是君子所为。对于那些故意含糊过去的，我只想说Navie!</span></p>
<p>转载请注明出处&nbsp;http://www.cnblogs.com/qiusuo/p/5656625.html</p>
<p><span style="font-family: 'Microsoft YaHei';"><strong>正文</strong></span></p>
<p>JNI是JAVA标准平台中的一个重要功能，它弥补了JAVA的与平台无关这一重大优点的不足，在JAVA实现跨平台的同时，也能与其它语言（如C、C++）的动态库进行交互，给其它语言发挥优势的机会。</p>
<p>Android&nbsp;NDK（Native&nbsp;Development&nbsp;Kit&nbsp;）是一套工具集合，允许你用像C/C++语言那样实现应用程序的一部分。</p>
<ol>
<li>在使用NDK之前需要配置NDK和LLDB<br />通过使用SDK Manager找到NDK和LLDB，进行安装<br /><span style="line-height: 1.5;"><span style="line-height: 1.5;"><img src="http://images2015.cnblogs.com/blog/662741/201607/662741-20160708141749499-1037503493.png" alt="" width="510" height="328" /></span></span></li>
<li>
<p>按照一般方法，创建一个Android应用<br />File - New - New Project</p>












</li>
<li>创建一个新的Java Class（与MainActivity一个目录），类名为JniDemo，其中有一个Native方法<br />
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">package</span><span style="color: #000000;"> com.example.angel.myapplication;

</span><span style="color: #008000;">/**</span><span style="color: #008000;">
 * Created by Angel on 2016/7/8.
 </span><span style="color: #008000;">*/</span>
<span style="color: #0000ff;">public</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> JniDemo {
    </span><span style="color: #0000ff;">public</span> <span style="color: #0000ff;">native</span><span style="color: #000000;"> String getJniMessage();
}</span><span style="font-family: verdana, Arial, Helvetica, sans-serif; font-size: 14px; line-height: 1.5; background-color: #ffffff;">&nbsp;</span></pre>
</div>
</li>
<li>编译JniDemo.java这个带有Native方法的类<br />在命令提示符中，cd到文件所在目录，执行<span style="font-family: 'courier new', courier;">javac JniDemo.java</span>，可以看到目录中生成了对应的.class文件</li>
<li>生成对应的.h头文件<br />a) 在命令提示符中，cd到src/main/java文件夹中（内部的目录结构是包名，例如我的包名是<span style="font-family: 'Courier New'; font-size: 12px; line-height: 1.5;">com.example.angel.myapplication</span>，目录结构为/src/main/java/com/example/angel/myapplication）<br />b) 执行<span style="font-family: 'courier new', courier;">javah com.example.angel.myapplication.JniDemo</span>，会在当前目录生成head file(.h)文件。</li>
<li>在Project树形目录下app - src - main，建立jni folder，并将head file放到里边<br /><img src="http://images2015.cnblogs.com/blog/662741/201607/662741-20160708144707827-354981711.png" alt="" width="239" height="216" /><span style="line-height: 1.5;">&nbsp;</span>


</li>
<li>在jni文件夹中创建C/C++源文件，并include这个头文件，实现其中的方法。<br />
<div class="cnblogs_code">
<pre>#include <span style="color: #800000;">"</span><span style="color: #800000;">com_example_angel_myapplication_JniDemo.h</span><span style="color: #800000;">"</span><span style="color: #000000;">
JNIEXPORT jstring JNICALL Java_com_example_angel_myapplication_JniDemo_getJniMessage
  (JNIEnv </span>*<span style="color: #000000;">, jobject)
{
    </span><span style="color: #0000ff;">return</span> (*env)-&gt;NewStringUTF(env,<span style="color: #800000;">"</span><span style="color: #800000;">Jni Message: Hello World!</span><span style="color: #800000;">"</span><span style="color: #000000;">);
}</span></pre>
</div>
</li>
<li>build - Rebuild Project后，会出现一个错误。并且给出了解决方案：Set "android.useDeprecatedNdk=true" in gradle.properties to continue using the current NDK integration.<br />在gradle.properties中添加一行android.useDeprecatedNdk=true</li>
<li>build - Rebuild Project后，又会出现warming，NDK option is not configured。按照提示，进行如下内容的添加：<br />在app的build.gradle文件中，添加如下内容：<br />
<div class="cnblogs_code">
<pre><span style="color: #000000;">android {
<span style="color: #ff0000;">    sourceSets {
        main {
            jniLibs.srcDir 'src/main/jni'</span></span><span style="color: #000000;"><span style="color: #ff0000;">
        }
    }</span>
}</span></pre>
</div>
<p>并且自定义so库的名称</p>
<div class="cnblogs_code">
<pre><span style="color: #000000;">android {
    ......
    defaultConfig {
        ......
<span style="color: #ff0000;">        ndk {
            moduleName </span></span><span style="color: #ff0000;">'jnidemo'//自定义名称
</span><span style="color: #000000;"><span style="color: #ff0000;">        }</span>
    }
}</span></pre>
</div>
<p>如果不这么做的话，生成的库文件名称是[lib][module name].so</p>
</li>
<li>build - Rebuild Project，可以看到生成了so文件<br />在目录：app - build - intermediates - ndk - debug - lib下<br /><img src="http://images2015.cnblogs.com/blog/662741/201607/662741-20160710104526124-1032126050.png" alt="" width="215" height="177" /></li>
<li>加载so文件。<br />so文件加载一次便可以使用，一般情况下，在静态代码段中进行加载<br />
<div class="cnblogs_code">
<pre>    <span style="color: #0000ff;">static</span><span style="color: #000000;"> {
        System.loadLibrary(</span><span style="color: #800000;">"</span><span style="color: #800000;">jnidemo</span><span style="color: #800000;">"</span><span style="color: #000000;">);
    }</span></pre>
</div>
</li>
<li>使用Native方法<br />
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">public</span> <span style="color: #0000ff;">class</span> MainActivity <span style="color: #0000ff;">extends</span><span style="color: #000000;"> AppCompatActivity {
    </span><span style="color: #ff0000;">static {
        System.loadLibrary("jnidemo"</span><span style="color: #000000;"><span style="color: #ff0000;">);
    }</span>
    @Override
    </span><span style="color: #0000ff;">protected</span> <span style="color: #0000ff;">void</span><span style="color: #000000;"> onCreate(Bundle savedInstanceState) {
        </span><span style="color: #0000ff;">super</span><span style="color: #000000;">.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        </span><span style="color: #ff0000;">final JniDemo jniDemo = new JniDemo();
        TextView textView =</span><span style="color: #000000;"><span style="color: #ff0000;"> (TextView) findViewById(R.id.text);
        textView.setText(jniDemo.getHelloWordText());</span>
    }
}</span><span style="font-family: verdana, Arial, Helvetica, sans-serif; font-size: 14px; line-height: 1.5; background-color: #ffffff;">&nbsp;</span></pre>
</div>
</li>
<li>Native方法使用java代码<br />在Java代码中，创建如下方法，用以在Native代码中调用<br />
<div class="cnblogs_code">
<pre>    <span style="color: #0000ff;">protected</span> <span style="color: #0000ff;">void</span><span style="color: #000000;"> onCreate(Bundle savedInstanceState) {
        </span><span style="color: #0000ff;">super</span><span style="color: #000000;">.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        <span style="color: #ff0000;">sContext </span></span><span style="color: #ff0000;">=</span><span style="color: #000000;"><span style="color: #ff0000;"> getApplicationContext();</span>
    }
    </span><span style="color: #ff0000;">private static Context sContext;
    public static void showToast() {
        Toast.makeText(sContext, "此方法由Native方法调用", Toast.LENGTH_SHORT).show();
    }</span></pre>
</div>
<p>在Native代码中，使用如下代码进行调用</p>
<div class="cnblogs_code">
<pre>    <span style="color: #008000;">//</span><span style="color: #008000;">找到我们要调用的方法，注意包名+类名</span>
    jclass clazz = (*env)-&gt;FindClass(env,<span style="color: #800000;">"</span><span style="color: #800000;">com/example/angel/myapplication/MainActivity</span><span style="color: #800000;">"</span><span style="color: #000000;">);
    </span><span style="color: #008000;">//</span><span style="color: #008000;">获取某个静态方法的ID
    </span><span style="color: #008000;">//</span><span style="color: #008000;">clazz 是我们上面找到的类的字节码文件
    </span><span style="color: #008000;">//</span><span style="color: #008000;">showToast 是clazz类中的方法名
    </span><span style="color: #008000;">//</span><span style="color: #008000;">"()V" 这个表示方法的签名；()是方法的参数列表；V表示方法的返回类型；V -&gt; void</span>
    jmethodID id = (*env)-&gt;GetStaticMethodID(env,clazz, <span style="color: #800000;">"</span><span style="color: #800000;">showToast</span><span style="color: #800000;">"</span>,<span style="color: #800000;">"</span><span style="color: #800000;">()V</span><span style="color: #800000;">"</span><span style="color: #000000;">);
    </span><span style="color: #008000;">//</span><span style="color: #008000;">最后调用这个方法，CallStaticVoidMethod(clazz,方法ID)</span>
    (*env)-&gt;CallStaticVoidMethod(env,clazz,id);</pre>
</div>
<p>&nbsp;</p>
</li>
</ol>
