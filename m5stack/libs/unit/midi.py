# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.sam2695 import SAM2695

import sys

if sys.platform != "esp32":
    from typing import Literal

MIDI_NOTES = {
    "REST": 0,
    "NOTE_B0": 23,
    "NOTE_C1": 24,
    "NOTE_CS1": 25,
    "NOTE_D1": 26,
    "NOTE_DS1": 27,
    "NOTE_E1": 28,
    "NOTE_F1": 29,
    "NOTE_FS1": 30,
    "NOTE_G1": 31,
    "NOTE_GS1": 32,
    "NOTE_A1": 33,
    "NOTE_AS1": 34,
    "NOTE_B1": 35,
    "NOTE_C2": 36,
    "NOTE_CS2": 37,
    "NOTE_D2": 38,
    "NOTE_DS2": 39,
    "NOTE_E2": 40,
    "NOTE_F2": 41,
    "NOTE_FS2": 42,
    "NOTE_G2": 43,
    "NOTE_GS2": 44,
    "NOTE_A2": 45,
    "NOTE_AS2": 46,
    "NOTE_B2": 47,
    "NOTE_C3": 48,
    "NOTE_CS3": 49,
    "NOTE_D3": 50,
    "NOTE_DS3": 51,
    "NOTE_E3": 52,
    "NOTE_F3": 53,
    "NOTE_FS3": 54,
    "NOTE_G3": 55,
    "NOTE_GS3": 56,
    "NOTE_A3": 57,
    "NOTE_AS3": 58,
    "NOTE_B3": 59,
    "NOTE_C4": 60,
    "NOTE_CS4": 61,
    "NOTE_D4": 62,
    "NOTE_DS4": 63,
    "NOTE_E4": 64,
    "NOTE_F4": 65,
    "NOTE_FS4": 66,
    "NOTE_G4": 67,
    "NOTE_GS4": 68,
    "NOTE_A4": 69,
    "NOTE_AS4": 70,
    "NOTE_B4": 71,
    "NOTE_C5": 72,
    "NOTE_CS5": 73,
    "NOTE_D5": 74,
    "NOTE_DS5": 75,
    "NOTE_E5": 76,
    "NOTE_F5": 77,
    "NOTE_FS5": 78,
    "NOTE_G5": 79,
    "NOTE_GS5": 80,
    "NOTE_A5": 81,
    "NOTE_AS5": 82,
    "NOTE_B5": 83,
    "NOTE_C6": 84,
    "NOTE_CS6": 85,
    "NOTE_D6": 86,
    "NOTE_DS6": 87,
    "NOTE_E6": 88,
    "NOTE_F6": 89,
    "NOTE_FS6": 90,
    "NOTE_G6": 91,
    "NOTE_GS6": 92,
    "NOTE_A6": 93,
    "NOTE_AS6": 94,
    "NOTE_B6": 95,
    "NOTE_C7": 96,
    "NOTE_CS7": 97,
    "NOTE_D7": 98,
    "NOTE_DS7": 99,
    "NOTE_E7": 100,
    "NOTE_F7": 101,
    "NOTE_FS7": 102,
    "NOTE_G7": 103,
    "NOTE_GS7": 104,
    "NOTE_A7": 105,
    "NOTE_AS7": 106,
    "NOTE_B7": 107,
    "NOTE_C8": 108,
    "NOTE_CS8": 109,
    "NOTE_D8": 110,
    "NOTE_DS8": 111,
}

SYNTH_INSTRUMENTS = {
    "GrandPiano_1": 1,
    "BrightPiano_2": 2,
    "ElGrdPiano_3": 3,
    "HonkyTonkPiano": 4,
    "ElPiano1": 5,
    "ElPiano2": 6,
    "Harpsichord": 7,
    "Clavi": 8,
    "Celesta": 9,
    "Glockenspiel": 10,
    "MusicBox": 11,
    "Vibraphone": 12,
    "Marimba": 13,
    "Xylophone": 14,
    "TubularBells": 15,
    "Santur": 16,
    "DrawbarOrgan": 17,
    "PercussiveOrgan": 18,
    "RockOrgan": 19,
    "ChurchOrgan": 20,
    "ReedOrgan": 21,
    "AccordionFrench": 22,
    "Harmonica": 23,
    "TangoAccordion": 24,
    "AcGuitarNylon": 25,
    "AcGuitarSteel": 26,
    "AcGuitarJazz": 27,
    "AcGuitarClean": 28,
    "AcGuitarMuted": 29,
    "OverdrivenGuitar": 30,
    "DistortionGuitar": 31,
    "GuitarHarmonics": 32,
    "AcousticBass": 33,
    "FingerBass": 34,
    "PickedBass": 35,
    "FretlessBass": 36,
    "SlapBass1": 37,
    "SlapBass2": 38,
    "SynthBass1": 39,
    "SynthBass2": 40,
    "Violin": 41,
    "Viola": 42,
    "Cello": 43,
    "Contrabass": 44,
    "TremoloStrings": 45,
    "PizzicatoStrings": 46,
    "OrchestralHarp": 47,
    "Timpani": 48,
    "StringEnsemble1": 49,
    "StringEnsemble2": 50,
    "SynthStrings1": 51,
    "SynthStrings2": 52,
    "ChoirAahs": 53,
    "VoiceOohs": 54,
    "SynthVoice": 55,
    "OrchestraHit": 56,
    "Trumpet": 57,
    "Trombone": 58,
    "Tuba": 59,
    "MutedTrumpet": 60,
    "FrenchHorn": 61,
    "BrassSection": 62,
    "SynthBrass1": 63,
    "SynthBrass2": 64,
    "SopranoSax": 65,
    "AltoSax": 66,
    "TenorSax": 67,
    "BaritoneSax": 68,
    "Oboe": 69,
    "EnglishHorn": 70,
    "Bassoon": 71,
    "Clarinet": 72,
    "Piccolo": 73,
    "Flute": 74,
    "Recorder": 75,
    "PanFlute": 76,
    "BlownBottle": 77,
    "Shakuhachi": 78,
    "Whistle": 79,
    "Ocarina": 80,
    "Lead1Square": 81,
    "Lead2Sawtooth": 82,
    "Lead3Calliope": 83,
    "Lead4Chiff": 84,
    "Lead5Charang": 85,
    "Lead6Voice": 86,
    "Lead7Fifths": 87,
    "Lead8BassLead": 88,
    "Pad1Fantasia": 89,
    "Pad2Warm": 90,
    "Pad3PolySynth": 91,
    "Pad4Choir": 92,
    "Pad5Bowed": 93,
    "Pad6Metallic": 94,
    "Pad7Halo": 95,
    "Pad8Sweep": 96,
    "FX1Rain": 97,
    "FX2Soundtrack": 98,
    "FX3Crystal": 99,
    "FX4Atmosphere": 100,
    "FX5Brightness": 101,
    "FX6Goblins": 102,
    "FX7Echoes": 103,
    "FX8SciFi": 104,
    "Sitar": 105,
    "Banjo": 106,
    "Shamisen": 107,
    "Koto": 108,
    "Kalimba": 109,
    "BagPipe": 110,
    "Fiddle": 111,
    "Shanai": 112,
    "TinkleBell": 113,
    "Agogo": 114,
    "SteelDrums": 115,
    "Woodblock": 116,
    "TaikoDrum": 117,
    "MelodicTom": 118,
    "SynthDrum": 119,
    "ReverseCymbal": 120,
    "GtFretNoise": 121,
    "BreathNoise": 122,
    "Seashore": 123,
    "BirdTweet": 124,
    "TelephRing": 125,
    "Helicopter": 126,
    "Applause": 127,
    "Gunshot": 128,
}


class MIDIUnit(SAM2695):
    SYNTH_INSTRUMENTS = SYNTH_INSTRUMENTS
    MIDI_NOTES = MIDI_NOTES

    def __init__(self, id: Literal[0, 1, 2], port: list | tuple) -> None:
        super().__init__(id, port)