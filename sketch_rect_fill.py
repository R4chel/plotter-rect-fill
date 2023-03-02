import vsketch
from shapely.geometry import Point

class RectFillSketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    step_count = vsketch.Param(20.)
    # radius = vsketch.Param(1.0, decimals=3, unit="in")

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}", landscape=self.landscape, center=False)
        self.width = self.width - 2 * self.margin
        self.height = self.height - 2 * self.margin
        vsk.translate(self.margin, self.margin)
        vsk.penWidth(f"{self.pen_width}")

        
        layers = [1 + i for i in range(self.num_layers)]

        step_size = max(self.width, self.height) / self.step_count
        x0, y0 = step_size, step_size
        x1 = self.width - step_size
        y1 = self.height - step_size
        while x0 <= x1 and y0 <= y1:
            layer = layers[int(vsk.random(0, len(layers)))]
            vsk.stroke(layer)
            match vsk.random(0,1):
                case rnd if 0 <= rnd < 0.25:
                    vsk.line(x0, y0, x0, y1)
                    x0 += step_size
                case rnd if 0.25 <= rnd < 0.5:
                    vsk.line(x1, y0, x1, y1)
                    x1 -= step_size
                case rnd if 0.5 <= rnd < 0.75:
                    vsk.line(x0, y0, x1, y0)
                    y0 += step_size
                case rnd if 0.75 <= rnd < 1:
                    vsk.line(x0, y1, x1, y1)
                    y1 -= step_size


        # implement your sketch here
        # vsk.fill(layer)
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    RectFillSketch.display()
