from PIL import Image
import time


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


def validate_message_capacity(img, message):
    width, height = img.size
    max_message_length = (width * height * 3) // 8  
    if len(message) + 3 > max_message_length:  
        return False, max_message_length
    return True, max_message_length


def encode_message(image_path, message, output_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("Error: Image file not found. Please provide a valid path.")
        return
    except Exception as e:
        print(f"Error: Unable to open image file. {e}")
        return

    message += "###"  
    binary_message = text_to_binary(message)

   
    can_fit, max_length = validate_message_capacity(img, message)
    if not can_fit:
        print(f"Error: Message too long to encode. Max message length: {max_length - 3} characters.")
        return

    pixels = list(img.getdata())  
    encoded_pixels = []
    message_index = 0

    for pixel in pixels:
        if message_index >= len(binary_message):
            encoded_pixels.append(pixel)
        else:
            encoded_pixel = list(pixel)
            for i in range(3):  
                if message_index < len(binary_message):
                    encoded_pixel[i] = encoded_pixel[i] & ~1 | int(binary_message[message_index])
                    message_index += 1
            encoded_pixels.append(tuple(encoded_pixel))

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(encoded_pixels)
    encoded_img.save(output_path)
    print("Message encoded successfully!")


def decode_message(image_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("Error: Image file not found. Please provide a valid path.")
        return ""
    except Exception as e:
        print(f"Error: Unable to open image file. {e}")
        return ""

    pixels = list(img.getdata())  
    binary_message = ""

    for pixel in pixels:
        for i in range(3):  
            binary_message += str(pixel[i] & 1)
            if len(binary_message) % 8 == 0:  
                char = binary_to_text(binary_message[-8:])
                if char == "#" and binary_message[-24:] == text_to_binary("###"):  
                    return binary_to_text(binary_message[:-24])

    return "No hidden message found."


# A menu to choose between encoding and decoding
def main():
    print("What do you want to do?")
    print("1. Encode a message")
    print("2. Decode a message")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":

        image_path = input("Enter the path of the image you want to encode: ")
        message = input("Enter the message you want to encode: ")
        output_path = input("Enter the path to save the encoded image (e.g., /path/to/save/encoded_image.png): ")

        
        if not output_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("Error: Specify a correct image file extension (e.g., .png, .jpg).")
        else:
            encode_message(image_path, message, output_path)

    elif choice == "2":

        image_path_decode = input("Enter the path of the image to decode (e.g., /path/of/encoded/image.png): ")


        start_time = time.time()
        decoded_message = decode_message(image_path_decode)
        end_time = time.time()


        total_time = end_time - start_time
        minutes = int(total_time // 60)
        seconds = total_time % 60
        print("Decoded Message:", decoded_message)
        print(f"Time taken to decode: {minutes} minute(s) and {seconds:.2f} second(s)")

    else:
        print("Choose 1 or 2.")

if __name__ == "__main__":
    main()
