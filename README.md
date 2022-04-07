# ESP-EYE width Edge Impulse

How to run custom inference on a ESP-EYE using Edge Impulse.

### Hardware

This code has only been tested on the ESP-EYE module.

![esp-eye](docs/esp-eye.jpg)

### Software

* [PlatformIO](docs/PLATFORMIO.md)

* Create your Image Classification model using [Edge Impulse](https://edgeimpulse.com).

* Due to the board limitations you will need to train your model with 96x96 images and use the MobileNetV1 0.01:*

    ![create-impulse](docs/create-impulse.png)

* Download the Arduino library under the `Deployment` tab in the Edge Impulse studio

    ![dl-arduino-lib](docs/deployment-tab.png)

### Image Classification Example

* Save the .zip library you have downloaded to [lib/](lib/) or use the default sample car library

    * Add library location to [platformio.ini](platformio.ini) if needed

        ```ini
        lib_deps = lib/<your-project>.zip
        ```

* Compile and deploy the code to your board

    ```bash
    pio run -t upload
    ```

* Open the serial monitor and use the provided IP to capture an image and run the inference:

    ```bash
    pio device monitor
    ```

    ![serial-output](docs/open-serial.png)

## Resources

- [TinyML ESP32-CAM: Edge Image classification with Edge Impulse](https://www.survivingwithandroid.com/tinyml-esp32-cam-edge-image-classification-with-edge-impulse/) 
- [https://github.com/v12345vtm/esp32-cam-webserver-arduino-simplified-arduino-html](https://github.com/v12345vtm/esp32-cam-webserver-arduino-simplified-arduino-html)
- [ESP32-CAM](https://github.com/edgeimpulse/example-esp32-cam)
