# FreeRTOS — Best Practices

## Common scenarios
- Building secure, cloud-connected firmware for microcontroller-based IoT devices        → Security, Reliability
- Deploying and rotating firmware/security patches across a device fleet via OTA        → Security, Operational Excellence
- Sizing constrained MCU RAM/flash for kernel objects, TLS, and application tasks        → Performance Efficiency, Cost Optimization
- Qualifying a board/port and keeping it on a supported, patched FreeRTOS version        → Reliability, Operational Excellence

## 🔒 Security
- **[Transport security]** Use TLS 1.2 or later (TLS 1.3 recommended) with mutual X.509 certificate authentication for every device connection to AWS IoT Core — this is what keeps data private and both endpoints authenticated in transit. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/infrastructure-security.html)
- **[Cipher suites]** Require cipher suites with perfect forward secrecy (DHE or ECDHE) rather than static key exchange — most modern TLS stacks support these modes, and PFS limits the blast radius if a key is later compromised. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/infrastructure-security.html)
- **[Key storage]** Store device secrets and private keys in a Hardware Root of Trust (secure element or secure enclave) rather than plain flash — this prevents a temporary or offline compromise from becoming permanent. [doc](https://docs.aws.amazon.com/freertos/latest/qualificationguide/freertos-qualification.html)
- **[Randomness]** Use a True Random Number Generator (TRNG) for the FreeRTOS libraries implementing DHCP, DNS, TCP/IP, and TLS — weak or predictable randomness enables network spoofing and man-in-the-middle attacks. [doc](https://docs.aws.amazon.com/freertos/latest/qualificationguide/freertos-qualification.html)
- **[Key management]** Access and manage cryptographic keys and objects through the PKCS #11 API rather than ad hoc storage, and prefer dedicated cryptographic hardware for keys when the device needs data-at-rest protection. [doc](https://aws.amazon.com/freertos/faqs/)
- **[Code integrity]** Digitally sign firmware images with Code Signing for AWS IoT (or your own signing tooling) before every OTA deployment — the device verifies the signature so tampered images are rejected before being installed. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html)
- **[Provisioning]** Provision unique per-device X.509 identity at manufacturing time using Just-in-Time Provisioning/Registration where possible, or Fleet Provisioning when unique credentials can't be embedded before sale — avoid shared or hardcoded credentials across devices. [doc](https://docs.aws.amazon.com/whitepapers/latest/device-manufacturing-provisioning/provisioning-identity-in-aws-iot-core-for-device-connections.html)
- **[Patch awareness]** Track FreeRTOS security updates through the FreeRTOS console, the Security Updates page, and GitHub, and apply them promptly via OTA — unpatched known vulnerabilities on deployed fleets are a primary compromise vector. [doc](https://aws.amazon.com/freertos/faqs/)

## 🛡️ Reliability
- **[OTA verification]** Have the OTA Agent verify digital signature, checksum, and version number of every downloaded image, and only commit the update after application-defined validation succeeds — this prevents a bad or corrupted image from bricking devices at scale. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/dev-guide-ota-workflow.html)
- **[Rollback safety]** Deploy an initial firmware version and verify it is running correctly before layering further OTA updates, and use a bootloader that supports OTA rollback — this bounds the blast radius of a failed update. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/dev-guide-ota-workflow.html)
- **[Connection resilience]** Implement exponential backoff with jitter when reconnecting the MQTT/TLS session after a dropped connection, rather than retrying immediately or at a fixed interval — this avoids reconnection storms against AWS IoT Core after fleet-wide network events. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/mqtt-demo-ma.html)
- **[State durability]** Use AWS IoT Device Shadow to persist desired/reported device state so that commands issued while a device is offline are applied automatically on reconnect, instead of relying on devices always being connected. [doc](https://aws.amazon.com/freertos/features/)
- **[LTS stability]** Build production firmware on a FreeRTOS Long Term Support (LTS) release rather than mainline — LTS guarantees stable public APIs, file structure, and build process while still delivering security and critical-bug patches. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-versioning.html)

## ⚡ Performance Efficiency
- **[Heap strategy]** Choose the FreeRTOS heap implementation (heap_1 through heap_5) that matches your allocation pattern — e.g. heap_4/heap_5 when you need coalescing and fragmentation control, heap_1 when objects are never freed and determinism matters most. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/application-memory-management.html)
- **[Static allocation]** Prefer static, compile-time allocation of RTOS objects (tasks, queues) over dynamic heap allocation where RAM budgets are tight — this avoids the non-determinism and fragmentation risk of runtime `pvPortMalloc()` calls. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/kernel-memory-allocation.html)
- **[Offload sizing]** Offload the communication and crypto stack to a networking co-processor when the main MCU is resource-constrained — this can reduce the main MCU's requirement from >25 MHz/>64 KB RAM down to roughly 10 MHz/16 KB RAM. [doc](https://aws.amazon.com/freertos/faqs/)
- **[Image sizing]** Budget program memory for two full executable images stored simultaneously (roughly 128 KB each) when supporting OTA updates, since the new image must coexist with the running image during the update. [doc](https://aws.amazon.com/freertos/faqs/)

## 💰 Cost Optimization
- **[LTS/EMP adoption]** Standardize on FreeRTOS LTS, and enroll long-lived devices in the Extended Maintenance Plan (EMP) when the field lifecycle exceeds the LTS window — this avoids costly, disruptive major-version upgrades on devices already deployed. [doc](https://aws.amazon.com/blogs/aws/new-freertos-extended-maintenance-plan-for-up-to-10-years/)
- **[Right-sized hardware]** Match MCU processing speed and RAM to the actual protocol/crypto footprint needed (full stack on-chip vs. offloaded to a connectivity module) instead of over-provisioning hardware for every unit in the fleet. [doc](https://aws.amazon.com/freertos/faqs/)

## ⚙️ Operational Excellence
- **[Board qualification]** Run your port through AWS IoT Device Tester (IDT) against the FreeRTOS-Libraries-Integration-Tests and Device Advisor test cases before shipping — this catches interoperability and protocol-compliance issues prior to field deployment. [doc](https://docs.aws.amazon.com/freertos/latest/qualificationguide/freertos-qualification.html)
- **[Version pinning]** Use the exact library version combinations published in a release's `manifest.yml` rather than mixing library versions — FreeRTOS only tests and supports specific version-tagged bundles for interoperability. [doc](https://docs.aws.amazon.com/freertos/latest/qualificationguide/afr-qualification-faqs.html)
- **[Fleet update process]** Drive firmware and security-patch rollout through AWS IoT Device Management OTA jobs (choosing MQTT/HTTP delivery, target groups, and rollout pace) rather than ad hoc field updates — this gives you progress monitoring and the ability to debug failed deployments. [doc](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html)
- **[Fleet health]** Integrate AWS IoT Device Defender to continuously audit device-side configuration and detect behavioral anomalies across the fleet, rather than only reacting to individual device reports. [doc](https://aws.amazon.com/freertos/features/)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
