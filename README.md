# Mission Control Backend

> 🚧 **Work in Progress**  
> This project is actively under development. Features, architecture, and APIs may change as the simulator evolves.

## Overview

Mission Control Backend is a Python-based backend that simulates the software used by spacecraft mission operations teams. The project focuses on the ground segment of a mission rather than spacecraft flight software, providing a collaborative environment where multiple users can monitor telemetry, issue commands, and interact with a simulated spacecraft in real time.

The long-term goal is to build a realistic mission operations simulator with support for real-time telemetry streaming, multi-user collaboration, subsystem simulation, command processing, fault injection, and mission scenarios.

---

## Current Features

- Multi-user mission rooms
- Participant roles and permissions
- Command processing and validation
- Mission event logging
- WebSocket infrastructure for live telemetry streaming
- Mission state management
- Telemetry generation pipeline
- Modular service-oriented architecture

---

## Planned Features

- Spacecraft subsystem simulation
  - Power
  - Thermal
  - Communications
  - Orbit
  - Payload
- Orbit propagation through an interchangeable provider architecture
- Fault injection and anomaly simulation
- Mission scenarios and scripted events
- Authentication and persistent storage
- AI-powered mission assistant

---

## Architecture

The project follows a modular architecture with clear separation of responsibilities.

```text
Mission Room
│
├── Mission State
│   ├── Orbit
│   ├── Power
│   ├── Thermal
│   ├── Communications
│   └── Fault Manager
│
├── Command Service
├── Telemetry Service
├── Room Manager
└── WebSocket Manager
```

---

## Technology Stack

- Python
- FastAPI
- WebSockets
- Pydantic
- Dataclasses
- AsyncIO

Future integrations may include PostgreSQL, SQLAlchemy, JWT authentication, and professional orbital mechanics libraries.

---

## Status

The project is currently in active development.

Current work includes:

- Expanding the spacecraft simulation model
- Implementing subsystem-based mission state
- Designing an extensible orbit propagation architecture
- Building realistic mission operations workflows

Additional features and documentation will be added as the project progresses.
