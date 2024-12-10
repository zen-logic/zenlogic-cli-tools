import wx, wx.grid


class InfoGrid(wx.grid.Grid):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.label_width = 100
        self.attr = wx.grid.GridCellAttr()
        self.EnableEditing(False)
        self.HideRowLabels()
        self.HideColLabels()
        self.SetCellHighlightPenWidth(0)
        self.SetCellHighlightROPenWidth(0)
        self.CreateGrid(0, 2)
        self.SetSelectionMode(wx.grid.Grid.GridSelectNone)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)
        self.Bind(wx.EVT_SIZE, self.on_resize)

        
    def set_item(self, label, value):
        # update item if it already exists
        for idx in range(self.GetNumberRows()):
            if self.GetCellValue(idx, 0) == label:
                self.SetCellValue(idx, 0, label)
                self.SetCellValue(idx, 1, str(value))
                return
        # create new item if it doesn't
        row_id = self.GetNumberRows()
        self.AppendRows()
        self.SetRowAttr(row_id, self.attr)
        self.attr.IncRef()
        self.SetCellValue(row_id, 0, label)
        self.SetCellValue(row_id, 1, str(value))


    def remove_item(self, label):
        for idx in range(0, self.GetNumberRows()):
            if self.GetCellValue(idx, 0) == label:
                self.DeleteRows(idx, 1)
                break
        

    def on_resize(self, event):
        w, h = self.GetSize()
        if h > 0 and w > 0:
            self.SetColSize(0, self.label_width)
            col_w = w - self.label_width
            if col_w < 0:
                col_w = -1
            self.SetColSize(1, col_w)
        event.Skip()
