class ThresholdSelector(object):
    def __init__(self, ax):
        self.ax = ax
        self.select_line = ax.axvline(
            color='lightskyblue',  label="Threshold selector")  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.95, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return
        x = int(event.xdata)
        self.select_line.set_xdata(x)
        self.txt.set_text('{}'.format(x))
        self.ax.figure.canvas.draw()
