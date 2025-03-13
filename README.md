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
