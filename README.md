Bluetooth Proximity Locker for elementary OS
==============

Lock/unlock your elementary computer based on proximity of bluetooth device (e.g. your phone or tablet).

This works for me under elementary OS 0.3 Freya.

- First step is to pair your device with your computer.
- Then get the devices address from System Settings > Bluetooth, or by running `bluez-test-device list` in the terminal.
- Then configure the script to run in the background at system startup (TODO)

Here's how it works:

1. The script pings the bluetooth device.
2. When the device moves out of range of the computer, the pings fail and the screen will lock.
3. Once the device is out of range, the script pings every second attempting to find the device again.
4. As soon as it pings successfully (you're back in range) the screen will automatically unlock again (WIP).

Replication of functionality of [blueproximity](https://launchpad.net/blueproximity) as this does not work in Freya. Likely to move to that in Loki.

### Roadmap
- Ignore locking attempts for separate duration after unlock.
- Implement plug patch for bluetooth locking in `Security & Privacy` > `Locking`
