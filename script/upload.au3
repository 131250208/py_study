WinWait("��","",10000);
ControlFocus("��", "", "Edit1");
ControlSetText("��" ,"", "Edit1", $CmdLine[1]);
Sleep(1000)
ControlClick("��", "","Button1");