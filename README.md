# HashMaster
*Various types of hash code operations*
*多种类型的哈希值操作*

---
## 1.Intro 简介
**HashMaster** is a lightweight hash processing program that uses wxPython for its frontend and hashlib for its backend. It aims to provide users with the simplest and most user-friendly features.
**HashMaster** 是一个轻量级的哈希处理程序，其前端使用 wxPython，后端使用 hashlib。它旨在为用户提供最简单和最用户友好的功能。

Each program comes with both a non-GUI and a GUI version. The non-GUI version offers the simplest operations and code, making it easier to understand. The GUI version supports more complex operations, providing a more advanced and user-friendly experience.
每个程序都有 GUI 和非 GUI 版本。非 GUI 版本提供最简单的操作和代码，更易于理解。GUI 版本支持更复杂的操作，提供更高级和更友好的用户体验。

Due to my limited capabilities, the code may have some imperfections. I warmly welcome everyone to share their suggestions and contribute to the project. For more details, please see the Contribution. Thank you for your understanding!
由于我的能力有限，代码可能存在一些不完善之处。我热烈欢迎大家提出建议并为该项目做出贡献。有关详细信息，请参见“贡献”部分。感谢您的理解！

---
## 2.Functions 功能

### 2.1. Strcucture 结构

This is the structure of this project:
这是该项目的结构：

![Structure](https://github.com/user-attachments/assets/3d2670c8-bc72-4ca1-b0ce-398cf0cc5cc6)


### 2.2. Info about HashChecker

When you have a hash value and content that needs to be verified (text, file, or folder), **HashChecker** can assist you. Simply input the hash value and provide the content to be verified (text can be entered directly, while files and folders can be selected via their paths). The program will automatically match the verification format (supporting SHA256, SHA512, and MD5) and provide you with the result.
当你有一个哈希值并需要验证内容（文本、文件或文件夹）时，**HashChecker** 可以帮助你。只需输入哈希值并提供需要验证的内容（文本可以直接输入，文件和文件夹可以通过路径选择），程序会自动匹配验证格式（支持 SHA256、SHA512 和 MD5），并为你提供结果。
### 2.3. Info about HashGenerator

If you want to generate a hash for your content, **HashGenerator** is an excellent choice. Whether it's text, a file, or a folder, it can generate the corresponding hash value. If you're using the GUI version, the program also includes a "Copy to Clipboard" feature, eliminating the need for manual selection. It's just that user-friendly.
如果你想为内容生成哈希值，**HashGenerator** 是一个很好的选择。无论是文本、文件还是文件夹，它都可以生成相应的哈希值。如果你使用的是 GUI 版本，程序还包含“复制到剪贴板”功能，无需手动选择，极其方便用户使用。

---
## 3. Required environment 运行环境

Python version should be at least 3.10.
Python 版本应至少为 3.10。

All GUI-version files require `wxPython`:
所有 GUI 版本文件需要安装 `wxPython`：
```bash
pip install wxPython
```

**HashGenerator_GUI.py** requires `pyperclip`:
**HashGenerator_GUI.py** 还需要安装 `pyperclip`：
```bash
pip install pyperclip
```

---
## 4. Examples 实例

### 4.1. HashGenerator
Text input:
文本输入：
![Generator_text](https://github.com/user-attachments/assets/9cd4b894-9217-405e-b557-db56557411a4)

File input:
文件输入：
![Generator_file](https://github.com/user-attachments/assets/b09c19cd-f25c-4bec-849e-9e0e72db2a39)

Folder input:
文件夹输入：
![Generator_folder](https://github.com/user-attachments/assets/5632217c-9b52-4546-a071-a03a675c640f)

### 4.2 HashChecker
Text input:
文本输入：
![Check_text](https://github.com/user-attachments/assets/f5870fc7-8a17-4fb8-ab51-da2cf07a9292)

File input:
文件输入：
![Check_file](https://github.com/user-attachments/assets/7aab8bc6-3abf-4b38-ba90-7c2563b0f5c3)

Folder input:
文件夹输入：
![Check_folder](https://github.com/user-attachments/assets/3d1b3e9c-db18-4da0-a475-acd47129e61d)

---

## 5. Contribution 贡献

Contributions are welcome! Follow these steps:
欢迎贡献！请按照以下步骤操作：
 - 1. Fork project.
   Fork 项目。
 - 2. Create branch:
   创建分支：
 ```bash
 git checkout -b feature-name
```
- 3. Submit changes:
  提交更改：
```bash
git commit -m "Explain changes"
```
- 4. Push branch:
  推送分支：
```bash
git push orgin feature-name
```
- 5. Submit Pull Request.
  提交拉取请求。

---
## 5. License 许可证

This project uses [MIT LICENSE](https://github.com/SomeB1oody/HashMaster/blob/main/LICENSE).
本项目使用[MIT LICENSE](https://github.com/SomeB1oody/HashMaster/blob/main/LICENSE)

---
## 6. Contact info 联系方式

- Email: stanyin64@gmail.com
- GitHub: [@SomeB1ooody](https://github.com/SomeB1oody)
