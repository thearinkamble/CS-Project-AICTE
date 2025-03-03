from PIL import Image

# Function to encode data into the image
def encode_image(input_image_path, secret_message, output_image_path):
    image = Image.open(input_image_path)
    encoded_image = image.copy()
    width, height = image.size
    message_binary = ''.join([format(ord(char), '08b') for char in secret_message]) + '1111111111111110'  # End marker
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for channel in range(len(pixel)):
                if data_index < len(message_binary):
                    pixel[channel] = (pixel[channel] & ~1) | int(message_binary[data_index])
                    data_index += 1
            encoded_image.putpixel((x, y), tuple(pixel))
            if data_index >= len(message_binary):
                break
        if data_index >= len(message_binary):
            break
    
    encoded_image.save(output_image_path)
    print(f"Data successfully encoded into {output_image_path}")

# Function to decode data from the image
def decode_image(input_image_path):
    image = Image.open(input_image_path)
    binary_data = ''
    
    for y in range(image.height):
        for x in range(image.width):
            pixel = list(image.getpixel((x, y)))
            for channel in range(len(pixel)):
                binary_data += str(pixel[channel] & 1)
    
    binary_message = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ''
    for byte in binary_message:
        if byte == '11111110':  # End marker
            break
        decoded_message += chr(int(byte, 2))
    return decoded_message

# Example usage
if __name__ == "__main__":
    # Encode a message
    input_image = "input_image.png"  # Input image file path
    output_image = "output_image.png"  # Encoded image file path
    secret_message = "This is a secret message."
    encode_image(input_image, secret_message, output_image)

    # Decode the message
    decoded_message = decode_image(output_image)
    print("Decoded message:", decoded_message)
