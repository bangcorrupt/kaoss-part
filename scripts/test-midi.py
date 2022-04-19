import mido

print()
print('Test MIDI', '\n')
#print('MIDI Inputs:  ', mido.get_input_names(), '\n')
#print('MIDI Outputs: ', mido.get_output_names(),'\n')

serial_inp = mido.open_input('Scarlett 8i6 USB:Scarlett 8i6 USB MIDI 1 32:0')
serial_outp = mido.open_output('Scarlett 8i6 USB:Scarlett 8i6 USB MIDI 1 32:0')

usb_inp = mido.open_input('KP3:KP3 KP3 _ SOUND 36:0')
usb_outp = mido.open_output('KP3:KP3 KP3 _ SOUND 36:0')

def sysex_response(inport):
    #return
    for msg in inport:
        if msg.type == 'sysex':
            response = msg.hex()
            break
    return response

dev_inq = mido.Message('sysex', data=[0x7e, 0x7f, 0x06, 0x01])

serial_outp.send(dev_inq)
serial_response = sysex_response(serial_inp)
print(serial_response)

usb_outp.send(dev_inq)
usb_response = sysex_response(usb_inp)
print(usb_response)
print()

if serial_response == usb_response:
    print('Success: Serial MIDI response matches USB MIDI response.', '\n')
else:
    print('Fail: Serial MIDI response does not match USB MIDI response.', '\n')

print('Test Audio', '\n')

serial_outp.send(mido.Message('control_change', control=12, value=0x3f))
serial_outp.send(mido.Message('control_change', control=13, value=0x3f))
serial_outp.send(mido.Message('control_change', control=92, value=0x7f))
serial_outp.send(mido.Message('control_change', control=93, value=0x7f))
serial_outp.send(mido.Message('control_change', control=94, value=0x7f))
serial_outp.send(mido.Message('control_change', control=95, value=0x7f))
serial_outp.send(mido.Message('program_change', program=60))

print('Pad-On=0x7f, Pad-X=0x3f, Pad-Y=0x3f, Hold=0x7f, Depth=0x7f, Level=0x7f', '\n')
print('Program=60', '\n')
print('Audio should have delay fx applied.', '\n')


