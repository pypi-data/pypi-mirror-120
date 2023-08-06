'''
Provides a layer between a universe and the GUI, turning
players, shots, grenades into sprites, and drawing mapblocks.
'''

import logging
import time

from trosnoth.model.projectile import MineProjectile, LocalMine
from trosnoth.trosnothgui.ingame.sprites import (
    PlayerSprite, ShotSprite, GrenadeSprite, GrenadeExplosionSprite,
    CollectableCoinSprite, ShoxwaveExplosionSprite, TrosballSprite,
    TrosballExplosionSprite, MineExplosionSprite, MineSprite,
)
from trosnoth.utils import globaldebug

log = logging.getLogger(__name__)


PROJECTILE_SPRITE_MAP = {
    MineProjectile: MineSprite,
    LocalMine: MineSprite,
}


class UniverseGUI(object):

    # For debugging, displays where the player is server-side too
    SHOW_SERVER_SHADOWS = False

    def __init__(self, app, gameViewer, universe):
        self.app = app
        self.gameViewer = gameViewer
        self.universe = universe
        self.playerSprites = {}     # playerId -> PlayerSprite
        self.localPlayerId = None
        self.localPlayerSprite = None
        self.shotSprites = {}       # shotId -> ShotSprite
        self.localShotSprites = {}  # shot -> ShotSprite
        self.grenade_sprites = {}    # GrenadeShot -> GrenadeSprite
        self.projectile_sprites = {}
        self.collectableCoinSprites = {}    # coinId -> CollectableCoinSprite
        self.extraSprites = set()
        self.trosballSprite = None
        self.tweenFraction = 1
        self.realTime = time.time()

        app.settings.display.on_detail_level_changed.addListener(
            self.detailLevelChanged)

    def stop(self):
        self.app.settings.display.on_detail_level_changed.removeListener(
            self.detailLevelChanged)

    def detailLevelChanged(self):
        # Clear everything long-lived
        self.playerSprites = {}
        self.collectableCoinSprites = {}
        self.trosballSprite = None
        if self.localPlayerId is not None:
            p = self.localPlayerSprite
            self.localPlayerSprite = PlayerSprite(self.app, self, p.player)

    def setTweenFraction(self, f):
        self.tweenFraction = f
        self.realTime = time.time()

    def getTime(self):
        t = self.universe.getMonotonicTime()
        t -= (1 - self.tweenFraction) * self.universe.tickPeriod
        return t

    @property
    def zones(self):
        return self.universe.zones

    @property
    def teams(self):
        return self.universe.teams

    @property
    def map(self):
        return self.universe.map

    @property
    def zoneBlocks(self):
        return self.universe.zoneBlocks

    def getTrosballSprite(self):
        if not self.universe.trosballManager.enabled:
            return None
        if self.trosballSprite is None:
            self.trosballSprite = TrosballSprite(self.app, self, self.universe)
        return self.trosballSprite

    def getPlayerSprite(self, playerId, ignoreLocal=False):
        player = self.universe.getPlayer(playerId)
        if player is None:
            return None
        if playerId == self.localPlayerId and not ignoreLocal:
            p = self.localPlayerSprite
            if p.spriteTeam != p.player.team:
                self.localPlayerSprite = PlayerSprite(
                    self.app, self, p.player)
                if p is self.gameViewer.viewManager.target:
                    self.gameViewer.viewManager.setTarget(
                        self.localPlayerSprite)
                p = self.localPlayerSprite
            return p

        try:
            p = self.playerSprites[playerId]
        except KeyError:
            self.playerSprites[player.id] = p = PlayerSprite(
                self.app, self, player)
            return p

        if p.spriteTeam != player.team:
            # Player has changed teams.
            self.playerSprites[player.id] = p = PlayerSprite(
                self.app, self, player)
        return p

    def overridePlayer(self, player):
        self.localPlayerId = player.id
        self.localPlayerSprite = PlayerSprite(self.app, self, player)

    def removeOverride(self):
        self.localPlayerId = None
        self.localPlayerSprite = None

    def iterPlayers(self):
        untouched = set(self.playerSprites.keys())
        for player in self.universe.players:
            untouched.discard(player.id)
            yield self.getPlayerSprite(player.id)
            if self.SHOW_SERVER_SHADOWS and player.id == self.localPlayerId:
                yield self.getPlayerSprite(player.id, ignoreLocal=True)

        # Clean up old players.
        for playerId in untouched:
            del self.playerSprites[playerId]

    def iter_projectiles(self):
        untouched = set(self.projectile_sprites)
        new_sprites = {}

        def sprite(p):
            try:
                sprite = self.projectile_sprites[p]
            except KeyError:
                # TODO: eventually localState.projectiles will also have other
                #   things, such as grenades
                sprite = PROJECTILE_SPRITE_MAP[type(p)](self.app, self, p)
            new_sprites[p] = sprite
            return sprite

        server_projectiles = set(self.universe.projectile_by_id.values())
        for projectile in self.gameViewer.interface.localState.projectiles:
            if not self.SHOW_SERVER_SHADOWS:
                server_projectiles.discard(projectile.server_projectile)
            yield sprite(projectile)
        for projectile in server_projectiles:
            yield sprite(projectile)

        self.projectile_sprites = new_sprites

    def iterGrenades(self):
        untouched = set(self.grenade_sprites.keys())
        for grenade in self.universe.grenades:
            if (
                    grenade.player.id == self.localPlayerId
                    and not self.SHOW_SERVER_SHADOWS):
                continue
            try:
                yield self.grenade_sprites[grenade]
            except KeyError:
                self.grenade_sprites[grenade] = g = (
                    GrenadeSprite(self.app, self, grenade))
                yield g
            else:
                untouched.discard(grenade)

        for grenade in self.gameViewer.interface.localState.local_grenades:
            yield GrenadeSprite(self.app, self, grenade)

        # Clean up old grenades.
        for grenade in untouched:
            del self.grenade_sprites[grenade]

    def iterShots(self):
        untouched = set(self.shotSprites.keys())
        untouchedLocals = set(self.localShotSprites.keys())
        for shot in self.universe.shots:
            if not shot.originatingPlayer and not shot.gun_type.neutral_shots:
                continue
            if (
                    not shot.gun_type.neutral_shots
                    and shot.originatingPlayer.id == self.localPlayerId
                    and not self.SHOW_SERVER_SHADOWS):
                continue
            if shot.justFired:
                continue
            if shot.expired and not globaldebug.enabled:
                continue
            try:
                yield self.shotSprites[shot.id]
            except KeyError:
                self.shotSprites[shot.id] = s = (
                    ShotSprite(self.app, self, shot))
                yield s
            untouched.discard(shot.id)

        for shot in self.gameViewer.interface.localState.shots:
            if shot.justFired:
                continue
            try:
                yield self.localShotSprites[shot]
            except KeyError:
                self.localShotSprites[shot] = s = ShotSprite(
                    self.app, self, shot)
                yield s
            untouchedLocals.discard(shot)

        # Clean up old shots.
        for shotId in untouched:
            s = self.shotSprites[shotId]
            s.noLongerInUniverse()
            if s.shouldRemove():
                del self.shotSprites[shotId]
            else:
                yield s
        for shot in untouchedLocals:
            s = self.localShotSprites[shot]
            s.noLongerInUniverse()
            if s.shouldRemove():
                del self.localShotSprites[shot]
            else:
                yield s

    def iterCollectableCoins(self):
        untouched = set(self.collectableCoinSprites.keys())
        for coin in self.universe.collectableCoins.values():
            if coin.hitLocalPlayer:
                continue
            try:
                yield self.collectableCoinSprites[coin.id]
            except KeyError:
                self.collectableCoinSprites[coin.id] = s = (
                    CollectableCoinSprite(self.app, self, coin))
                yield s
            else:
                untouched.discard(coin.id)

        # Clean up old shots.
        for coinId in untouched:
            del self.collectableCoinSprites[coinId]

    def iterExtras(self):
        for sprite in list(self.extraSprites):
            if sprite.isDead():
                self.extraSprites.remove(sprite)
            yield sprite
        trosball = self.getTrosballSprite()
        if trosball:
            yield trosball

    def getPlayerCount(self):
        return len(self.universe.players)

    def hasPlayer(self, player):
        return (
            player.id in self.playerSprites or player.id == self.localPlayerId)

    def getPlayersInZone(self, zone):
        result = []
        for p in zone.players:
            ps = self.getPlayerSprite(p.id)
            if ps is not None:
                result.append(ps)
        return result

    def addExplosion(self, pos):
        self.extraSprites.add(GrenadeExplosionSprite(self, pos))

    def addTrosballExplosion(self, pos):
        self.extraSprites.add(TrosballExplosionSprite(self, pos))

    def addShoxwaveExplosion(self, pos):
        self.extraSprites.add(ShoxwaveExplosionSprite(self, pos))

    def add_mine_explosion(self, pos):
        self.extraSprites.add(MineExplosionSprite(self, pos))
