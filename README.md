# fdu elearning(canvas) grab

This is a fork version of [skyhz/canvas_grab](https://github.com/skyzh/canvas_grab/). For more information, please refer to the original repository.

This is meant to be used by FDU students only.

## Getting Started

1. Install Python
2. Download canvas_grab source code. 
   * Go to [Release Page](https://github.com/ThisisKUNMENG/canvas_grab/releases) and download `{version}.zip`.
   * Or `git clone https://github.com/ThisisKUNMENG/canvas_grab`.
3. Run `./canvas_grab.sh` (Linux, macOS) or `.\canvas_grab.ps1` (Windows) in Terminal.
   Please refer to `Build and Run from Source` for more information.
4. Ignore API key (i.e. do not enter anything and press Enter) and enter your student ID and password.
5. Please don't modify any file inside download folder (e.g. take notes, add supplementary items). They will be overwritten upon each run.

You may interrupt the downloading process at any time. The program will automatically resume from where it stopped.


If you have any questions, feel free to file an issue [here](https://github.com/ThisisKUNMENG/canvas_grab/issues).

## Build and Run from Source

First of all, please install Python 3.8+, and download source code.

We have prepared a simple script to automatically install dependencies and run canvas_grab.

For macOS or Linux users, open a Terminal and run:

```bash
./canvas_grab.sh
```

For Windows users:

1. Right-click Windows icon on taskbar, and select "Run Powershell (Administrator)".
2. Run `Set-ExecutionPolicy Unrestricted` in Powershell.
3. If some courses in Canvas LMS have very long module names that exceed Windows limits (which will causes "No such file" error
   when downloading), run the following command to enable long path support.
   ```
   Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name LongPathsEnabled -Type DWord -Value 1 
   ```
4. Open `canvas_grab` source file in file browser, Shift + Right-click on blank area, and select `Run Powershell here`.
5. Now you can start canvas_grab with a simple command:
    ```powershell
    .\canvas_grab.ps1
    ```
   
The script also support several command line arguments, please refer to `./canvas_grab.sh -h` or `.\canvas_grab.ps1 -h` for more information.

## Configure

The setup wizard will automatically create a configuration for you.
You can change `config.toml` to fit your needs. If you need to
re-configure, run `./configure.sh` or `./configure.ps1`.

## Common Issues

* ~~**Acquire API token** Access Token can be obtained at "Account - Settings - New Access Token".~~
* ~~**FDU users** 请在[此页面](https://elearning.fudan.edu.cn/profile/settings)内通过“创建新访问许可证”按钮生成访问令牌。~~
  * 注意复旦Elearning虽然也有API token，但据本人测试，该token有效期即使设置为永久，也会在一段时间后失效，因此请使用账号密码登录。
* **An error occurred** You'll see "An error occurred when processing this course" if there's no file in a course.
* **File not available** This file might have been included in an unpublished unit. canvas_grab cannot bypass restrictions.
* **No module named 'canvasapi'** You haven't installed the dependencies. Follow steps in "build and run from source" or download prebuilt binaries.
  * 注意这里canvasapi库由本人进行了修改，因此在安装时请使用[此仓库](https://github.com/ThisisKUNMENG/canvasapi)内的canvasapi库。使用`pip install canvasapi`会导致安装的是原版canvasapi库，无法正常运行。使用`pip install -r requirements.txt`会正常安装canvasapi特供库。
* **Error when checking update** It's normal if you don't have a stable connection to GitHub. You may regularly check updates by visiting this repo.
* **Reserved escape sequence used** please use "/" as the path seperator instead of "\\".
* **Duplicated files detected** There're two files of same name in same folder. You should download it from Canvas yourself.

## Contributors

See [Contributors](https://github.com/skyzh/canvas_grab/graphs/contributors) list.
[@skyzh](https://github.com/skyzh), [@danyang685](https://github.com/danyang685) are two core maintainers.

## License

MIT

Which means that we do not shoulder any responsibilities for, included but not limited to:

1. API key leaking
2. Students' personal information, account and password leaking
3. Users upload copyright material from website to the Internet
