#!/usr/bin/env python3
"""
Tastatur-Soundboard
Öffnet ein Fenster. Im Vordergrund spielen Tasten 1-` und Buchstaben
die Dateien <taste>.mp3 / .ogg / .wav aus dem Programmverzeichnis.
Während der Ton läuft, wird <taste>.gif in Dauerschleife angezeigt.
"""

# alternatives:
# https://github.com/lovelak-pro/PySoundBoard
#

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
from pathlib import Path
from typing import Any

import pygame

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(__file__).absolute().parent

EXTENSIONS = (".mp3", ".ogg", ".wav")
ALLOWED_EXTRA = set("`-=ß´^")

KEY_TO_CH: dict[Any, str] = {
    pygame.K_BACKSPACE: "backspace",
    pygame.K_TAB: "tab",
    pygame.K_RETURN: "return",
    pygame.K_PLUS: "plus",
    pygame.K_COMMA: "comma",
    pygame.K_MINUS: "minus",
    pygame.K_PERIOD: "period",
    pygame.K_DELETE: "delete",
    pygame.K_INSERT: "insert",
    pygame.K_HOME: "home",
    pygame.K_END: "end",
    pygame.K_PAGEUP: "page_up",
    pygame.K_PAGEDOWN: "page_down",
    pygame.K_F1: "f1",
    pygame.K_F2: "f2",
    pygame.K_F3: "f3",
    pygame.K_F4: "f4",
    pygame.K_F5: "f5",
    pygame.K_F6: "f6",
    pygame.K_F7: "f7",
    pygame.K_F8: "f8",
    pygame.K_F9: "f9",
    pygame.K_F10: "f10",
    pygame.K_F11: "f11",
    pygame.K_F12: "f12",
    pygame.K_F13: "f13",
    pygame.K_F14: "f14",
    pygame.K_F15: "f15",
}


def is_trigger_key(ch: str, key: Any) -> str:
    ch_from_key = KEY_TO_CH.get(key, "")
    if len(ch_from_key):
        return ch_from_key
    if not ch:
        print(f"key {ch=} and {key=} is NO trigger key")
        return ""
    if len(ch) != 1:
        print(f"key {ch=} is NO trigger key")
        return False
    if ch.isalpha() or ch.isdigit():
        return ch
    if ch in ALLOWED_EXTRA:
        return ch
    print(f"key {ch=} and {key=} is NO trigger key")
    return ""


def _relative_path(file: Path, base: Path) -> Path:
    try:
        rel_path = file.relative_to(base, walk_up=True)
    except ValueError:
        return file
    if len(str(rel_path)) < len(str(file)):
        return rel_path
    return file


def find_sound_file(key: str) -> Path | None:
    base = key.lower()
    for ext in EXTENSIONS:
        path = APP_DIR / (base + ext)
        if path.is_file() and path.exists():
            rp = path.resolve()
            rel_path = _relative_path(path, APP_DIR)
            rel_rp = _relative_path(rp, APP_DIR)
            if rp == path:
                print(f"play file '{rel_rp}' for {key=}")
            else:
                print(f"play file '{rel_rp}' linked from '{rel_path}' for {key=}")
            return rp
    cwd = Path.cwd()
    if cwd != APP_DIR:
        for ext in EXTENSIONS:
            path = cwd / (base + ext)
            if path.is_file() and path.exists():
                rp = path.resolve()
                rel_path = _relative_path(path, cwd)
                rel_rp = _relative_path(rp, cwd)
                if rp == path:
                    print(f"play file '{rel_rp}' for {key=}")
                else:
                    print(f"play file '{rel_rp}' linked from '{rel_path}' for {key=}")
                return rp
    print(f"cannot find file for {key=} with basename '{base}'")
    return None


def find_gif_file(key: str) -> Path | None:
    base = key.lower()
    dirs = [APP_DIR, Path.cwd()]
    names = [base + ".gif", base + ".GIF", key + ".gif"]
    seen = set()
    for d in dirs:
        for name in names:
            path = d / name
            if path in seen:
                continue
            seen.add(path)
            if path.is_file() and path.exists():
                return path
    return None


def pil_to_surface(pil_image) -> pygame.Surface:
    rgba = pil_image.convert("RGBA")
    surf = pygame.image.frombytes(rgba.tobytes(), rgba.size, "RGBA")
    return surf.convert_alpha()


def load_gif_frames(path: Path | None) -> tuple[list, str]:
    if not path:
        return [], "kein Pfad"
    if not HAS_PIL:
        return [], "Pillow nicht geladen"
    try:
        img = Image.open(str(path))
        n = getattr(img, "n_frames", 1)
        frames = []
        for i in range(n):
            img.seek(i)
            frames.append(pil_to_surface(img.copy()))
        if not frames:
            return [], "0 Frames"
        return frames, ""
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}"


def scale_to_fit(surf: pygame.Surface, max_w: int, max_h: int) -> pygame.Surface:
    w, h = surf.get_size()
    if w <= 0 or h <= 0 or max_w <= 0 or max_h <= 0:
        return surf
    scale = min(max_w / w, max_h / h)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    if new_size == (w, h):
        return surf
    return pygame.transform.smoothscale(surf, new_size)


def main() -> None:
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    width, height = 720, 520
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tastatur-Soundboard – Fenster im Vordergrund halten")
    font = pygame.font.SysFont(None, 28)
    small = pygame.font.SysFont(None, 22)
    last_key = "–"
    status = "Bereit. Fenster fokussieren und Taste drücken."
    if not HAS_PIL:
        status = "Pillow fehlt (pip install Pillow) – GIFs aus. Ton geht."
    gif_frames: list[pygame.Surface] = []
    gif_index = 0
    gif_timer = 0
    frame_ms = 80
    clock = pygame.time.Clock()
    running = True
    paused = False
    snd_vol_db = 0.0
    print(f"will look for sound files in '{APP_DIR}'")
    print(f"  and in current working dir '{Path.cwd()}'")
    print(f"  valid sound file extensions: {EXTENSIONS}")
    print()
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keymods = pygame.key.get_mods()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                elif event.key == pygame.K_SPACE:
                    if not paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    paused = not paused
                    continue
                elif event.key == pygame.K_LEFT:
                    try:
                        pygame.mixer.music.play()
                    except pygame.error:
                        pass
                    continue
                elif event.key == pygame.K_DOWN:
                    if keymods & pygame.KMOD_CTRL:
                        snd_vol_db = -60.0
                    elif keymods & pygame.KMOD_SHIFT:
                        snd_vol_db = snd_vol_db - 6.0
                    else:
                        snd_vol_db = snd_vol_db - 1.0
                    snd_vol_db = max(snd_vol_db, -60.0)
                    snd_volume = 10 ** (snd_vol_db / 20.0)
                    print(f"volume: {snd_vol_db} dB = {snd_volume:.2f}")
                    pygame.mixer.music.set_volume(snd_volume)
                    continue
                elif event.key == pygame.K_UP:
                    if keymods & pygame.KMOD_CTRL:
                        snd_vol_db = 0.0
                    elif keymods & pygame.KMOD_SHIFT:
                        snd_vol_db = snd_vol_db + 6.0
                    else:
                        snd_vol_db = snd_vol_db + 1.0
                    snd_vol_db = min(snd_vol_db, 0.0)
                    snd_volume = 10 ** (snd_vol_db / 20.0)
                    print(f"volume: {snd_vol_db} dB = {snd_volume:.2f}")
                    pygame.mixer.music.set_volume(snd_volume)
                    continue
                ch = is_trigger_key(event.unicode or "", event.key)
                if not ch:
                    continue
                path = find_sound_file(ch)
                if path is None:
                    continue
                last_key = ch
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                    status = f"Spielt: {path.name}"
                except pygame.error:
                    continue
                gif_path = find_gif_file(ch)
                gif_frames, gif_err = load_gif_frames(gif_path)
                gif_index = 0
                gif_timer = 0
                if gif_frames:
                    status += f"  |  {gif_path.name} ({len(gif_frames)} Frames)"
                else:
                    status += f"  |  GIF nicht ladbar: {gif_err}"

        playing = pygame.mixer.music.get_busy()
        if gif_frames and not playing:
            gif_frames = []
            gif_index = 0
            gif_timer = 0

        screen.fill((28, 30, 38))
        title = font.render("Tastatur-Soundboard", True, (230, 230, 240))
        screen.blit(title, (20, 16))
        hint1 = small.render("Fokus halten. Tasten: Buchstaben, 0–9, ` - =", True, (160, 165, 180))
        hint2 = small.render(
            "Ton: Taste.mp3/.ogg/.wav   Bild: Taste.gif  (Dauerschleife solange Ton läuft)",
            True,
            (160, 165, 180),
        )
        hint3 = small.render("ESC oder Fenster schließen = Beenden", True, (160, 165, 180))
        screen.blit(hint1, (20, 50))
        screen.blit(hint2, (20, 72))
        screen.blit(hint3, (20, 94))
        key_surf = font.render(f"Letzte Taste:  {last_key}", True, (255, 200, 80))
        file_surf = small.render(status, True, (120, 200, 140))
        screen.blit(key_surf, (20, 122))
        screen.blit(file_surf, (20, 150))

        area_x, area_y = 20, 185
        area_w, area_h = width - 40, height - 205
        pygame.draw.rect(screen, (18, 20, 26), (area_x, area_y, area_w, area_h), border_radius=8)
        pygame.draw.rect(screen, (50, 54, 66), (area_x, area_y, area_w, area_h), width=1, border_radius=8)

        if playing and gif_frames:
            gif_timer += dt
            if gif_timer >= frame_ms:
                steps = max(1, gif_timer // frame_ms)
                gif_timer %= frame_ms
                gif_index = (gif_index + steps) % len(gif_frames)
            frame = scale_to_fit(gif_frames[gif_index], area_w - 16, area_h - 16)
            fx = area_x + (area_w - frame.get_width()) // 2
            fy = area_y + (area_h - frame.get_height()) // 2
            screen.blit(frame, (fx, fy))
        else:
            idle = small.render(
                "Kein GIF aktiv. Lege z. B. q.gif neben q.mp3.",
                True,
                (110, 115, 130),
            )
            screen.blit(idle, (area_x + 16, area_y + 16))
        pygame.display.flip()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
