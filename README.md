# Battlematica

## What is this?

Battlematica is an open source Python coding game and research framework created by Federico Rosato. 
You write the AI for simulated battle bots and let them fight.

It was mainly inspired by the awesome [Gladiabots](https://gladiabots.com/)
 by [GFX47](https://github.com/GFX47) (check it out!), of which is a coder-oriented clone with slightly simplified mechanics.

## What's cool about Battlematica?
 
- You can define the stats of as many bot "models" as you want;
- you can set up the starting position freely;
- most importantly, you have complete freedom and control over what's in the AIs.

Battlematica ships with a library of primitives that aids you in writing Gladiabots-style AIs, yet in Battlematica the full power of Python is unlocked to the power user.


## Can I see the pew-pew?

![Screenshot](screenshot.png)

Battlematica includes optional 2D graphics output through the [arcade](https://arcade.academy/) library.
 
The game engine is decoupled from the graphics by design and you can use it stand-alone if you want to run battles in batch.

Battlematica includes a structured .zip archive containing the 2D assets used, but if you want you can override it with your own archive (with the same structure) and thus customize everything to your liking.


## What can I do with it?

You can have fun writing awesome AIs with the included library or experiment freely.
Some ideas that you can explore:

- stateful AIs
- team coordination
- neural networks
- reinforcement learning
- opponent modeling
- hijack an AI and read joypad inputs
- ...whatever you fancy to experiment with!

Battlematica lives, as I hope, at the intersection between fun and serious research in multiagent systems, AI and the likes. If you plan to use it the latter way, let me know!

## How do I use it?

Read the docs!

## I'll read later, how do I just start a game?

`python run_game.py -f 3v1_square.json  -t 1500  -d`

---
Contributions are welcome!