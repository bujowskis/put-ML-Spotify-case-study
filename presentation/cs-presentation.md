<style>
body {
  overflow-y: auto !important;
}
</style>

Recommendation of harder styles music on Spotify
========================================================
author: Szymon Bujowski
date: 5/12/2022
autosize: true

Acknowledgements
========================================================

![PUT-img](./res/PP_logotyp_ANG_RGB.png)

## Artificial Intelligence - Machine Learning classes
## dr hab. inz. Izabela Szczech

===
# Introduction

Music
===

![music headphones](res/music-headphones.jpg)

Harder styles
===

<img src="res/Thunderdome_logo.jpg" height=300 />
<img src="res/defqon-logo.png" height=300 />
<img src="res/dominator-logo.jpg" height=300 />

What is considered "Harder"?
===

- Techno
- Acid
- Frenchcore
- Hardstyle
- Hardcore
- Gabber
- Piepcore
- Uptempo
- (so on ...)

Music streaming
===

![best music streaming services 2022](res/music-streaming.webp)

Market share
===

![Global music streaming market](./res/MIDiA-music-streaming-subscription-market.png)

Problem
===

![problem](res/frustrated-problem.jpg)

===
# The data

Attributes
========================================================

- meta
  - **name**
  - **artists**
  - **uri**
- **acousticness** - [0.0, 1.0] *(not acoustic, acoustic)*
  - acoustic - primarily uses instruments to produce sound through acoustic means
  - opposite to electric/electronic means
- **danceability** - [0.0, 1.0] *(not good - good)*
- **energy** - [0.0, 1.0] *(not so much, very)*
- **instrumentalness** - [0.0, 1.0] *(lyrical, instrumental)*
- **key** - C, C#, (...), B *[0, 1, (...), 11] mapping, according to standard Pitch Class notation*
- **liveness** - [0.0, 1.0] *(studio recording, live performance)*
- **loudness** - (-inf, **-60, 0**, inf) *(quiet, loud)*
- **mode** - binary *0: minor, 1: major*
- **speechiness** - [0.0, 1.0] *(no speech detected, speech-intensive)*
- **tempo** - [0.0, inf) *overall estimated tempo in BPM*
- **time_signature** - [0, 1, (...), inf] *number of beats in each bar*
- **valence** - [0.0, 1.0] *(sounds negative, sounds positive)*
- **liked** - binary *True/False*

Working dataset
===

<img src="res/working-liked.png" width=1000 />

- 420 songs total
- relatively balanced
  - Blue: Liked
  - Red: Disliked

Acousticness
===

<img src ="res/working-acousticness.png" width=1000 />

- mostly electronic/electric sounds (as expected)

Danceability
===

<img src ="res/working-danceability.png" width=1000 />

- similar to normal distribution
- small shift towards **danceable** in **liked**
- unsure about the definition of *danceable*

jumpstyle

![jumpstyle](res/jump-style.gif)

shuffle dance

![shuffle dance](res/shuffle.gif)

gabber, hakken

![hakken](res/gabber.gif)

Energy
===

<img src ="res/working-energy.png" width=1000 />

- very energetic in general

Instrumentalness
===

<img src ="res/working-instrumentalness.png" width=1000 />

- most songs contain vocals
- it seems lower no. of vocals tends to be more liked

Key
===

<img src ="res/working-key.png" width=1000 />

F - A - A# - C# - G - E - B -  G# -  D - C - F# - D#

- some preference can be seen
  - Like A
  - Like A#
  - Like B
  - Like G#

Liveness
===

<img src ="res/working-liveness.png" width=1000 />

- mostly studio recordings (as expected)

Loudness
===

<img src ="res/working-loudness.png" width=1000 />

- **loud** side of the spectrum
- it's **not** just about being loud
- Disliked songs are very loud
  - outlier - relatively quiet

Mode
===

<img src ="res/working-mode.png" width=1000 />

Minor - Major

- Minor more or less balanced
- small preference for Major

Speechiness
===

<img src ="res/working-speechiness.png" width=1000 />

- majority has little to no speech (as expected)

Tempo
===

<img src ="res/working-tempo.png" width=1000 />

- 100-145BPM and 160-190BPM seem to be the sweet spots (more or less expected)

Time_signature
===

<img src ="res/working-time_signature.png" width=1000 />

- most songs are made in time signature of 4 (general trend)
- 3 and 1 respectively next in popularity (general trend)

Valence
===

<img src ="res/working-valence.png" width=1000 />

- majority sounds negative (as expected)

===
# Correlations

(X-axis first, Y-axis second)

Energy - Loudness
===

<img src ="res/working-corr-energy-loudness.png", width=1000 />

- louder tracks are more energetic
- nice and expected

Speechiness - Energy
===

<img src ="res/working-corr-speechiness-energy.png" width=1000 />

- great majority is very energetic
- not energetic are low on speechiness
  - speech gives energy?

(The same goes for Speechiness - Loudness because of Energy - Loudness correlation)

===
# Classification

- 10-Folds Cross-validation for all of the algorithms

J48
===
