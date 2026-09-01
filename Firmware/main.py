"""
KMK firmware for hackpad (Seeeduino XIAO, direct-wired keys — no matrix).

Pin mapping was extracted directly from PCB/hackpad.kicad_sch (net list):
  SW1 -> D5 (SCL)      SW4 -> D3
  SW2 -> D2             SW5 -> D4 (SDA)
  SW3 -> D1             SW6 -> D0
  SW8 (rotary encoder): A -> D8 (SCK), B -> D6 (TX), C -> D7 (RX)
                         push-switch S1 -> D9 (MISO), S2 -> D10 (MOSI)

All SW1-SW6 pin 1 legs go to GND, so keys are wired GPIO -> GND directly
(no diode matrix), hence KMK's direct pin map is used instead of matrix scan.

NOTE: the rotary encoder's push-switch (S1/S2) is wired between two GPIOs
rather than GPIO-to-GND in this design. Double check that's intentional
before assuming the encoder click works as a normal button.
"""
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

# Direct-wired pins (no matrix / no diodes)
keyboard.col_pins = (board.D5, board.D2, board.D1, board.D3, board.D4, board.D0)
keyboard.row_pins = (board.D9,)  # dummy single row required for direct pin scanning
keyboard.diode_orientation = DiodeOrientation.COLUMNS

# Keymap: one row of 6 keys, matching SW1..SW6 order above
keyboard.keymap = [
    [KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.Z), KC.LCTL(KC.Y), KC.LCTL(KC.S), KC.MUTE]
    # SW1: Copy   SW2: Paste   SW3: Undo   SW4: Redo   SW5: Save   SW6: Mute
]

# Rotary encoder (SW8): A=D8, B=D6. Turning it adjusts volume.
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D8, board.D6, None),)  # (pin_a, pin_b, button_pin)
encoder_handler.map = [((KC.VOLU, KC.VOLD),)]
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
