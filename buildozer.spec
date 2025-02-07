[app]
title = Tetris
package.name = tetris
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,wav,mp3
version = 1.0

requirements = python3,kivy,pygame

orientation = portrait

android.permissions = INTERNET

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1 