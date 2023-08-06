import wx
from wx.lib.filebrowsebutton import FileBrowseButton
from typing import Dict
import os

class Submit(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(Submit, self).__init__(*args, **kwargs)


        self.submission_template = ""
        self.submission_cmd = ""
        self.submission_textfield : wx.TextCtrl = None
        self.filebrower: FileBrowseButton = None
        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(4, 1, 4, 4)

        #btn1 = wx.Button(panel, label='Info')
        #btn2 = wx.Button(panel, label='Error')

        row_submission_cmnd = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(panel, label=" Submission command: ")
        try:
            default_submission_cmd = os.environ['CRYOLO_SUBMIT_CMD']
        except:
            default_submission_cmd = 'sbatch'

        self.submission_textfield = wx.TextCtrl(panel, value=default_submission_cmd)
        row_submission_cmnd.Add(lbl, 0, flag = wx.EXPAND)
        row_submission_cmnd.Add(self.submission_textfield, 1, flag = wx.ALIGN_LEFT | wx.EXPAND)

        try:
            default_submission_script = os.environ['CRYOLO_SUBMIT_SCRIPT']
        except:
            default_submission_script = ''
        self.filebrower = FileBrowseButton(panel, labelText="Submission template:", initialValue=default_submission_script)  # wx.Button(panel, label='Alert')

        row_ok_cancel = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, label='OK')
        btn_cancel = wx.Button(panel, label='Cancel')
        row_ok_cancel.Add(btn_cancel)
        row_ok_cancel.Add(btn_ok)

        sizer.Add(self.filebrower, flag = wx.ALIGN_LEFT | wx.EXPAND)
        sizer.Add(row_submission_cmnd, flag = wx.ALIGN_LEFT | wx.EXPAND)
        sizer.AddStretchSpacer(1)
        sizer.Add(row_ok_cancel,1 , flag = wx.ALIGN_RIGHT)
        ### XXX_SXCMD_LINE_XXX
        hbox.Add(sizer, 1, wx.ALL, 15)
        panel.SetSizer(hbox)

        #btn1.Bind(wx.EVT_BUTTON, self.ShowMessage1)
        #btn2.Bind(wx.EVT_BUTTON, self.ShowMessage2)
        btn_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        btn_ok.Bind(wx.EVT_BUTTON, self.onOKPressed)

        self.SetSize((400, 200))
        self.SetTitle('Submit to queue')
        self.Centre()
        self.cancled = False

        #self.SetSize((500, 200))
        #self.SetTitle('Messages')
        #self.Centre()


    def onCancel(self, event):
        self.cancled=True
        self.Close()

    def onOKPressed(self, event):
        self.submission_cmd = self.submission_textfield.GetValue()
        self.submission_template = self.filebrower.GetValue()
        self.Close()
        '''
        dial = wx.MessageDialog(None, 'Unallowed operation', 'Exclamation',
            wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()
        '''
    def generate_submission_script(self,path_template : str, replacement_dict : Dict):
        import os
        filename = os.path.basename(path_template)
        filename = os.path.splitext(filename)[0]
        new_script=filename+"_job.sh"

        with open(path_template, "rt") as fin:
            with open(new_script, "wt") as fout:
                content = fin.read()
                for key, value in replacement_dict.items():
                    content = content.replace(key, value)
                fout.write(content)

        return new_script

