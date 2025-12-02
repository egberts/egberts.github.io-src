title: Comparison of Console Editors of its Color Handling
date: 2025-01-13 02:58
modified: 2025-07-13T03:55
status: published
tags: comparison, color, terminal, vim, neovim, xfce4terminal, gnome-terminal
category: research
summary: A comparison of console terminals of its color handling.
keywords: comparison
lang: en
private: False


With regard to [Vim Nftables syntax highlight](https://github.com/egberts/vim-nftables), the problem
is getting consistency of color scheme used in syntax highlighter between various console and graphic editors.

Even with the vaunted consistent 16-ANSI-color were bastardized by Neovim among the many editors, 
presumably JUST to make it work with upcoming but heavily-laden, resource-intensive Language 
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
termius, [termius.com]
[/jtable]

[jtable caption="console terminals" separator="," th=1 ai="1"]
# caption - the table caption
# separator - default is comma
# th - table header (=0 means disable)
# ai - auto-index, adds a column numbering starts at 1
name, default scheme, script 
vim, default, Vim
neovim, colorscheme, Vim
# : if the date is not specified and DEFAULT_DATE is set to 'fs', Pelican will rely on the file’s “mtime” timestamp, and the category can be determined by the directory in which the file resides.
[/jtable]
