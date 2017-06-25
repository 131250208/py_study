WinWait("打开","",10000);
ControlFocus("打开", "", "Edit1");
ControlSetText("打开" ,"", "Edit1", $CmdLine[1]);
Sleep(1000)
ControlClick("打开", "","Button1");