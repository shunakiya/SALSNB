# Secure Access Lock System with NFC and Biometrics

## Collaborators
- Shunsuke Akiya
- Christopher Cao
- Rafael Ceja
- Miguel Rodriguez
- Matthew Uy

---

## Overview

### Purpose
The Secure Access Lock System enhances the daily experience of locking and unlocking doors by automating the process. Users can unlock their doors using various methods, including a fingerprint sensor, an NFC card, or remotely via a web-based app. Traditional keys are included as a failsafe, ensuring accessibility for all.

### Objectives
1. Improve user quality of life by eliminating manual locking and unlocking.
2. Enhance home security with multiple authentication methods.
3. Incorporate AI to learn user habits and offer preemptive prompts via a smartphone app.

### Key Features
- **Authentication Methods**:
  - Fingerprint sensor for biometric access.
  - NFC cards/tags for quick, contactless unlocking.
  - Remote control via a web-based application.
  - Hidden keyhole for traditional manual unlocking.
- **Auto-Lock**: Automatically re-engages the lock after a preset period of inactivity.
- **Multi-Platform Compatibility**: Works with both iOS and Android.

---

## System Design

### Components
1. **Raspberry Pi**: The central control unit for processing data and managing lock operations.
2. **Fingerprint Sensor**: Biometric authentication module with green/red LED indicators for feedback.
3. **NFC Reader**: Allows unlocking using NFC-enabled devices or cards.
4. **Solenoid Lock**: The mechanical locking mechanism controlled by the Raspberry Pi.
5. **Relay**: Enables/disables the solenoid lock based on authentication signals.
6. **Power Source**: Powered by 3 AA batteries, with a backup key for emergencies.

### Inputs and Outputs
| Component          | Input                                 | Output                          |
|---------------------|---------------------------------------|---------------------------------|
| Raspberry Pi        | Fingerprint/NFC data, HTTP requests  | Relay signal, web app feedback |
| Fingerprint Sensor  | User fingerprint                     | Authentication result          |
| NFC Reader          | NFC tag/card proximity               | Authentication result          |
| Solenoid Lock       | Power from relay                     | Physical lock/unlock           |
| 3 AA Batteries      | N/A                                  | Power for system components    |

---

## User Guide

### Initial Setup
1. **Account Registration**: Create an account via the web-based app using Google or email/password.
2. **Device Pairing**: Pair the lock with your device using Bluetooth, then connect to Wi-Fi for remote access.
3. **Adding Fingerprints**: Follow the app's instructions to register fingerprints.

### App Features
- **Main Screen**:
  - Central button for remote unlocking.
  - Hamburger menu for additional options (device info, account settings, etc.).
- **Supported Platforms**: iOS and Android.

---

## Technical Details

### Power Supply
- Primary: 3 AA batteries housed in a secure casing.
- Backup: Manual key accessible behind the fingerprint sensor.

### Communication Protocols
- **NFC**: Two-way communication for tag/card authentication.
- **HTTP**: Data transmission between the Raspberry Pi and the web app.

### System Workflow
1. User provides input (e.g., fingerprint, NFC card, or app command).
2. Raspberry Pi processes the input and signals the relay.
3. Relay activates/deactivates the solenoid to lock/unlock the door.

---

## Testing and Results

| Test                   | Result                           |
|------------------------|----------------------------------|
| 9V battery for solenoid| Failed (insufficient power)     |
| 3 AA batteries         | Success (adequate power)        |
| Fingerprint recognition| Success (accurate and responsive) |
| NFC tag/card testing   | Success (validated multiple tags/cards) |

### Problem Areas
- Initial power supply (9V battery) proved inadequate and was replaced with 3 AA batteries.
- During testing, one AA battery exploded and was immediately replaced.

---

## Marketing Studies
- **Security Statistics**: 56% of home break-ins occur through doors. A secure smart lock system acts as a deterrent.
- **User Convenience**: 70% of people forget to lock their doors occasionally; remote control mitigates this issue.
- **Accessibility**: Enhances life for the 42.5 million Americans with disabilities.

---

## Future Improvements
- Integrating advanced power management.
- Refining mechanical components for enhanced durability.
- Expanding features to support voice assistants.
