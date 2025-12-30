title: Comparison of ANSI Terminal Emulators
date: 2025-01-13 02:58
modified: 2025-12-30 05:30
status: published
tags: comparison, color, terminal, vim, neovim, xfce4terminal, gnome-terminal
category: research
summary: A comparison of console terminals of its color handling.
keywords: comparison
lang: en
private: False

Focus is to ensure consistency of ANSI color scheme across terminal emulators, console/graphic.

ANSI Terminal Emulator is a text terminal or terminal emulator that supports in-banding of ANSI
escape sequences as outlined by following engineering standards:

* [ECMA-48](https://ecma-international.org/publications-and-standards/standards/ecma-48/)
* [ISO/IEC 6429](https://www.iso.org/standard/12782.html)
* [FIPS 86](https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub86-1981.pdf), National Bureau of Standards, U.S. Dept. of Commerce.
* [ANSI X3.64-1979](https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub86.pdf),
* JIS X 0211


With regard to [Vim Nftables syntax highlight](https://github.com/egberts/vim-nftables), the problem
is getting consistency of color scheme used in syntax highlighter between console and graphic editors.

Even with the vaunted consistent 16-ANSI-color got bastardized by Neovim amongst the editors,
to make it work with upcoming but heavily-laden, resource-intensive Language
Server Protocol (LSP) (and Microsoft Visual Code did well to preserve color scheme, unlike Neovim).


[jtable caption="terminal emulators" separator="," th=1 ai="1"]
name, Linux,macOS,BSD,Windows,Language,HW Accel,Image / Terminal Graphics Protocol Support, Sixel Support
[Alacritty](https://github.com/alacritty/alacritty),Linux,macOS,BSD,Windows,Rust,yes,yes,no
[BlackBox](https://gitlab.gnome.org/raggesilver/blackbox),Linux, , , ,Vala, no, yes, no
Cathode, ,macOS, , C++, yes, yes, no
[ConEmu](https://github.com/Maximus5/ConEmu), , , ,Windows, C++, yes, yes, no
[ConTour](https://github.com/contour-terminal/contour),Linux,macOS,BSD,Windows,C++, yes, yes, no
[Cool Retro Term](https://github.com/Swordfish90/cool-retro-term),Linux,macOS,, QML, yes, no, no
[Foot](https://codeberg.org/dnkl/foot#logo-a-terminal-with-a-foot-shaped-prompt-icons-hicolor-48x48-apps-foot-png-foot),Linux,,BSD, C, no, yes, yes
Ghostty,Linux,macOS,,
Hyper,Linux,macOS,,Windows
iTerm2,,macOS,,
Rio Terminal,Linux,macOS,BSD,Windows
Suckless Terminal,Linux,,,
Tabby,Linux,macOS,,Windows
Warp,Linux,macOS,,Windows
WezTerm,Linux,macOS,BSD,Windows
Windows Terminal,,,,Windows
xfce4-terminal,Linux,,,
xterm,Linux,macOS,BSD,

Kconsole,Linux,,,
gnome-terminal, default
hyper,
termius, `[termius.com]`
[/jtable]

[jtable caption="console terminals" separator="," th=1 ai="1"]
name, default scheme, script
vim, default, Vim
neovim, colorscheme, Vim
[/jtable]
