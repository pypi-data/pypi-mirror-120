import functools
import logging
import random
from dataclasses import dataclass
from typing import Optional, Type, Callable

import pygame

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE,
    ACTION_SETTINGS_MENU, ACTION_QUIT_MENU,
    ACTION_REALLY_QUIT, ACTION_JOIN_GAME, ACTION_PAUSE_GAME, ACTION_MAIN_MENU,
    ACTION_TERMINAL_TOGGLE, ACTION_FOLLOW, ACTION_RADIAL_UPGRADE_MENU, ACTION_USE_UPGRADE,
    ACTION_RESPAWN,
    ACTION_READY, ACTION_CLEAR_UPGRADE, ACTION_CHAT,
    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE,
    MAX_EMOTE, ACTION_NEXT_WEAPON, ACTION_PREVIOUS_WEAPON, ACTION_BUY_AMMO, MOUSE_UP,
    ACTION_NEXT_TEAM_BOOST, KEY_UP, ACTION_CONTRIBUTE_TO_TEAM_BOOST,
)
from trosnoth.gui.framework import framework
from trosnoth.gui.framework.declarative import (
    DeclarativeElement, Rectangle, Text, PygameSurface,
    Button,
)
from trosnoth.gui.common import (
    Location, FullScreenAttachedPoint, ScaledSize, Area,
)
from trosnoth.gui.keyboard import shortcutName
from trosnoth.messages import (
    BuyUpgradeMsg, RespawnRequestMsg, EmoteRequestMsg,
    PlayerIsReadyMsg, ThrowTrosballMsg,
)
from trosnoth.model.player import Player
from trosnoth.model.shot import (
    PredictedGhostShotTrajectory,
)
from trosnoth.model.trosball import PredictedTrosballTrajectory
from trosnoth.model.unit import PredictedTrajectory, PredictedProjectileTrajectory
from trosnoth.model.upgrades import allUpgrades, gun_types, TeamBoost
from trosnoth.trosnothgui.ingame.messagebank import MessageBank
from trosnoth.trosnothgui.ingame import mainMenu
from trosnoth.trosnothgui.ingame.gamevote import GameVoteMenu
from trosnoth.trosnothgui.ingame.gauges import (
    RespawnGauge, SingleUpgradeGauge, GunGauge, SingleAmmoGauge, ItemCostGauge,
    SingleTeamBoostGauge, GaugeAppearance,
)
from trosnoth.trosnothgui.ingame.chatBox import ChatBox
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen

from trosnoth.trosnothgui.ingame.upgradeinterface import RadialUpgradeMenu
from trosnoth.utils.aio import create_safe_task
from trosnoth.welcome.keygrab import hidden_qt_toplevels, KeyGrabberElement

log = logging.getLogger(__name__)


class DetailsInterface(framework.CompoundElement):
    '''Interface containing all the overlays onto the screen:
    chat messages, player lists, gauges, coins, etc.'''
    def __init__(self, app, gameInterface):
        super(DetailsInterface, self).__init__(app)
        self.gameInterface = gameInterface
        self.settings_screen_task = None
        self.settings_screen = None
        self.cycle_team_boost = False
        self.team_boost_contributor = TeamBoostContributor(gameInterface.current_boost_purchase)

        # Maximum number of messages viewable at any one time
        maxView = 8

        self.world = gameInterface.world
        self.player = None
        font = app.screenManager.fonts.messageFont
        self.currentMessages = MessageBank(self.app, maxView, 50,
                Location(FullScreenAttachedPoint(ScaledSize(-40,-40),
                'bottomright'), 'bottomright'), 'right', 'bottom', font)

        # If we want to keep a record of all messages and their senders
        self.input = None
        self.inputText = None
        self.unobtrusiveGetter = None
        self.reloadGauge = GunGauge(self.app, Area(
                FullScreenAttachedPoint(ScaledSize(0,-60), 'midbottom'),
                ScaledSize(100,30), 'midbottom'))
        self.respawn_gauge = None
        self._update_respawn_gauge()
        self.itemGauge = ItemGauge(self.app, self.player)
        self.gun_gauge = AllGunsGauge(self.app, self.player)
        self.currentUpgrade = None

        self.chatBox = ChatBox(app, self.world, self.gameInterface)

        menuloc = Location(FullScreenAttachedPoint((0,0), 'bottomleft'),
                'bottomleft')
        self.menuManager = mainMenu.MainMenu(self.app, menuloc, self,
                self.gameInterface.keyMapping)
        self.trajectoryOverlay = TrajectoryOverlay(app, gameInterface.gameViewer.viewManager, self)
        self.radialUpgradeMenu = RadialUpgradeMenu(app, self.player, self._setCurrentUpgrade)
        self.radialUpgradeMenu.start()
        self.gameVoteMenu = GameVoteMenu(app, self.world, on_change=self._castGameVote)
        self._gameVoteUpdateCounter = 0
        self.elements = [
            self.currentMessages,
            DeclarativeElement(app, (0, -1), UpgradePanel(self)),
            self.reloadGauge, self.respawn_gauge,
            self.gameVoteMenu, self.chatBox,
            self.trajectoryOverlay, self.menuManager, self.itemGauge, self.gun_gauge,
            self.radialUpgradeMenu,
        ]

        self.upgradeMap = dict((upgradeClass.action, upgradeClass) for
                upgradeClass in allUpgrades)
        self.gun_map = {gun_type.action: gun_type for gun_type in gun_types}

    def stop(self):
        self.radialUpgradeMenu.stop()

    def sendRequest(self, msg):
        return self.gameInterface.sendRequest(msg)

    def tick(self, delta_t):
        super(DetailsInterface, self).tick(delta_t)

        self._updateGameVoteMenu()
        self.team_boost_contributor.tick(delta_t)

    def _castGameVote(self, msg):
        self.sendRequest(msg)

    def _updateGameVoteMenu(self):
        show_vote_menu = self.world.uiOptions.showReadyStates and self.player is not None
        self.gameVoteMenu.set_active(show_vote_menu)
        self.gameInterface.gameInfoDisplay.set_active(not show_vote_menu)

        if show_vote_menu:
            if self._gameVoteUpdateCounter <= 0:
                self.gameVoteMenu.update(self.player)
                self._gameVoteUpdateCounter = 25
            else:
                self._gameVoteUpdateCounter -= 1

    def _update_respawn_gauge(self):
        if self.respawn_gauge is not None:
            self.elements.remove(self.respawn_gauge)
        self.respawn_gauge = RespawnGauge(
            self.app,
            Area(
                FullScreenAttachedPoint(ScaledSize(0, -60), 'midbottom'),
                ScaledSize(100, 30),
                'midbottom'),
            self.player,
            self.world)
        self.elements.append(self.respawn_gauge)

    def setPlayer(self, player):
        if self.player is not None:
            self.player.onPrivateChatReceived.removeListener(self.privateChat)

        self.player = player
        if player:
            self.player.onPrivateChatReceived.addListener(self.privateChat)

        self.reloadGauge.player = player
        self._update_respawn_gauge()
        self.itemGauge.set_player(player)
        self.gun_gauge.set_player(player)
        self.radialUpgradeMenu.set_player(player)

    def show_settings(self):
        from trosnoth.welcome.settings import SettingsScreen
        if self.settings_screen_task and not self.settings_screen_task.done():
            self.settings_screen.raise_to_top()
            return
        self.settings_screen = SettingsScreen(self.grab_hotkey)
        self.settings_screen_task = create_safe_task(self._show_settings_then_update_key_map())

    async def _show_settings_then_update_key_map(self):
        try:
            await self.settings_screen.run()
        finally:
            self.gameInterface.updateKeyMapping()

    async def grab_hotkey(self, parent_window, prompt, title=None):
        with hidden_qt_toplevels():
            return await KeyGrabberElement(self.app, prompt).show()

    def _setCurrentUpgrade(self, upgradeType):
        self.currentUpgrade = upgradeType
        self.menuManager.manager.reset()

    def _requestUpgrade(self):
        if self.player.hasTrosball():
            self.sendRequest(ThrowTrosballMsg(self.getTickId()))
        elif self.currentUpgrade is not None and self.currentUpgrade.pre_buy_check(self.player):
            self.sendRequest(BuyUpgradeMsg(
                self.currentUpgrade.upgradeType, self.getTickId()))

    def getTickId(self):
        return self.world.lastTickId

    def doAction(self, action):
        '''
        Activated by hotkey or menu.
        action corresponds to the action name in the keyMapping.
        '''
        if action == ACTION_SETTINGS_MENU:
            self.show_settings()
        elif action == ACTION_QUIT_MENU:
            self.menuManager.showQuitMenu()
        elif action == ACTION_REALLY_QUIT:
            # Disconnect from the server.
            self.gameInterface.disconnect()
        elif action == ACTION_JOIN_GAME:
            # Join if currently spectating
            self.gameInterface.spectatorWantsToJoin()
        elif action == ACTION_PAUSE_GAME:
            if self.world.isServer:
                self.world.pauseOrResumeGame()
                if self.world.paused:
                    self.newMessage('Game paused')
                else:
                    self.newMessage('Game resumed')
            else:
                self.newMessage(
                    'You can only pause games from the server', error=True)
        elif action == ACTION_MAIN_MENU:
            # Return to main menu and show or hide the menu.
            self.menuManager.escape()
        elif action == ACTION_TERMINAL_TOGGLE:
            self.gameInterface.toggleTerminal()
        elif self.gameInterface.is_spectating():
            # Replay-specific actions
            if action in (ACTION_FOLLOW, ACTION_USE_UPGRADE):
                # Follow the game action
                self.gameInterface.gameViewer.setTarget(None)
        else:
            # All actions after this line should require a player.
            if self.player is None:
                return

            paused = self.world.uiOptions.showPauseMessage
            if action == ACTION_RESPAWN:
                if not paused:
                    self.sendRequest(
                        RespawnRequestMsg(tickId=self.getTickId()))
            elif action == ACTION_READY:
                if self.player.readyToStart:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, False))
                else:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, True))
            elif action in self.upgradeMap:
                self._setCurrentUpgrade(self.upgradeMap[action])
            elif action == ACTION_CLEAR_UPGRADE:
                self._setCurrentUpgrade(None)
                self.menuManager.manager.reset()
            elif action in self.gun_map:
                gun = self.player.guns.get(self.gun_map[action])
                cost = gun.get_required_coins(self.player)
                if gun.ammo > 0 or gun.max_ammo == 0 or (
                        cost is not None and self.player.coins >= cost):
                    self.player.guns.please_select(gun)
            elif action == ACTION_CHAT:
                self.chat()
                self.menuManager.manager.reset()
            elif action == ACTION_USE_UPGRADE:
                if not paused:
                    self._requestUpgrade()
            elif action == ACTION_BUY_AMMO:
                self.player.current_gun.please_buy_ammo()
            elif action == ACTION_EMOTE:
                self.sendRequest(
                    EmoteRequestMsg(
                        tickId=self.getTickId(),
                        emoteId=random.randrange(MAX_EMOTE + 1)))
            elif action == ACTION_RADIAL_UPGRADE_MENU:
                self.radialUpgradeMenu.toggle()
            elif action == ACTION_NEXT_WEAPON:
                self.player.guns.scroll_selection(1)
            elif action == ACTION_PREVIOUS_WEAPON:
                self.player.guns.scroll_selection(-1)
            elif action == ACTION_NEXT_TEAM_BOOST:
                self.cycle_team_boost = True
            elif action == ACTION_CONTRIBUTE_TO_TEAM_BOOST:
                self.team_boost_contributor.start()
            elif action == ACTION_CONTRIBUTE_TO_TEAM_BOOST + KEY_UP:
                self.team_boost_contributor.stop()
            elif action.endswith(KEY_UP):
                pass
            elif action not in (
                    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
                    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY):
                log.warning('Unknown action: %r', action)

    def newMessage(self, text, colour=None, error=False):
        if colour is None:
            if error:
                colour = self.app.theme.colours.errorMessageColour
            else:
                colour = self.app.theme.colours.grey
        self.currentMessages.newMessage(text, colour)

    def privateChat(self, text, sender):
        # Destined for the one player
        text = " (private): " + text
        self.newChat(text, sender)

    def newChat(self, text, sender: Optional[Player]):
        if sender is None:
            self.chatBox.newServerMessage(text)
        else:
            colour = sender.team.shade(0.5, 1) if sender.team else (192, 192, 192)
            self.chatBox.newMessage(text, sender.nick, colour)

    def endInput(self):
        if self.input:
            self.elements.remove(self.input)
            self.input = None
        if self.inputText:
            self.elements.remove(self.inputText)
            self.inputText = None
        if self.unobtrusiveGetter:
            self.elements.remove(self.unobtrusiveGetter)
            self.unobtrusiveGetter = None
        if self.menuManager not in self.elements:
            self.elements.append(self.menuManager)
        self.input = self.inputText = None


    def inputStarted(self):
        self.elements.append(self.input)
        self.elements.append(self.inputText)
        self.input.onEsc.addListener(lambda sender: self.endInput())
        self.input.onEnter.addListener(lambda sender: self.endInput())

        try:
            self.elements.remove(self.menuManager)
        except ValueError:
            pass

    def chat(self):
        if not self.player:
            return

        if self.chatBox.isOpen():
            self.chatBox.close()
        else:
            pygame.key.set_repeat(300, 30)
            self.chatBox.open()
            self.chatBox.setPlayer(self.player)

    def upgradeUsed(self, player, upgradeCode):
        upgradeClass = player.world.getUpgradeType(upgradeCode)
        message = upgradeClass.getActivateNotification(player.nick)

        self.newMessage(message)


class MultiGauge(framework.CompoundElement):
    '''
    Keeps track of currently active items.
    '''

    def __init__(self, app):
        super().__init__(app)
        self.elements = []
        self.modification_key = None

    def tick(self, delta_t):
        key = self.get_modification_key()
        if key != self.modification_key:
            self.modification_key = key
            self.rebuild_gauges()
        super().tick(delta_t)

    def get_modification_key(self):
        raise NotImplementedError

    def rebuild_gauges(self):
        raise NotImplementedError

    def gauge_areas(self, items, y):
        items = list(items)
        x_offset = 80
        x = -0.5 * (len(items) - 1) * x_offset

        for item in items:
            area = Area(
                FullScreenAttachedPoint(ScaledSize(x, y), 'midbottom'),
                ScaledSize(40, 10), 'midbottom')

            yield area, item
            x += x_offset


class ItemGauge(MultiGauge):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_modification_key(self):
        return self.get_items() + self.get_team_boosts()

    def get_items(self):
        if self.player is None:
            return []
        return sorted(self.player.items.getAll(), key=lambda i: (i.sort_order, i.upgradeType))

    def get_team_boosts(self):
        if self.player is None or self.player.team is None:
            return []
        return sorted(
            self.player.team.boosts.get_active(), key=lambda b: (b.sort_order, b.boost_code))

    def rebuild_gauges(self):
        self.elements = []
        for area, item in self.gauge_areas(self.get_items() + self.get_team_boosts(), y=-40):
            if isinstance(item, TeamBoost):
                self.elements.append(SingleTeamBoostGauge(self.app, area, item))
            else:
                self.elements.append(SingleUpgradeGauge(self.app, area, item))


class AllGunsGauge(MultiGauge):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_modification_key(self):
        if self.player is None:
            return ()
        return (list(self.player.guns), self.player.current_gun)

    def rebuild_gauges(self):
        self.elements = []
        if self.player is None:
            return
        for area, gun in self.gauge_areas(self.player.guns, y=-10):
            gauge = SingleAmmoGauge(
                self.app, area,
                gun=gun,
                draw_panel=self.player.current_gun == gun,
            )
            self.elements.append(gauge)


@dataclass(frozen=True)
class UpgradePanel:
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if not self.details_interface.player:
            return
        frame.add(MoneyDisplayPanel(self.details_interface), at=(-170, 0))
        frame.add(UpgradeDisplayPanel(self.details_interface), at=(-90, 0))
        frame.add(TeamBoostPurchasePanel(self.details_interface), at=(141, 0))


@dataclass(frozen=True)
class MoneyDisplayPanel:
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {'coins': 0}

    def draw(self, frame, state):
        target_coins = self.details_interface.player.coins
        diff = target_coins - state['coins']
        if diff > 0:
            diff = round(max(0.1 * diff, min(diff, 500 * frame.delta_t)))
        elif diff < 0:
            diff = round(min(0.1 * diff, max(diff, -500 * frame.delta_t)))
        state['coins'] += diff
        coins = state['coins']
        coins -= round(self.details_interface.gameInterface.current_boost_purchase.coins)

        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                90, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        frame.add(
            Text(
                f'${coins:,}'.replace(',', '\N{hair space}'),
                height=30,
                max_width=70,
                font='FreeSans.ttf',
                text_colour=frame.app.theme.colours.coinsDisplayColour,
                shadow_offset=(1, 1),
            ),
            at=(0, 40),
        )

        try:
            shop_key = self.details_interface.gameInterface.keyMapping.getkey(
                ACTION_RADIAL_UPGRADE_MENU)
        except KeyError:
            subcaption = None
        else:
            subcaption = f'({shortcutName(shop_key)})'

        frame.add(
            Button(
                'SHOP',
                subcaption=subcaption,
                pos=(0, 65),
                size=(86, 29),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                on_click=self.details_interface.radialUpgradeMenu.toggle,
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=frame.app.settings.display.disable_shop_buttons,
            ),
        )


@dataclass(frozen=True)
class UpgradeDisplayPanel:
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        player = self.details_interface.player
        upgrade = self.details_interface.currentUpgrade
        if player.hasTrosball():
            image = frame.app.theme.sprites.trosball_image()
            use_text = 'THROW'
            gauge = None
            button_disabled = False
        elif upgrade:
            image = upgrade.get_icon(frame.app.theme.sprites)
            use_text = 'THROW' if upgrade.projectile_kind else 'USE'
            gauge = ItemCostGauge(
                player=player,
                upgrade=upgrade,
                size=(44, 8),
            )
            button_disabled = upgrade.get_denial_reason(player) is not None
        else:
            return

        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                48, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        frame.add(
            PygameSurface(image, width=38, height=38),
            at=(0, 20),
        )

        if gauge:
            frame.add(gauge, at=(0, 45))

        try:
            use_key = self.details_interface.gameInterface.keyMapping.getkey(ACTION_USE_UPGRADE)
        except KeyError:
            subcaption = None
        else:
            subcaption = f'({shortcutName(use_key)})'

        button_disabled = button_disabled or frame.app.settings.display.disable_shop_buttons
        frame.add(
            Button(
                use_text,
                subcaption=subcaption,
                pos=(0, 65),
                size=(44, 29),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                on_click=functools.partial(self.details_interface.doAction, ACTION_USE_UPGRADE),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=button_disabled,
            ),
        )


class TeamBoostContributor:
    def __init__(self, tracker):
        self.tracker = tracker
        self.running = False
        self.boost_class = None

    def switch(self, boost_class):
        if boost_class == self.boost_class:
            return
        self.stop()
        self.boost_class = boost_class

    def start(self, boost_class=None):
        self.stop()
        if boost_class is not None:
            self.boost_class = boost_class
        if self.boost_class is not None:
            self.running = True
            self.tracker.start_boost_purchase(self.boost_class)

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.boost_class == self.tracker.boost_class:
            self.tracker.complete_purchase()

    def is_active(self):
        if not self.running:
            return False
        return self.boost_class == self.tracker.boost_class

    def tick(self, delta_t):
        if self.is_active():
            self.tracker.contribute(500 * delta_t)
            if self.tracker.get_boost_progress_ratio() >= 1:
                self.stop()


@dataclass(frozen=True)
class TeamBoostPurchasePanel:
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {'order': [], 'current': 0}

    def draw(self, frame, state):
        if self.details_interface.cycle_team_boost:
            self.next_clicked(state)
            self.details_interface.cycle_team_boost = False

        new_order = []
        selected_index = 0
        if self.details_interface.player.team is None:
            pending = set()
        else:
            pending = {type(b) for b in self.details_interface.player.team.boosts.get_pending()}

            new_i = 0
            for i, boost_class in enumerate(state['order']):
                if boost_class in pending:
                    pending.remove(boost_class)
                    new_order.append(boost_class)
                    if i == state['current']:
                        selected_index = new_i
                    new_i += 1

        contributor = self.details_interface.team_boost_contributor
        if pending and not contributor.is_active():
            # Select the new upgrade
            selected_index = len(new_order)
        state['order'] = new_order + list(pending)
        state['current'] = selected_index
        if not state['order']:
            contributor.switch(None)
            return
        contributor.switch(state['order'][state['current']])

        boost_class = state['order'][selected_index]

        if contributor.is_active():
            coins = contributor.tracker.get_total_contributed_coins()
        else:
            boost = self.details_interface.player.team.boosts.get(boost_class)
            coins = boost.total_cost - boost.remaining_cost

        try:
            contribute_key = self.details_interface.gameInterface.keyMapping.getkey(
                ACTION_CONTRIBUTE_TO_TEAM_BOOST)
        except KeyError:
            contribute_key_name = None
        else:
            contribute_key_name = shortcutName(contribute_key)
        frame.add(TeamBoostPurchaseAppearance(
            boost_class=boost_class,
            index=selected_index + 1,
            count=len(state['order']),
            coins=coins,
            button_disabled=frame.app.settings.display.disable_shop_buttons,
            contribute_key=contribute_key_name,
            on_contribute_click=functools.partial(self.contribute_clicked, state),
            on_next_click=functools.partial(self.next_clicked, state),
            on_prev_click=functools.partial(self.prev_clicked, state),
        ))
        frame.register_listener(MOUSE_UP, self.seen_mouse_up)

    def contribute_clicked(self, state):
        self.details_interface.team_boost_contributor.start(state['order'][state['current']])

    def seen_mouse_up(self, state, pos, button):
        contributor = self.details_interface.team_boost_contributor
        if button == 1 and contributor.running:
            contributor.stop()
            return True
        return False

    def next_clicked(self, state):
        state['current'] += 1
        state['current'] %= len(state['order'])
        self.details_interface.team_boost_contributor.switch(state['order'][state['current']])

    def prev_clicked(self, state):
        state['current'] -= 1
        state['current'] %= len(state['order'])
        self.details_interface.team_boost_contributor.switch(state['order'][state['current']])


@dataclass(frozen=True)
class TeamBoostPurchaseAppearance:
    boost_class: Type[TeamBoost]
    index: int
    count: int
    coins: float
    button_disabled: bool
    contribute_key: str
    on_next_click: Callable
    on_prev_click: Callable
    on_contribute_click: Callable

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                150, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        extra_text = f' ({self.index}/{self.count})' if self.count > 1 else ''
        frame.add(
            Text(
                text=f'TEAM BOOST{extra_text}',
                height=9,
                font='FreeSans.ttf',
                max_width=140,
                text_colour=(0, 0, 0),
                shadow_offset=(1, 1),
                shadow_colour=(225, 225, 225),
            ),
            at=(0, 13),
        )
        frame.add(
            Text(
                text=self.boost_class.name,
                height=15,
                font='FreeSans.ttf',
                max_width=140,
                text_colour=(0, 0, 0),
                shadow_offset=(1, 1),
                shadow_colour=(240, 240, 240),
            ),
            at=(0, 28),
        )
        image = self.boost_class.get_icon(frame.app.theme.sprites)
        frame.add(
            PygameSurface(image, width=34, height=34),
            at=(-59, 45),
        )
        frame.add(
            GaugeAppearance(
                size=(114, 20),
                ratio=self.coins / self.boost_class.total_cost,
                foreground=colours.gaugeGood,
                border_width=1,
            ),
            at=(15, 45),
        )

        frame.add(
            Button(
                'Contribute' + f' ({self.contribute_key})' if self.contribute_key else '',
                pos=(0, 71),
                size=(106, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.button_disabled,
                on_click=self.on_contribute_click,
            ),
        )
        frame.add(
            Button(
                '«',
                pos=(-64, 71),
                size=(18, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.count <= 1,
                on_click=self.on_next_click,
            ),
        )
        frame.add(
            Button(
                '»',
                pos=(64, 71),
                size=(18, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.count <= 1,
                on_click=self.on_prev_click,
            ),
        )


class TrajectoryOverlay(framework.Element):
    def __init__(self, app, viewManager, details_interface):
        super(TrajectoryOverlay, self).__init__(app)
        self.viewManager = viewManager
        self.details_interface = details_interface
        self.enabled = False

    def setEnabled(self, enable):
        self.enabled = enable

    def isActive(self):
        return self.getTrajectory() is not None

    def getTrajectory(self) -> Optional[PredictedTrajectory]:
        if not self.enabled:
            return None

        player = self.viewManager.getTargetPlayer()
        if player.dead:
            if not player.inRespawnableZone():
                return None
            return PredictedGhostShotTrajectory(
                player.world, player, self.viewManager)

        if player.hasTrosball():
            return PredictedTrosballTrajectory(player.world, player)

        selected_upgrade = self.details_interface.currentUpgrade
        if selected_upgrade and selected_upgrade.projectile_kind:
            if player.coins >= selected_upgrade.requiredCoins:
                return PredictedProjectileTrajectory(player, selected_upgrade.projectile_kind)

        return player.current_gun.build_trajectory(player)

    def draw(self, surface):
        trajectory = self.getTrajectory()
        if trajectory is None:
            return

        focus = self.viewManager._focus
        area = self.viewManager.sRect

        points = list(trajectory.predictedTrajectoryPoints())
        numPoints = len(points)
        if numPoints == 0:
            return
        greenToYellow = [(i, 255, 0) for i in range(
            0, 255, 255 // (numPoints // 2 + numPoints % 2))]
        yellowToRed = [(255, i, 0) for i in range(
            255, 0, -255 // (numPoints // 2))]

        colours = [(0, 255, 0)] + greenToYellow + yellowToRed

        lastPoint = None
        for item in zip(points, colours):
            point = item[0]
            colour = item[1]
            # Set first point
            if lastPoint is None:
                lastPoint = point
                adjustedPoint = mapPosToScreen(point, focus, area)
                pygame.draw.circle(surface, colour, adjustedPoint, 2)
                continue


            adjustedPoint = mapPosToScreen(point, focus, area)
            adjustedLastPoint = mapPosToScreen(lastPoint, focus, area)

            pygame.draw.line(surface, colour, adjustedLastPoint, adjustedPoint, 5)

            lastPoint = point

        pygame.draw.circle(surface, colour, adjustedPoint, 2)

        radius = int(trajectory.explosionRadius() * MAP_TO_SCREEN_SCALE)
        if radius > 0:
            pygame.draw.circle(surface, (0,0,0), adjustedPoint, radius, 2)
