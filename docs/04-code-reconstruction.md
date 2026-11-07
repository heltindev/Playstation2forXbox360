# 04 · Reconstructing Portable Game Code

[← Reverse engineering](03-reverse-engineering.md) · [Next: Assets →](05-asset-pipeline.md)

> **Goal:** Implement observable game behavior without binding it to PS2-specific APIs or Xbox 360 hardware.

## Build an interface, not a giant decompilation dump

The original MIPS executable cannot be linked as ordinary PowerPC object code. A decompiler gives candidate pseudocode, not a buildable original project. Reconstruct small systems with clear inputs and outputs, then test against observed behavior.

Suggested design:

```text
src/
├── game/
│   ├── scene.cpp
│   ├── player.cpp
│   ├── camera.cpp
│   └── physics.cpp
├── engine/
│   ├── input.hpp
│   ├── renderer.hpp
│   ├── audio.hpp
│   └── filesystem.hpp
├── platform/
│   ├── desktop/
│   └── xbox360/
└── tests/
    └── gameplay_tests.cpp
```

This is a proposed layout; no port is implemented by this repository.

## Define platform-neutral contracts

```cpp
struct InputState {
    float moveX = 0.0f;
    float moveY = 0.0f;
    bool jumpPressed = false;
};

struct PlayerState {
    float positionX = 0.0f;
    float positionY = 0.0f;
    float velocityY = 0.0f;
};

void updatePlayer(PlayerState& player,
                  const InputState& input,
                  float deltaSeconds);
```

This code is deliberately independent of hardware. The desktop and Xbox backends each supply controller state, frame timing and rendering services.

## Recommended reconstruction order

1. **Scene and game state:** identify which states exist and how transitions occur.
2. **Input translation:** normalize buttons, sticks, dead zones and action edges.
3. **Movement and camera:** reproduce units, speeds and update order.
4. **Collision/physics:** study discrete steps, broadphase and callbacks.
5. **Actors and scripting:** identify entity storage, event ordering and triggers.
6. **Asset calls:** replace direct resource access with a validated loader.
7. **Rendering and audio commands:** issue logical operations to separate backends.
8. **Persistence:** model save data, version and failure behavior.

## Frame rate is a compatibility question

If the original game advances physics once per video frame, changing the update frequency may alter movement and collision. Measure the source game's behavior before choosing a fixed timestep.

An illustrative engine accumulator:

```cpp
constexpr double step = 1.0 / 60.0;
double accumulator = 0.0;

void tick(double elapsedSeconds) {
    accumulator += elapsedSeconds;
    while (accumulator >= step) {
        // simulateFixedStep(step);
        accumulator -= step;
    }
}
```

This is educational pseudocode, **not** a claim that the target game uses 60 Hz.

## Numerical fidelity matters

Differences between MIPS and PowerPC computations can affect gameplay. Test:

- Coordinate handedness and matrix order.
- Integer overflow, fixed-point values and bit shifts.
- Floating-point rounding and instruction behavior.
- Animation interpolation and normalization.
- Random number generation and determinism.
- Structure layout, endianness and binary serialization.

Do not optimize for Xbox 360-specific vector instructions until the portable implementation is correct.

## Static recompilation: realistic limits

Experimental static recompilation can be helpful when instruction behavior is understood. It still must handle MIPS-specific code, self-modification if present, memory maps, ABI differences, VU/GS/IOP services and the original runtime's assumptions. It should be treated as a research technique, **not** an automatic complete-port solution.

## Module exit criteria

- [ ] Platform-neutral interface.
- [ ] Reproducible test inputs and expected outcomes.
- [ ] At least two boundary cases tested.
- [ ] Cross-platform representation documented.
- [ ] Memory safety and ownership reviewed.
- [ ] Differences from the original recorded.
- [ ] No copyrighted executable contents committed.

[Next: Asset pipeline →](05-asset-pipeline.md)
