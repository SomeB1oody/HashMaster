import wx
import hashlib
import pyperclip
import os

def split_string_in_half(s):
    length = len(s)
    mid = length // 2

    if length % 2 == 0:
        # 如果长度是偶数
        return s[:mid], s[mid:]
    else:
        # 如果长度是奇数，将前半部分比后半部分多一个字符
        return s[:mid + 1], s[mid + 1:]

def hash_string(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    sha512_hash = hashlib.sha512(text.encode()).hexdigest()
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    return sha256_hash, sha512_hash, md5_hash

def hash_file(file_path):
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    md5 = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
                sha512.update(chunk)
                md5.update(chunk)
    except FileNotFoundError:
        raise FileNotFoundError

    return sha256.hexdigest(), sha512.hexdigest(), md5.hexdigest()

def hash_directory(directory_path):
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    md5 = hashlib.md5()

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
                        sha512.update(chunk)
                        md5.update(chunk)
            except FileNotFoundError:
                continue

    return sha256.hexdigest(), sha512.hexdigest(), md5.hexdigest()

class ValidationCodeGeneratorWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(ValidationCodeGeneratorWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.input_type = wx.RadioBox(
            panel, label="Choose a input type", choices=[
                'Text', 'File', 'Folder'
            ]
        )
        self.input_type.Bind(wx.EVT_RADIOBOX, self.on_input_type)
        self.vbox.Add(self.input_type, flag=wx.ALL, border=5)

        # 文字输入
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.input_text = wx.StaticText(panel, label="Text input:")
        self.hbox.Add(self.input_text, flag=wx.ALL, border=5)
        self.text_input = wx.TextCtrl(panel)
        self.hbox.Add(self.text_input, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox, flag=wx.EXPAND)

        # 文件夹和文件选择
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_button = wx.Button(panel, label="Select file")
        self.file_button.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.on_select_file, self.file_button)
        self.hbox2.Add(self.file_button, flag=wx.ALL, border=5)
        self.folder_button = wx.Button(panel, label="Select folder")
        self.folder_button.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.on_select_folder, self.folder_button)
        self.hbox2.Add(self.folder_button, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox2, flag=wx.EXPAND)
        self.path_text = wx.StaticText(panel, label="Click \"Select file\" or \"Select folder\" first")
        self.vbox.Add(self.path_text, flag=wx.ALL, border=5)

        # 生成按钮
        self.generate_button = wx.Button(panel, label="Generate")
        self.vbox.Add(self.generate_button, flag=wx.ALL, border=5)
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

        # 生成的值与复制操作
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_sha256 = wx.Button(panel, label="Copy SHA256")
        self.copy_sha256.Bind(wx.EVT_BUTTON, self.on_copy_sha256)
        self.hbox3.Add(self.copy_sha256, flag=wx.ALL, border=5)
        self.copy_sha256.Enable(False)
        self.sha256_text = wx.StaticText(panel, label="SHA256: ")
        self.hbox3.Add(self.sha256_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox3, flag=wx.EXPAND)
        self.sha256_2nd_line = wx.StaticText(panel, label="")
        self.vbox.Add(self.sha256_2nd_line, flag=wx.ALL, border=5)

        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_sha512 = wx.Button(panel, label="Copy SHA512")
        self.copy_sha512.Bind(wx.EVT_BUTTON, self.on_copy_sha512)
        self.hbox4.Add(self.copy_sha512, flag=wx.ALL, border=5)
        self.copy_sha512.Enable(False)
        self.sha512_text = wx.StaticText(panel, label="SHA512: ")
        self.hbox4.Add(self.sha512_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox4, flag=wx.EXPAND)
        self.sha512_2nd_line = wx.StaticText(panel, label="")
        self.vbox.Add(self.sha512_2nd_line, flag=wx.ALL, border=5)
        self.sha512_3rd_line = wx.StaticText(panel, label="")
        self.vbox.Add(self.sha512_3rd_line, flag=wx.ALL, border=5)
        self.sha512_4th_line = wx.StaticText(panel, label="")
        self.vbox.Add(self.sha512_4th_line, flag=wx.ALL, border=5)

        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_md5 = wx.Button(panel, label="Copy MD5")
        self.copy_md5.Bind(wx.EVT_BUTTON, self.on_copy_md5)
        self.hbox5.Add(self.copy_md5, flag=wx.ALL, border=5)
        self.copy_md5.Enable(False)
        self.md5_text = wx.StaticText(panel, label="MD5: ")
        self.hbox5.Add(self.md5_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox5, flag=wx.EXPAND)

        # 设置面板的布局管理器
        panel.SetSizer(self.vbox)
        panel.Layout()

    def on_input_type(self, event):
        choice = self.input_type.GetSelection()
        if choice == 0:
            self.file_button.Enable(False)
            self.folder_button.Enable(False)
            self.text_input.Enable(True)
        elif choice == 1:
            self.file_button.Enable(True)
            self.folder_button.Enable(False)
            self.text_input.Enable(False)
        else:
            self.file_button.Enable(False)
            self.folder_button.Enable(True)
            self.text_input.Enable(False)

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a file", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_file = dialog.GetPath()

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_generate(self, event):
        choice = self.input_type.GetSelection()

        if choice == 0:
            text = self.text_input.GetValue()
            if not text:
                wx.MessageBox("Please enter text.", "Error", wx.OK | wx.ICON_ERROR)
                return
            self.sha256, self.sha512, self.md5 = hash_string(text)
        elif choice == 1:
            file_path = self.selected_file
            if not file_path:
                wx.MessageBox("Please select a file.", "Error", wx.OK | wx.ICON_ERROR)
                return
            try:
                self.sha256, self.sha512, self.md5 = hash_file(file_path)
            except FileNotFoundError:
                wx.MessageBox("File not found.", "Error", wx.OK | wx.ICON_ERROR)
                return
        else:
            directory_path = self.selected_folder
            if not directory_path:
                wx.MessageBox("Please select a folder.", "Error", wx.OK | wx.ICON_ERROR)
                return
            self.sha256, self.sha512, self.md5 = hash_directory(directory_path)

        self.copy_sha256.Enable(True)
        self.copy_sha512.Enable(True)
        self.copy_md5.Enable(True)

        sha256_1st_line, sha256_2nd_line = split_string_in_half(self.sha256)
        self.sha256_text.SetLabel(f"SHA256: {sha256_1st_line}")
        self.sha256_2nd_line.SetLabel(f"                                         {sha256_2nd_line}")

        sha512_ls1, sha512_ls2 = split_string_in_half(self.sha512)
        sha512_1st_line, sha512_2nd_line = split_string_in_half(sha512_ls1)
        sha512_3rd_line, sha512_4th_line = split_string_in_half(sha512_ls2)
        self.sha512_text.SetLabel(f"SHA512: {sha512_1st_line}")
        self.sha512_2nd_line.SetLabel(f"                                         {sha512_2nd_line}")
        self.sha512_3rd_line.SetLabel(f"                                         {sha512_3rd_line}")
        self.sha512_4th_line.SetLabel(f"                                         {sha512_4th_line}")

        self.md5_text.SetLabel(f"MD5: {self.md5}")

    def on_copy_sha256(self, event):
        pyperclip.copy(self.sha256)
        wx.MessageBox("SHA256 copied to clipboard.", "Success", wx.OK | wx.ICON_INFORMATION)

    def on_copy_sha512(self, event):
        pyperclip.copy(self.sha512)
        wx.MessageBox("SHA512 copied to clipboard.", "Success", wx.OK | wx.ICON_INFORMATION)

    def on_copy_md5(self, event):
        pyperclip.copy(self.md5)
        wx.MessageBox("MD5 copied to clipboard.", "Success", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = ValidationCodeGeneratorWX(None)
    frame.SetTitle('Hash Code Generator with GUI')
    frame.SetSize((425, 470))
    frame.Show()
    app.MainLoop()