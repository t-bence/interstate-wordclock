# interstate-wordclock

This repo is about implementing the word clock on the Pimoroni Interstate75 board using MicroPython.

## Resources

- My version of the Interstate 75: <https://shop.pimoroni.com/products/interstate-75-w?variant=54977948713339>
- Getting started docs: <https://github.com/pimoroni/interstate75/blob/main/README.md> (again, I have the RP2350 version)
- Released MicroPython and sample files: <https://github.com/pimoroni/interstate75/releases/latest> -- I was using i75w_rp2350-v0.0.5-micropython-with-filesystem.uf2. The "with-filesystem" means there are examples.
- Getting started with the Interstate 75, including photos of wiring it up: <https://learn.pimoroni.com/article/getting-started-with-interstate-75>
- The file to get started with: <https://github.com/pimoroni/interstate75/blob/main/examples/today.py>

## Word clock

Let's get started with the [today example](https://github.com/pimoroni/interstate75/blob/main/examples/today.py)

You will need to add a secrets.py as well, with two variables for the SSID and the network password.

## Directions

Take a look at the two arrows on the back of the panel. They should point up and right, then the display is in the expected position. X starts from the left, Y starts from the top.

## TODO

- [x] Get proper word indices for WORD_POSITIONS
- [ ] Think about the letter sizing again. The outermost cells should extend a bit out of the LED array I think.
- [ ] Implement a Display class that wraps the i75.display and handles drawing words with a `show_time(hour: int, minute: int)` method
- [ ] Create a mock display class
- [ ] Test the code
- [ ] Create tests for pull requests
