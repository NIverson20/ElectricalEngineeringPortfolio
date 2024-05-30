# NNL Capstone Project: Energy Harvesting Embedded System

## Project Overview

This project, sponsered by the Naval Nuclear Labs, aimed to develop an energy-harvesting embedded system that operates independently of traditional power sources. This capability is crucial for applications where power availability is limited or non-existent.

## Importance of the Project

The system's ability to harness environmental energy allows it to capture critical temperature data continuously, without concerns about power outages or the need for battery replacements. This technology is vital for long-term environmental monitoring and other autonomous operations.

## Problem Statement

The objective was to create a microcontroller-based sensor prototype capable of logging temperature data without a power supply or battery for at least 30 days. The device would utilize various transducers to harness energy from solar, RF, heat, and vibration sources.

## Key System Requirements

- **Functional Requirements:** Record temperature data at intervals ranging from 30 seconds to 5 minutes for at least 30 days autonomously.
- **Non-Functional Requirements:** The device must operate as a closed system with secure, temporary hardwired connections for data transmission and withstand long periods without human intervention.

## My Role

- **System Design and Integration:** Involved in comparing and selecting microcontrollers based on their power consumption and capabilities. Also, designed and tested the integration of energy transducers with the microcontroller.
- **Data Analysis and Optimization:** Conducted extensive testing to optimize the power consumption of the microcontroller, achieving low power draws essential for long-term deployment.
- **Prototyping and Testing:** Assisted in the physical assembly of the device and conducted field tests to validate the functionality under various environmental conditions.

## Challenges and Solutions

A primary challenge was minimizing the power consumption of the microcontroller while maintaining reliable data logging capabilities. Through iterative design and testing, we achieved ambient power draws significantly lower than typical low-power devices, which was a critical success factor for the project.

## Results and Impact

The project demonstrated the feasibility of a self-sustaining microcontroller system, with power consumption low enough to allow indefinite operation under optimal conditions. This breakthrough paves the way for more widespread use of autonomous sensors in remote or challenging environments.

## Technical Details

- **Microcontroller Used:** MSP430FR5994, known for its low power consumption and sufficient memory capacity.
- **Energy Transducers:** Included solar cells and piezoelectric sensors, which were crucial for the device's energy autonomy.
- **Performance Metrics:** The system's power management was fine-tuned to achieve an operational power draw of approximately 5µW, with a potential indefinite lifespan under certain conditions.

## Next Steps

- Further development will focus on refining the energy management system, enhancing data transmission security, and fully integrating the system into a printed circuit board (PCB) for robustness and ease of deployment.

## Gallery

Here are some visuals from the project

![Logical Design Diagram](/images/nnl_capstone_images/nnl_logical_design.JPG)

**Figure 1: Logical Design Diagram** - This diagram outlines the logical structure of the field unit used in the microclimate monitoring system. It shows the integration of the sensor, processing unit, and power system within the unit, detailing the flow of data and energy.
![Logical Design Diagram](/images/nnl_capstone_images/nnl_micro_power_usage.JPG)

![Logical Design Diagram](/images/nnl_capstone_images/nnl_vibrational_voltage_output.JPG)

![Logical Design Diagram](/images/nnl_capstone_images/nnl_micro_power_usage.JPG)

![Logical Design Diagram](/images/nnl_capstone_images/nnl_micro_power_usage.JPG)
Thank you for exploring this project. For more detailed discussions or technical inquiries, feel free to contact me.

