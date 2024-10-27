# Library for communication with the BNO055 sensor

## Dependencies
* smbus2

## Resources
Register values and address definitions can be found in the (datasheet)[https://cdn-shop.adafruit.com/datasheets/BST_BNO055_DS000_12.pdf].

## To-do
* Convert signed int raw sensor values to float (degree/rad)
* Check IMU mode --> implement Euler angles and Quaternion API
* Check calibration mode
* Calibrate sensor