from adafruit_ssd1306 import SSD1306_I2C
from busio import I2C
from math import ceil


class ssd1306:
    def __init__(self):
        # internal use only
        self._display = None

        # public
        self.connected = False
        self.hw_name = "ssd1306"
        self.interface_type = "display"
        self.display_size = [128, 64]

    def setup(self, scl, sda, x=None, y=None):
        # Initialises the display, defaults to 128x64 resolution if x&y unset
        
        if x is not None:
            self.display_size[0] = x
        if y is not None:
            self.display_size[1] = y
        del x, y
        if not self.connected:
            self._display = SSD1306_I2C(
                self.display_size[0], self.display_size[1], I2C(scl, sda)
            )
            self.connected = True
        else:
            raise NotImplementedError
        del scl, sda

    def reset(self):
        raise NotImplementedError

    def _fetch_points(self, xs, ys, xe, ye, expand=False):
        # Draws a virtual line and returns the set of points
        
        pointarr = []
        dx, dy = abs(xs - xe), abs(ys - ye)
        cx, cy = xs, ys
        sx = -1 if xs > xe else 1
        sy = -1 if ys > ye else 1
        if dx > dy:
            err = dx / 2.0
            while cx != xe:
                pointarr.append([int(cx), int(cy)])
                if expand:
                    pointarr.append([ceil(cx), ceil(cy)])
                err -= dy
                if err < 0:
                    cy += sy
                    err += dx
                cx += sx
            del err
        else:
            err = dy / 2.0
            while cy != ye:
                pointarr.append([int(cx), int(cy)])
                if expand:
                    pointarr.append([ceil(cx), ceil(cy)])
                err -= dx
                if err < 0:
                    cx += sx
                    err += dy
                cy += sy
            del err
            pointarr.append([int(cx), int(cy)])
        del dx, dy, cx, cy, sx, sy, expand
        return pointarr

    def line(self, xs, ys, xe, ye, col=1, sync=True, expand=False):
        """
            Draw a line between [xs, ys] and [xe, ye]
            "expand" keyword makes the line fill both pixels in case of float
        """
        dx, dy = abs(xs - xe), abs(ys - ye)
        cx, cy = xs, ys
        sx = -1 if xs > xe else 1
        sy = -1 if ys > ye else 1
        if dx > dy:
            err = dx / 2.0
            while cx != xe:
                self._display.pixel(int(cx), int(cy), col)
                if expand:
                    self._display.pixel(ceil(cx), ceil(cy), col)
                err -= dy
                if err < 0:
                    cy += sy
                    err += dx
                cx += sx
            del err
        else:
            err = dy / 2.0
            while cy != ye:
                self._display.pixel(int(cx), int(cy), col)
                if expand:
                    self._display.pixel(ceil(cx), ceil(cy), col)
                err -= dx
                if err < 0:
                    cx += sx
                    err += dy
                cy += sy
            del err
            self._display.pixel(int(cx), int(cy), col)
        if sync:
            self.frame()
        del dx, dy, cx, cy, sx, sy, sync, expand

    def frame(self):
        # Refresh display
        
        self._display.show()

    def circle(self, xc, yc, r, col=1, fill=False, sync=True):
        """
            Draw a circle with the center [xc, yc] and radius r
        """
        f = 1 - r
        ddf_x = 1
        ddf_y = -2 * r
        x = 0
        y = r

        points = [[xc, yc + r], [xc, yc + r], [xc, yc - r], [xc + r, yc], [xc - r, yc]]

        for point in points:
            self._display.pixel(point[0], point[1], col)
            del point

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            for point in [
                [xc + x, yc + y],
                [xc - x, yc + y],
                [xc + x, yc - y],
                [xc - x, yc - y],
                [xc + y, yc + x],
                [xc - y, yc + x],
                [xc + y, yc - x],
                [xc - y, yc - x],
            ]:
                points.append(point)
                self._display.pixel(point[0], point[1], col)
                del point

        if fill:
            for point in points:
                self.line(xc, yc, point[0], point[1], col, sync=False, expand=True)
                del point

        if sync:
            self.frame()
        del xc, yc, r, col, fill, sync, f, ddf_x, ddf_y, x, y, points

    def pixel(self, x, y, col=1, sync=True):
        # Draw a single pixel on [x, y]
        
        self._display.pixel(x, y, col)
        if sync:
            self.frame()
        del x, y, col, sync

    def triangle(self, x1, y1, x2, y2, x3, y3, col=1, fill=False, sync=True):
        # Draw a triangle between points [x1, y1], [x2, y2], [x3, y3]
        
        self.line(x1, y1, x2, y2, col, sync=False)
        self.line(x1, y1, x3, y3, col, sync=False)
        self.line(x2, y2, x3, y3, col, sync=False)
        
        if fill:
            vl = self._fetch_points(x1, y1, x2, y2)  # virtual line
            for point in vl:
                self.line(x3, y3, point[0], point[1], col, sync=False, expand=True)
                del point
            del vl
        
        if sync:
            self.frame()
        del x1, y1, x2, y2, x3, y3, col, fill, sync

    def fill(self, col=1, sync=True):
        # fill the whole display
        
        self._display.fill(col)
        
        if sync:
            self.frame()
        
        del sync, col

    def text(self, x, y, text, col=1, sync=True):
        # Write some text, starting from point [x, y]
        
        self._display.text(text, x, y, col, font_name="/LjinuxRoot/etc/font5x8.bin")
        if sync:
            self.frame()
        del x, y, text, col, sync

    def enter(self, args=None):
        print("This kernel module provides no cli interface.\nPlease use farland to interface with it instead.")
