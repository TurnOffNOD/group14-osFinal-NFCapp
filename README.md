## group14-osFinal-NFCapp
这是OS大作业第14组（选做实验3）的NFC驱动部分。 需要提前根据https://github.com/TurnOffNOD/linux_kernel_for_d1-OSFinal 的介绍使能uart5.

代码依赖：ndeflib库（pip3 install ndeflib）

用./get-wifi.py -h获取帮助信息。

在NFC板子上电第一次使用的时候，使用./get-wifi.py --wakeup True；之后不断电的情况下，再次收取数据使用./get-wifi.py即可

现在对实验3的实现进度：
读取用手机NFC以ndef格式写入的nfc卡，内容为wifi名称和密码，并且将收取到的ndef格式数据包以16进制输出在屏幕终端上。
