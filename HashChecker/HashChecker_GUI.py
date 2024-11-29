import wx
import hashlib
import os

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
        return None, None, None

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

class HashCheckerWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(HashCheckerWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入哈希码
        self.vbox.Add(wx.StaticText(panel, label="Enter hash code:"), flag=wx.ALL, border=5)
        self.input_hash = wx.TextCtrl(panel)
        self.vbox.Add(self.input_hash, flag=wx.ALL, border=5)

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

        # 检查按钮
        self.check_button = wx.Button(panel, label="Check")
        self.check_button.Bind(wx.EVT_BUTTON, self.on_check_button)
        self.vbox.Add(self.check_button, flag=wx.ALL, border=5)

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

    def on_check_button(self, event):
        hash_value = self.input_hash.GetValue()

        if len(hash_value) == 64:
            hash_type = "sha256"
        elif len(hash_value) == 128:
            hash_type = "sha512"
        elif len(hash_value) == 32:
            hash_type = "md5"
        else:
            wx.MessageBox(
            "Invalid hash length. Hash must be either 64, 128, or 32 characters long.", "Error",
            wx.OK | wx.ICON_ERROR)
            return

        input_type = self.input_type.GetSelection()

        if input_type == 0:
            text = self.text_input.GetValue()
            if not text:
                wx.MessageBox("Please enter text.", "Error", wx.OK | wx.ICON_ERROR)
                return
            sha256_hash, sha512_hash, md5_hash = hash_string(text)
        elif input_type == 1:
            if not self.selected_file:
                wx.MessageBox("Please select a file.", "Error", wx.OK | wx.ICON_ERROR)
                return
            sha256_hash, sha512_hash, md5_hash = hash_file(self.selected_file)
        else:
            if not self.selected_folder:
                wx.MessageBox("Please select a folder.", "Error", wx.OK | wx.ICON_ERROR)
                return
            sha256_hash, sha512_hash, md5_hash = hash_directory(self.selected_folder)

        if hash_type == "sha256":
            is_match = hash_value == sha256_hash
        elif hash_type == "sha512":
            is_match = hash_value == sha512_hash
        elif hash_type == "md5":
            is_match = hash_value == md5_hash
        else:
            is_match = False

        if is_match:
            wx.MessageBox("Hash matches.", "Congratulation", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Hash does not match.", "Sorry", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    frame = HashCheckerWX(None)
    frame.SetTitle('Hash Checker with GUI')
    frame.SetSize((300, 300))
    frame.Show()
    app.MainLoop()
