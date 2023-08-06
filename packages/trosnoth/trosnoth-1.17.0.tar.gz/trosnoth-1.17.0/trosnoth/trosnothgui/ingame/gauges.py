import logging
from dataclasses import dataclass

import pygame
from typing import Type, Tuple

from trosnoth.gui.framework import framework
from trosnoth.gui.framework.declarative import Colour, Rectangle
from trosnoth.model.player import Player
from trosnoth.trosnothgui.common import setAlpha
from trosnoth.model.upgrades import Upgrade

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class GaugeAppearance:
    size: Tuple[float, float]
    ratio: float
    foreground: Colour
    background: Colour = (255, 255, 255, 0)
    border_width: float = 2

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        ratio = min(1., max(0., self.ratio))
        width, height = self.size

        if len(self.background) < 4 or self.background[-1] != 0:
            frame.add(Rectangle(
                width, height,
                self.background,
            ))

        if ratio > 0:
            foreground_width = width * ratio
            frame.add(
                Rectangle(
                    max(0, foreground_width - self.border_width),
                    max(0, height - self.border_width),
                    self.foreground,
                ),
                at=((foreground_width + self.border_width - width) / 2, 0),
            )

        # Add frame
        frame.add(Rectangle(
            width, height,
            colour=(255, 255, 255, 0),
            border=colours.gaugeBorder, border_width=self.border_width,
        ))


class GaugeBase(framework.Element):
    def __init__(self, app, area, draw_panel=False):
        super(GaugeBase, self).__init__(app)
        self.area = area
        self.draw_panel = draw_panel

        self.icon = self.getIcon()
        if self.icon is not None:
            self.icon = self.icon.copy()
            setAlpha(self.icon, 160)

    def is_showing(self):
        return True

    def draw(self, surface):
        if not self.is_showing():
            return

        colours = self.app.theme.colours
        rect = self.area.getRect(self.app)
        pos = rect.topleft
        ratio = min(1, max(0, self.getRatio()))
        amount = int(ratio * rect.width)

        if self.draw_panel:
            panel_offset = 15
            panel_rect = pygame.Rect(rect)
            panel_rect.width += 3 * panel_offset
            panel_rect.left -= 2 * panel_offset
            panel_rect.height += 2 * panel_offset
            panel_rect.top -= panel_offset

            surface.fill(colours.gauge_panel, panel_rect)
            pygame.draw.rect(surface, colours.gaugeBorder, panel_rect, 2)

        backColour = self.getBackColour()
        if backColour is not None:
            backRect = pygame.rect.Rect(
                pos[0] + amount, pos[1], rect.width - amount + 1, rect.height)
            surface.fill(backColour, backRect)

        if amount > 0:
            insideRect = pygame.rect.Rect(pos, (amount, rect.height))
            surface.fill(self.getForeColour(), insideRect)

        # Draw the border on top
        pygame.draw.rect(surface, colours.gaugeBorder, rect, 2)

        if self.icon is not None:
            r = self.icon.get_rect()
            r.center = rect.midleft
            r.left -= r.width // 5
            surface.blit(self.icon, r)

    def getRatio(self):
        '''
        Return a number as a proportion (0..1) of how complete
        this box is. To be implemented in subclasses
        '''
        raise NotImplementedError

    def getForeColour(self):
        '''
        Return the foreground colour that this gauge should be.
        To be implemented in subclasses
        '''
        raise NotImplementedError

    def getBackColour(self):
        '''
        Return the background colour that this gauge should be.
        None = blank
        To be implemented in subclasses
        '''
        return None

    def getIcon(self):
        return None


class RespawnGauge(GaugeBase):
    '''Represents a graphical gauge to show how close to respawning a player
    is.'''
    def __init__(self, app, area, player, world, *args, **kwargs):
        self.player = player
        self.world = world
        super().__init__(app, area, *args, **kwargs)

    def is_showing(self):
        return self.player and self.player.dead

    def getRatio(self):
        return 1 - (self.player.timeTillRespawn / self.player.total_respawn_time)

    def getForeColour(self):
        if self.getRatio() >= 1:
            return self.app.theme.colours.gaugeGood
        else:
            return self.app.theme.colours.gaugeBad

    def getIcon(self):
        if self.player is None:
            return None
        return self.app.theme.sprites.ghostIcon(self.player.team).getImage()


class GunGauge(GaugeBase):
    player = None

    def is_showing(self):
        return self.player and not self.player.dead

    def getRatio(self):
        player = self.player
        if player is None:
            return 0

        override = player.current_gun.get_reload_ratio_and_colour(self.app.theme.colours)
        if override is not None:
            ratio, colour = override
            return ratio

        if player.guns.reload_time > 0:
            return 1 - player.guns.reload_time / player.guns.reload_from

        return 1

    def getForeColour(self):
        player = self.player
        override = player.current_gun.get_reload_ratio_and_colour(self.app.theme.colours)
        if override is not None:
            ratio, colour = override
            return colour
        if player is None or player.guns.reload_time > 0:
            return self.app.theme.colours.gaugeBad
        return self.app.theme.colours.gaugeGood

    def getIcon(self):
        return self.app.theme.sprites.gunIcon.getImage()


class SingleUpgradeGauge(GaugeBase):
    '''Represents a graphical gauge to show how much time a player has left
    to use their upgrade.'''

    def __init__(self, app, area, item, *args, **kwargs):
        self.item = item
        super().__init__(app, area, *args, **kwargs)

    def getRatio(self):
        item = self.item
        if item.totalTimeLimit == 0:
            return 1
        return item.timeRemaining / item.totalTimeLimit

    def getForeColour(self):
        return self.app.theme.colours.gaugeGood

    def getIcon(self):
        return type(self.item).get_icon(self.app.theme.sprites)


class SingleTeamBoostGauge(GaugeBase):
    def __init__(self, app, area, boost, *args, **kwargs):
        self.boost = boost
        super().__init__(app, area, *args, **kwargs)

    def getRatio(self):
        if self.boost.time_limit == 0:
            return 1
        return self.boost.time_remaining / self.boost.time_limit

    def getForeColour(self):
        return self.app.theme.colours.gaugeGood

    def getIcon(self):
        return type(self.boost).get_icon(self.app.theme.sprites)


class SingleAmmoGauge(GaugeBase):
    '''
    Represents a graphical gauge to show how much ammo a player has
    remaining for a particular gun.
    '''

    def __init__(self, app, area, gun, *args, **kwargs):
        self.gun = gun
        super().__init__(app, area, *args, **kwargs)

    def getRatio(self):
        if self.gun.max_ammo == 0:
            return 1
        return self.gun.ammo / self.gun.max_ammo

    def getForeColour(self):
        return self.app.theme.colours.gauge_ammo

    def getIcon(self):
        return self.gun.get_icon(self.app.theme.sprites)


@dataclass(frozen=True)
class ItemCostGauge:
    player: Player
    upgrade: Type[Upgrade]
    size: Tuple[float, float]
    border_width: float = 1

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if not self.upgrade.enabled:
            ratio = 1
            colour = frame.app.theme.colours.gaugeBad
        elif self.upgrade.requiredCoins == 0:
            ratio = 1
            colour = frame.app.theme.colours.gaugeGood
        else:
            ratio = self.player.coins / self.upgrade.requiredCoins
            if ratio < 1:
                colour = frame.app.theme.colours.gaugeBad
            else:
                colour = frame.app.theme.colours.gaugeGood

        frame.add(GaugeAppearance(
            ratio=ratio, foreground=colour, size=self.size, border_width=self.border_width))
