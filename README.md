# ESP-EYE with Edge Impulse

How to run object detection on an ESP-EYE using Edge Impulse.

## Quickstart - Dog Detection (Ubuntu)

Plug your ESP-EYE into your PC's USB port then type in this:

```bash
# Clone repo, enter, and run
git clone https://github.com/JimothyJohn/uEye && cd uEye && ./Quickstart.sh
```

## Hardware

This code has only been tested on the [ESP-EYE](https://www.mouser.com/ProductDetail/?qs=l7cgNqFNU1iWrlpTZmwCRA%3D%3D) module.

![esp-eye](docs/esp-eye.jpg)

## Software

- [PlatformIO](docs/PLATFORMIO.md)

- Create your model using [Edge Impulse](https://docs.edgeimpulse.com/docs/edge-impulse-studio/data-acquisition).

- Due to the board limitations you will need to train your model with 96x96 images and use the MobileNetV1 0.01:\*

  ![create-impulse](docs/create-impulse.png)

- Download the Arduino library under the `Deployment` tab in the Edge Impulse studio

  ![dl-arduino-lib](docs/deployment-tab.png)

## Object Detection Example

- Save the .zip library you downloaded to [lib/](lib/)

  - Add library location to [platformio.ini](platformio.ini) if needed

    ```ini
    lib_deps =
      lib/<your-project>.zip
    ```

- Compile and deploy the code to your board

  ```bash
  pio run -t upload && pio device monitor
  ```

## Resources

- [TinyML ESP32-CAM: Edge Image classification with Edge Impulse](https://www.survivingwithandroid.com/tinyml-esp32-cam-edge-image-classification-with-edge-impulse/)
- [https://github.com/v12345vtm/esp32-cam-webserver-arduino-simplified-arduino-html](https://github.com/v12345vtm/esp32-cam-webserver-arduino-simplified-arduino-html)
- [ESP32-CAM](https://github.com/edgeimpulse/example-esp32-cam)
- [ESP-EYE](https://docs.edgeimpulse.com/docs/development-platforms/officially-supported-mcu-targets/espressif-esp32)

### To-do (test-driven)

- Establish separate endpoints for image, predictions, and metrics
- Convert to async webserver
- Add telemetry for location via 6-axis transformations
