"""
Nice Picture - A Beautiful Mathematical Visualization
Created with ManimGL

To render this scene, run:
    manimgl nice_picture.py NicePicture -s

To render as video:
    manimgl nice_picture.py NicePicture -o
"""

from manimlib import *
import numpy as np


class NicePicture(Scene):
    """
    A beautiful mathematical visualization featuring:
    - Spiraling golden ratio curves
    - Harmonious color gradients
    - Elegant geometric patterns
    """

    def construct(self):
        # Create a dark gradient background effect with circles
        background_circles = VGroup()
        for i in range(20, 0, -1):
            circle = Circle(radius=i * 0.4)
            # Create a gradient from deep purple to dark blue
            t = i / 20
            color = interpolate_color(
                "#1a0533",  # Deep purple
                "#0a1628",  # Dark blue
                t
            )
            circle.set_fill(color, opacity=0.3)
            circle.set_stroke(width=0)
            background_circles.add(circle)

        self.add(background_circles)

        # Create the main golden spiral
        golden_ratio = (1 + np.sqrt(5)) / 2

        def golden_spiral(t):
            # Logarithmic spiral with golden ratio
            a = 0.1
            b = np.log(golden_ratio) / (PI / 2)
            r = a * np.exp(b * t)
            return np.array([
                r * np.cos(t),
                r * np.sin(t),
                0
            ])

        # Create multiple spirals with different rotations
        spirals = VGroup()
        colors = [BLUE_C, TEAL_C, GREEN_C, YELLOW_C, GOLD_C, RED_C, MAROON_C, PURPLE_C]

        for i in range(8):
            spiral = ParametricCurve(
                golden_spiral,
                t_range=[0, 6 * PI],
                stroke_width=3,
            )
            spiral.rotate(i * TAU / 8)
            spiral.set_stroke(
                color=colors[i % len(colors)],
                width=2 + i * 0.3,
                opacity=0.8
            )
            spirals.add(spiral)

        # Add glow effect by duplicating with lower opacity and larger width
        glow_spirals = spirals.copy()
        for spiral in glow_spirals:
            spiral.set_stroke(width=8, opacity=0.2)

        self.add(glow_spirals)
        self.add(spirals)

        # Create concentric hexagons
        hexagons = VGroup()
        for i in range(12):
            radius = 0.5 + i * 0.35
            hex_shape = RegularPolygon(n=6)
            hex_shape.scale(radius)
            hex_shape.rotate(i * PI / 12)

            # Color gradient from center outward
            t = i / 12
            color = interpolate_color(YELLOW_C, PURPLE_C, t)
            hex_shape.set_stroke(color, width=1.5, opacity=0.6 - i * 0.03)
            hex_shape.set_fill(opacity=0)
            hexagons.add(hex_shape)

        self.add(hexagons)

        # Add floating dots in a Fibonacci pattern
        dots = VGroup()
        phi = golden_ratio
        for n in range(150):
            # Fibonacci/Golden angle distribution
            theta = n * 2 * PI / (phi * phi)
            r = 0.15 * np.sqrt(n)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

            if abs(x) < 7 and abs(y) < 4:  # Keep within frame
                dot = Dot(point=[x, y, 0], radius=0.02 + 0.002 * np.sqrt(n))

                # Color based on angle
                hue = (theta % TAU) / TAU
                color = interpolate_color(
                    interpolate_color(BLUE_A, TEAL_A, hue),
                    interpolate_color(YELLOW_A, PINK, hue),
                    n / 150
                )
                dot.set_fill(color, opacity=0.9)
                dot.set_stroke(WHITE, width=0.5, opacity=0.3)
                dots.add(dot)

        self.add(dots)

        # Add elegant curves - Lissajous figures
        lissajous_curves = VGroup()
        for k in range(3):
            def make_lissajous(a, b, delta, scale):
                def curve(t):
                    return np.array([
                        scale * np.sin(a * t + delta),
                        scale * np.sin(b * t),
                        0
                    ])
                return curve

            a_vals = [3, 5, 7]
            b_vals = [4, 6, 8]

            curve = ParametricCurve(
                make_lissajous(a_vals[k], b_vals[k], PI/4, 2.5 - k * 0.3),
                t_range=[0, TAU],
                stroke_width=2,
            )
            color = interpolate_color(BLUE_B, PURPLE_B, k / 3)
            curve.set_stroke(color, opacity=0.4)
            lissajous_curves.add(curve)

        self.add(lissajous_curves)

        # Add a central mandala-like pattern
        mandala = VGroup()
        for i in range(12):
            petal = VMobject()
            # Create a petal shape using bezier curves
            petal.set_points_smoothly([
                ORIGIN,
                0.8 * UP + 0.3 * RIGHT,
                1.5 * UP,
                0.8 * UP + 0.3 * LEFT,
                ORIGIN
            ])
            petal.rotate(i * TAU / 12, about_point=ORIGIN)

            # Gradient coloring
            t = i / 12
            color = interpolate_color(GOLD_A, MAROON_A, t)
            petal.set_stroke(color, width=2, opacity=0.7)
            petal.set_fill(color, opacity=0.15)
            mandala.add(petal)

        # Add inner details to mandala
        for i in range(24):
            small_petal = VMobject()
            small_petal.set_points_smoothly([
                ORIGIN,
                0.3 * UP + 0.1 * RIGHT,
                0.6 * UP,
                0.3 * UP + 0.1 * LEFT,
                ORIGIN
            ])
            small_petal.rotate(i * TAU / 24, about_point=ORIGIN)
            t = i / 24
            color = interpolate_color(TEAL_A, BLUE_A, t)
            small_petal.set_stroke(color, width=1.5, opacity=0.8)
            small_petal.set_fill(color, opacity=0.2)
            mandala.add(small_petal)

        # Center dot
        center = Dot(radius=0.15)
        center.set_fill(WHITE, opacity=0.9)
        center.set_stroke(GOLD, width=2)
        mandala.add(center)

        self.add(mandala)

        # Add title text with elegant styling
        title = Text(
            "Entropy Audit Tool",
            font="Consolas",
            font_size=48,
        )
        title.set_fill(WHITE, opacity=0.9)
        title.set_stroke(BLUE_E, width=1, opacity=0.5)
        title.to_edge(UP, buff=0.5)

        # Add subtitle
        subtitle = Text(
            "Mathematical Harmony",
            font="Consolas",
            font_size=24,
        )
        subtitle.set_fill(GREY_A, opacity=0.8)
        subtitle.next_to(title, DOWN, buff=0.2)

        self.add(title)
        self.add(subtitle)

        # Final wait for static image
        self.wait()


class AnimatedNicePicture(Scene):
    """
    An animated version of the nice picture with flowing movements.
    """

    def construct(self):
        # Background
        background = FullScreenRectangle()
        background.set_fill("#0a0a1a", opacity=1)
        self.add(background)

        # Create flowing curves
        curves = VGroup()
        for i in range(20):
            def make_wave(offset, amplitude, frequency):
                def wave(t):
                    return np.array([
                        t - 7,
                        amplitude * np.sin(frequency * t + offset),
                        0
                    ])
                return wave

            curve = ParametricCurve(
                make_wave(i * 0.5, 0.3 + 0.1 * np.sin(i), 1 + i * 0.1),
                t_range=[0, 14],
                stroke_width=2,
            )
            color = interpolate_color(BLUE_C, PURPLE_C, i / 20)
            curve.set_stroke(color, opacity=0.6)
            curve.shift((i - 10) * 0.3 * UP)
            curves.add(curve)

        self.play(
            *[ShowCreation(curve, run_time=3) for curve in curves],
            lag_ratio=0.1
        )

        # Add central element
        central = VGroup()
        for i in range(8):
            arc = Arc(
                radius=1.5,
                start_angle=i * TAU / 8,
                angle=TAU / 8 - 0.1,
                stroke_width=4
            )
            color = [BLUE, TEAL, GREEN, YELLOW, GOLD, RED, MAROON, PURPLE][i]
            arc.set_stroke(color, opacity=0.8)
            central.add(arc)

        self.play(
            *[ShowCreation(arc) for arc in central],
            run_time=2
        )

        # Rotate the central element
        self.play(
            Rotate(central, TAU / 4, run_time=3)
        )

        self.wait(2)


if __name__ == "__main__":
    # This allows running the scene directly
    import os
    os.system("manimgl nice_picture.py NicePicture -s")
