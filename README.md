[![Documentation Status](https://readthedocs.org/projects/battlematica/badge/?version=latest)](https://battlematica.readthedocs.io/en/latest/?badge=latest)

# Battlematica

![alt text](https://github.com/f-rosato/battlematica/blob/master/battlematica_banner.png)

## What is this?

Battlematica is an open source Python coding game and research framework created by Federico Rosato. 
You write the AI for simulated battle bots and let them fight.

It was mainly inspired by the awesome [Gladiabots](https://gladiabots.com/)
 by [GFX47](https://github.com/GFX47) (check it out!), of which is a coder-oriented clone with slightly simplified mechanics.

## What's cool about Battlematica?
 
- You can define the stats of as many bot classes as you want;
- you can set up the starting position freely;
- most importantly, you have complete freedom and control over what's in the AIs.

Battlematica ships with a small language, BATTLANG, and a library of Python primitives that aids you in writing Gladiabots-style AIs, yet in Battlematica the full power of Python is unlocked to the power user.

Example BATTLANG script, to give you the flavor:

    ? me shield_level(0,50)
        ? enemy bot in_range(0,300) targeting here
            ? me carrying
                drop here
            move away_from nearest enemy bot with_target here
    
    ? me carrying
        drop at nearest ally port
    
    shoot nearest enemy bot in_range(0,100)
    shoot weakest enemy bot in_range(0,300) shield_level(0,25)
    shoot least_shield enemy bot in_range(0,200)
    
    ? me shield_level(75,100)
        ? not enemy bot shooting with_target here
            pick nearest ally artifact
            move to nearest enemy bot
    
    shoot least_shield enemy bot in_range(0,300)
    move to nearest enemy bot

## Can I see the pew-pew?

![alt text](https://github.com/f-rosato/battlematica/blob/master/screenshot.PNG)

Battlematica includes optional 2D graphics output through the [arcade](https://arcade.academy/) library.
 
The game engine is decoupled from the graphics by design and you can use it stand-alone if you want to run battles in batch.

Battlematica includes a structured .zip archive containing the 2D assets used, but if you want you can override it with your own archive (with the same structure) and thus customize everything to your liking.


## What can I do with it?

You can have fun writing awesome AIs with BATTLANG (Battlematica's own language), the included library, or experiment freely.
Some ideas that you can explore:

- stateful AIs
- team coordination
- neural networks
- reinforcement learning
- opponent modeling
- ...whatever you fancy to experiment with!

Battlematica lives, as I hope, at the intersection between fun and serious research in multiagent systems, AI and the likes. If you plan to use it the latter way, let me know!

## How do I use it?

[Read the docs!](https://battlematica.readthedocs.io/en/latest/)


## I'll read later, how do I just start a game?

(After setting up an environment with the requirements)

`python3 run_game.py -f 3v1_square.json  -t 1200  -d`

---
Contributions are welcome!
