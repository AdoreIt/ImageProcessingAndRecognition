class ThresholdSelector(object):
    def __init__(self, subplot):
        self.subplot = subplot
        self.select_line = subplot.axvline(
            color='lightskyblue', label="Threshold selector")  # the vert line

        # text location in axes coords
        self.txt = subplot.text(0.95, 0.9, '', transform=subplot.transAxes, color="steelblue")

    def mouse_move(self, event):
        if not event.inaxes:
            return
        x = int(event.xdata)
        self.select_line.set_xdata(x)
        self.txt.set_text('{}'.format(x))
        self.subplot.figure.canvas.draw()
