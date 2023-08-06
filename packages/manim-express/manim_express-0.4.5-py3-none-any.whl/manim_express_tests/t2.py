import sys
from pathlib import Path

sys.path.append('..')
# sys.path.append(str(Path.cwd().parent))
# sys.path.append(str(Path.cwd().parents[1]))
# sys.path.append(str(Path.cwd().joinpath('manim_express')))

from manim_express import *
from manimlib import *



class Timer(VGroup):
    CONFIG = {
        "radius": 1,
        "frame_color": WHITE,
        "frame_width": 5,
        "sweep_angle": TAU,
        "sweep_color": TEAL_D,
        "sweep_opacity": 1,
        "pillar_radius_factor": 0.1,
        "hand_length_factor": 0.7,
        "hand_color": RED,
    }

    def __init__(self, **kwargs):
        self.kw = kwargs
        VGroup.__init__(self, **kwargs)
        timer_frame = Circle(radius=1).set_stroke(width=self.frame_width, color=self.frame_color)
        sweep_area = Sector(outer_radius=1, start_angle=PI / 2, angle=-self.sweep_angle)
        sweep_area.set_fill(color=self.sweep_color, opacity=self.sweep_opacity)
        theta = np.arcsin(self.pillar_radius_factor / self.hand_length_factor)
        hand = Polygon(
            ORIGIN,
            (np.cos(theta) * RIGHT + np.sin(theta) * UP) * self.pillar_radius_factor,
            self.hand_length_factor * UP,
            (np.cos(theta) * LEFT + np.sin(theta) * UP) * self.pillar_radius_factor
        )
        hand.rotate_about_origin(-self.sweep_angle)
        hand.set_stroke(width=0).set_fill(color=self.hand_color, opacity=1)
        pillar = Circle(radius=self.pillar_radius_factor)
        pillar.set_stroke(width=0).set_fill(color=self.hand_color, opacity=1)
        # Add a big transparent circle to fix its center while animating.
        transparent_circle = Circle(radius=1.2).set_stroke(width=0)
        self.add(transparent_circle, sweep_area, timer_frame, hand, pillar)
        self.scale(self.radius)


class Countdown(UpdateFromAlphaFunc):
    def __init__(self, timer, **kwargs):
        def update_timer(timer_mob, alpha):
            new_timer_mob = Timer(sweep_angle=(1 - alpha) * TAU, **timer_mob.kw)
            new_timer_mob.move_to(timer_mob)
            timer_mob.become(new_timer_mob)
            return timer_mob

        UpdateFromAlphaFunc.__init__(self, timer, update_timer, rate_func=linear, **kwargs)


def countdown_timer(scene_ctx, run_time=5):
    """
    Usage:
    countdown_timer(self)
    """
    timer = Timer().to_corner(DR)
    scene_ctx.play(FadeIn(timer))
    scene_ctx.play(Countdown(timer, run_time=run_time))
    scene_ctx.play(FadeOut(timer))
    scene_ctx.wait()


class Button(VGroup):
    CONFIG = {
        "fill_color": WHITE,
        "fill_opacity": 0.5
    }

    def __init__(self, **kwargs):
        annulus = Annulus(inner_radius=0.8, outer_radius=1)
        symbol = self.get_symbol()
        VGroup.__init__(self, annulus, symbol, **kwargs)
        self.set_fill(color=self.fill_color, opacity=self.fill_opacity)

    def get_symbol(self):
        return VMobject()


class PlayButton(Button):
    def get_symbol(self):
        return Triangle(start_angle=0).set_stroke(width=0).shift(0.1 * LEFT).round_corners(0.1).scale(0.6)


class PauseButton(Button):
    def get_symbol(self):
        component_left = RoundedRectangle(width=0.2, height=0.9, corner_radius=0.1).set_stroke(width=0)
        component_right = component_left.copy()
        return VGroup(
            component_left.shift(0.3 * LEFT),
            component_right.shift(0.3 * RIGHT)
        )


def pause_video(scene_ctx, pause_duration=2):
    pause_button = PauseButton().to_corner(DR)
    play_button = PlayButton().to_corner(DR)
    scene_ctx.add(pause_button)
    scene_ctx.wait(pause_duration)
    scene_ctx.remove(pause_button)
    scene_ctx.add(play_button)
    scene_ctx.play(FadeOut(play_button))

scene = EagerModeScene()

scene.play(ShowCreation(Triangle()))
pause_video(scene)
scene.play(ShowCreation(Square()))
scene.hold_on()

