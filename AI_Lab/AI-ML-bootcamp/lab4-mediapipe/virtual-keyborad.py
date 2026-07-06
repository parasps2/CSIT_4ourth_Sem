import cv2
import mediapipe as mp
import numpy as np
import time

# ── MediaPipe setup ──────────────────────────────────────────────────────────
mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
)

# ── Keyboard layout ──────────────────────────────────────────────────────────
KEYBOARD_ROWS = [
    ['1','2','3','4','5','6','7','8','9','0','&','N','M'],
    ['Q','W','E','R','T','Y','U','I','C','P','A','S','D'],
    ['F','G','H','J','K','L','Z','X','O','V','B','Sp','Bk'],
]

# ── Window / frame size ──────────────────────────────────────────────────────
WIN_W, WIN_H = 1500, 900

# ── Layout constants (scaled up) ─────────────────────────────────────────────
KEY_W, KEY_H = 88, 70
KEY_GAP      = 10
KB_ORIGIN_X  = 55
KB_ORIGIN_Y  = 420

TEXTBOX_X, TEXTBOX_Y = 55, 35
TEXTBOX_W, TEXTBOX_H = 960, 90

# Buttons top-right area
BTN_Y       = 35
BTN_H       = 90
CLEAR_X     = TEXTBOX_X + TEXTBOX_W + 20
CLEAR_W     = 140
RULES_X     = CLEAR_X + CLEAR_W + 12
RULES_W     = 140
START_X     = RULES_X + RULES_W + 12
START_W     = 165

# ── Interaction constants ────────────────────────────────────────────────────
CLICK_DIST  = 38    # px – pinch threshold
COOLDOWN    = 0.75  # s  – between any two clicks

# ── Colors (BGR) ─────────────────────────────────────────────────────────────
C_KEY_BG       = (170, 170, 170)
C_KEY_HOVER    = (50,  190, 255)
C_KEY_ACTIVE   = (30,  220, 80)   # flash on press
C_KEY_TXT      = (15,  15,  15)
C_TEXTBOX_BG   = (255, 255, 255)
C_TEXTBOX_BD   = (90,  90,  90)
C_CLEAR        = (50,  50,  210)
C_RULES        = (0,   0,   200)
C_START        = (20,  140, 20)
C_START_HOVER  = (30,  200, 30)
C_BAR          = (18,  18,  18)
C_WHITE        = (255, 255, 255)
C_BLACK        = (0,   0,   0)
C_DOT_IDX      = (0,   255, 100)
C_DOT_MID      = (0,   160, 255)
C_HOVER_BORDER = (0,   230, 255)


# ── Drawing helpers ───────────────────────────────────────────────────────────
def filled_rounded(img, x, y, w, h, r, color):
    cv2.rectangle(img, (x+r, y),   (x+w-r, y+h),   color, -1)
    cv2.rectangle(img, (x,   y+r), (x+w,   y+h-r), color, -1)
    for cx, cy in [(x+r, y+r),(x+w-r, y+r),(x+r, y+h-r),(x+w-r, y+h-r)]:
        cv2.circle(img, (cx, cy), r, color, -1)

def border_rounded(img, x, y, w, h, r, color, t=2):
    cv2.rectangle(img, (x+r, y),   (x+w-r, y+h),   color, t)
    cv2.rectangle(img, (x,   y+r), (x+w,   y+h-r), color, t)
    for cx, cy in [(x+r, y+r),(x+w-r, y+r),(x+r, y+h-r),(x+w-r, y+h-r)]:
        cv2.circle(img, (cx, cy), r, color, t)

def center_text(img, text, x, y, w, h, font_scale, color, thickness=2):
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    tx = x + (w - tw) // 2
    ty = y + (h + th) // 2
    cv2.putText(img, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

def inside(px, py, rx, ry, rw, rh):
    return rx <= px <= rx+rw and ry <= py <= ry+rh

def finger_pts(lm, idx_a, idx_b, fw, fh):
    ax = int(lm[idx_a].x * fw);  ay = int(lm[idx_a].y * fh)
    bx = int(lm[idx_b].x * fw);  by = int(lm[idx_b].y * fh)
    return np.hypot(ax-bx, ay-by), (ax, ay), (bx, by)

def key_rect(row, col):
    x = KB_ORIGIN_X + col * (KEY_W + KEY_GAP)
    y = KB_ORIGIN_Y + row * (KEY_H + KEY_GAP)
    return x, y, KEY_W, KEY_H


# ── Rules overlay ────────────────────────────────────────────────────────────
RULES_LINES = [
    "VIRTUAL KEYBOARD  –  HOW TO USE",
    "",
    "1.  Point your index finger at any key to hover it.",
    "2.  Pinch index + middle finger together to CLICK.",
    "3.  [Sp]  →  Space bar",
    "4.  [Bk]  →  Backspace  (removes last character)",
    "5.  Clear →  Wipes entire text box",
    "6.  Start Session →  Closes keyboard when done.",
    "7.  Keep hand steady; cooldown = 0.75 s per press.",
    "",
    "  Hover BACK below and pinch to return.",
]
BACK_X, BACK_Y, BACK_W, BACK_H = 80, 620, 160, 65

def draw_rules(frame):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0,0), (frame.shape[1], frame.shape[0]), (15,15,15), -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    y0 = 90
    for i, line in enumerate(RULES_LINES):
        big  = (i == 0)
        fs   = 0.95 if big else 0.68
        fw   = 2    if big else 1
        col  = C_KEY_HOVER if big else C_WHITE
        cv2.putText(frame, line, (80, y0 + i*48),
                    cv2.FONT_HERSHEY_SIMPLEX, fs, col, fw)
    filled_rounded(frame, BACK_X, BACK_Y, BACK_W, BACK_H, 12, (70,70,70))
    center_text(frame, "BACK", BACK_X, BACK_Y, BACK_W, BACK_H, 0.85, C_WHITE, 2)


# ── Session-end splash ────────────────────────────────────────────────────────
def draw_session_end(frame, typed):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0,0), (frame.shape[1], frame.shape[0]), (10,20,10), -1)
    cv2.addWeighted(overlay, 0.90, frame, 0.10, 0, frame)
    msg1 = "Session Ended"
    msg2 = f'You typed: "{typed}"' if typed else "(nothing typed)"
    msg3 = "Window closing..."
    cv2.putText(frame, msg1, (WIN_W//2 - 180, WIN_H//2 - 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, C_START_HOVER, 3)
    cv2.putText(frame, msg2, (WIN_W//2 - 300, WIN_H//2 + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, C_WHITE, 2)
    cv2.putText(frame, msg3, (WIN_W//2 - 130, WIN_H//2 + 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (120,120,120), 1)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  WIN_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WIN_H)

    typed_text      = ""
    last_click_time = 0.0
    show_rules      = False
    # Track which key was last pressed for visual flash
    last_pressed_key = None   # (row, col) or special string
    last_press_time  = 0.0

    # --- Backspace state machine ---
    bk_held_since   = None    # time when Bk pinch started
    BK_HOLD_DELAY   = 0.6     # seconds before repeat kicks in
    BK_REPEAT_RATE  = 0.12    # seconds between repeat deletes
    bk_last_repeat  = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        # Resize to guaranteed window size
        frame = cv2.resize(frame, (WIN_W, WIN_H))
        h, w  = frame.shape[:2]

        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        ix, iy    = -1, -1
        pinching  = False   # currently pinched (not edge-triggered)
        clicked   = False   # edge: just pinched this frame (with cooldown)
        now       = time.time()

        if result.multi_hand_landmarks:
            for hand_lm in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)
                lm = hand_lm.landmark

                dist, pt_idx, pt_mid = finger_pts(lm, 8, 12, w, h)
                ix, iy = pt_idx
                pinching = dist < CLICK_DIST

                # Finger dots
                cv2.circle(frame, pt_idx, 12, C_DOT_IDX, -1)
                cv2.circle(frame, pt_mid,  9, C_DOT_MID, -1)
                if pinching:
                    cv2.line(frame, pt_idx, pt_mid, (0, 255, 0), 3)

                if pinching and (now - last_click_time) > COOLDOWN:
                    clicked = True
                    last_click_time = now

        # ── Rules screen ─────────────────────────────────────────────────────
        if show_rules:
            draw_rules(frame)
            hover_back = inside(ix, iy, BACK_X, BACK_Y, BACK_W, BACK_H)
            if hover_back:
                border_rounded(frame, BACK_X, BACK_Y, BACK_W, BACK_H, 12, C_HOVER_BORDER, 3)
            if clicked and hover_back:
                show_rules = False
            cv2.rectangle(frame, (0, h-45), (w, h), C_BAR, -1)
            cv2.putText(frame, "Pinch to click BACK  |  ESC to quit",
                        (w//2-200, h-12), cv2.FONT_HERSHEY_SIMPLEX, 0.65, C_WHITE, 1)
            cv2.imshow("Virtual Keyboard", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # ── Text box ─────────────────────────────────────────────────────────
        filled_rounded(frame, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_W, TEXTBOX_H, 12, C_TEXTBOX_BG)
        border_rounded(frame, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_W, TEXTBOX_H, 12, C_TEXTBOX_BD, 2)
        # Show last N chars that fit
        display = typed_text
        max_chars = 52
        if len(display) > max_chars:
            display = "…" + display[-(max_chars-1):]
        cv2.putText(frame, display,
                    (TEXTBOX_X+18, TEXTBOX_Y+62),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.95, C_BLACK, 2)
        # Blinking cursor
        if int(now * 2) % 2 == 0:
            (cw, _), _ = cv2.getTextSize(display, cv2.FONT_HERSHEY_SIMPLEX, 0.95, 2)
            cx = TEXTBOX_X + 18 + cw + 4
            cv2.line(frame, (cx, TEXTBOX_Y+20), (cx, TEXTBOX_Y+70), C_BLACK, 2)

        # ── Clear button ─────────────────────────────────────────────────────
        hov_clear = inside(ix, iy, CLEAR_X, BTN_Y, CLEAR_W, BTN_H)
        filled_rounded(frame, CLEAR_X, BTN_Y, CLEAR_W, BTN_H, 12,
                       C_KEY_HOVER if hov_clear else C_CLEAR)
        if hov_clear:
            border_rounded(frame, CLEAR_X, BTN_Y, CLEAR_W, BTN_H, 12, C_HOVER_BORDER, 3)
        center_text(frame, "Clear", CLEAR_X, BTN_Y, CLEAR_W, BTN_H, 0.9, C_WHITE, 2)
        if clicked and hov_clear:
            typed_text = ""      # ← clears ALL text

        # ── Rules button ─────────────────────────────────────────────────────
        hov_rules = inside(ix, iy, RULES_X, BTN_Y, RULES_W, BTN_H)
        filled_rounded(frame, RULES_X, BTN_Y, RULES_W, BTN_H, 12,
                       C_KEY_HOVER if hov_rules else C_RULES)
        if hov_rules:
            border_rounded(frame, RULES_X, BTN_Y, RULES_W, BTN_H, 12, C_HOVER_BORDER, 3)
        center_text(frame, "Rules", RULES_X, BTN_Y, RULES_W, BTN_H, 0.9, C_WHITE, 2)
        if clicked and hov_rules:
            show_rules = True

        # ── Start Session button ──────────────────────────────────────────────
        hov_start = inside(ix, iy, START_X, BTN_Y, START_W, BTN_H)
        filled_rounded(frame, START_X, BTN_Y, START_W, BTN_H, 12,
                       C_START_HOVER if hov_start else C_START)
        if hov_start:
            border_rounded(frame, START_X, BTN_Y, START_W, BTN_H, 12, C_HOVER_BORDER, 3)
        center_text(frame, "Start Session", START_X, BTN_Y, START_W, BTN_H, 0.72, C_WHITE, 2)
        if clicked and hov_start:
            # Show splash for 2 seconds, then exit
            draw_session_end(frame, typed_text)
            cv2.imshow("Virtual Keyboard", frame)
            cv2.waitKey(2200)
            break

        # ── Keyboard keys ─────────────────────────────────────────────────────
        bk_hovered = False
        for r, row in enumerate(KEYBOARD_ROWS):
            for c, key in enumerate(row):
                x, y, kw, kh = key_rect(r, c)
                hovering = inside(ix, iy, x, y, kw, kh)

                # Flash recently pressed key green
                flashing = (
                    last_pressed_key == (r, c)
                    and (now - last_press_time) < 0.18
                )
                if flashing:
                    bg = C_KEY_ACTIVE
                elif hovering:
                    bg = C_KEY_HOVER
                else:
                    bg = C_KEY_BG

                filled_rounded(frame, x, y, kw, kh, 10, bg)
                if hovering:
                    border_rounded(frame, x, y, kw, kh, 10, C_HOVER_BORDER, 2)

                fs = 0.58 if len(key) > 1 else 0.78
                center_text(frame, key, x, y, kw, kh, fs, C_KEY_TXT, 2)

                if key == 'Bk' and hovering:
                    bk_hovered = True

                if clicked and hovering:
                    if key == 'Bk':
                        typed_text = typed_text[:-1]
                        bk_held_since = now
                        bk_last_repeat = now
                    elif key == 'Sp':
                        typed_text += ' '
                    else:
                        typed_text += key
                    last_pressed_key = (r, c)
                    last_press_time  = now

        # ── Backspace HOLD-to-repeat ──────────────────────────────────────────
        if bk_hovered and pinching:
            if bk_held_since is None:
                bk_held_since = now
            held = now - bk_held_since
            if held > BK_HOLD_DELAY and (now - bk_last_repeat) > BK_REPEAT_RATE:
                typed_text    = typed_text[:-1]
                bk_last_repeat = now
        else:
            bk_held_since = None

        # ── Bottom status bar ─────────────────────────────────────────────────
        cv2.rectangle(frame, (0, h-45), (w, h), C_BAR, -1)
        status = (f"Chars: {len(typed_text)}  |  "
                  "Point to hover  |  Pinch to click  |  Hold [Bk] to delete  |  ESC to quit")
        cv2.putText(frame, status, (30, h-13),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.58, C_WHITE, 1)

        cv2.imshow("Virtual Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    if 'typed_text' in dir():
        print(f"\n[Session ended] Typed text: {typed_text}")


if __name__ == "__main__":
    main()